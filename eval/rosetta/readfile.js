var fs = require("fs");
const filename = process.argv[2];

var readFile = function(path) {
    return fs.readFileSync(path).toString();
};

console.log(readFile(filename));
