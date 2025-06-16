char rot13(char c) {
    if (c >= 'a' && c <= 'z') {
        return ((c - 'a' + 13) % 26) + 'a';
    } else if (c >= 'A' && c <= 'Z') {
        return ((c - 'A' + 13) % 26) + 'A';
    } else {
        return c; // Non-alphabetic characters remain unchanged
    }
}
