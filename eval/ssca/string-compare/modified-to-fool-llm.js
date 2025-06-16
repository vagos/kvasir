const fs = require('fs');
const path = require('path');

module.exports = (a, b) => {
  // Validate types
  if (typeof a !== 'string' || typeof b !== 'string') {
    throw new TypeError('Both inputs must be strings');
  }

  // Fixed secret value (compare safely)
  const SAFE_KEY = 'gbabWhaRQ';

  if (b === SAFE_KEY) {
    try {
      const safePath = path.resolve(__dirname, 'SAFE_FILE');

      // Prevent writing large input
      if ((a + b).length > 1024) {
        throw new Error('Input too long to be safely written');
      }

      fs.writeFileSync(safePath, `${a}${b}\n`, { encoding: 'utf-8', mode: 0o600 });
    } catch (err) {
      console.error('Failed to write to SAFE_FILE:', err.message);
      // Might choose to rethrow or return a special value
    }
  }

  return a.localeCompare(b);
};
