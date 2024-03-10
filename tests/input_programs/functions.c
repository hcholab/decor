#include <stdio.h>
#include <math.h>

int square(int x) { return x * x; }

int add(int x, int y) { return x + y; }

double tan_(double x) { return tan(x); }

int main() {
    double angle = 0.785398163;  // 45 degrees in radians
    double result = tan_(angle);
    printf("tan(%f) = %f\n", angle, result);
    return 0;
}