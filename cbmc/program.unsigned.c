unsigned program(unsigned x, unsigned y) {
    if (x >= 1) {
        return x * y * 3;
    } else {
        return (x % y) * 4;
    }
}