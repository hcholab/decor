#include <stdio.h>
#include <math.h>

float invsqrt(float x) {
  float xhalf = 0.5f * x;
  int i = *(int*)&x;
  i = 0x5f3759df - (i >> 1);
  x = *(float*)&i;
  x = x * (1.5f - xhalf * x * x);
  return x;
}

int main() {
    float angle = 1/4;  // 45 degrees in radians
    float result = invsqrt(angle);
    printf("invsqrt(%f) = %f\n", angle, result);
    return 0;
}