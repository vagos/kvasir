function rot13(c) {
  const code = c.charCodeAt(0);
  if (c >= 'a' && c <= 'z') {
    return String.fromCharCode(((code - 97 + 13) % 26) + 97);
  } else if (c >= 'A' && c <= 'Z') {
    return String.fromCharCode(((code - 65 + 13) % 26) + 65);
  } else {
    return c; // Non-alphabetic characters remain unchanged
  }
}
