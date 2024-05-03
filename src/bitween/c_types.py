import random

# Mapping of type names to their corresponding format specifiers.
format_specifiers = {
    "double": "%lf",
    "float": "%f",
    "int": "%d",
    "unsigned int": "%u",
    "long": "%ld",
    "unsigned": "%u",  # Assuming unsigned int
    "unsigned long": "%lu",
    "long long": "%lld",
    "unsigned long long": "%llu",
    "size_t": "%zu",  # Use "%u" or "%lu" for older C versions without C99 support
    "uint8_t": "%hhu",
    "uint16_t": "%hu",
    "uint32_t": "%u",  # Assuming uint32_t maps to unsigned int
    "uint64_t": "%llu",  # Assuming uint64_t maps to unsigned long long
    "int8_t": "%hhd",
    "int16_t": "%hd",
    "int32_t": "%d",  # Assuming int32_t maps to int
    "int64_t": "%lld",  # Assuming int64_t maps to long long
    "long double": "%Lf",
    "float32_t": "%f",  # Assuming float32_t maps to float
    "float64_t": "%lf",  # Assuming float64_t maps to double
    "float128_t": "%Lf",  # Assuming float128_t maps to long double
    "double32_t": "%f",  # Assuming this is a non-standard type that maps to float
    "double64_t": "%lf",  # Assuming double64_t maps to double
    "double128_t": "%Lf",  # Assuming double128_t maps to long double
}

int_types = {
    "int",
    "unsigned int",
    "long",
    "unsigned",
    "unsigned long",
    "long long",
    "unsigned long long",
    "size_t",
    "uint8_t",
    "uint16_t",
    "uint32_t",
    "uint64_t",
    "int8_t",
    "int16_t",
    "int32_t",
    "int64_t",
}

int_upper_bound_civl = 100

float_types = {
    "float",
    "double",
    "long double",
    "float32_t",
    "float64_t",
    "float128_t",
    "double32_t",
    "double64_t",
    "double128_t",
}

flouat_upper_bound_civl = 100.0

random_functions = {
    # 32-bit signed
    "int": (random.randint, (0, 300)),
    # IEEE 754 single-precision
    "float": (random.uniform, (-5, 5)),
    # IEEE 754 double-precision
    "double": (random.uniform, (-5, 5)),
    # 64-bit signed
    "long": (random.randint, (0, 300)),
    # Assuming unsigned int, 32-bit
    "unsigned": (random.randint, (0, 300)),
    # 32-bit unsigned
    "unsigned int": (random.randint, (0, 300)),
    # 64-bit unsigned
    "unsigned long": (random.randint, (0, 300)),
    # 64-bit signed
    "long long": (random.randint, (-9223372036854775808, 9223372036854775807)),
    # 64-bit unsigned
    "unsigned long long": (random.randint, (0, 18446744073709551615)),
    # IEEE 754 extended double-precision (commonly 80-bit on x86-64, but up to 128-bit on some systems)
    "long double": (random.uniform, (-1.1e4932, 1.1e4932)),
    # Assuming size_t is 64-bit unsigned
    "size_t": (random.randint, (0, 18446744073709551615)),
    "uint8_t": (random.randint, (0, 255)),
    "uint16_t": (random.randint, (0, 65535)),
    "uint32_t": (random.randint, (0, 4294967295)),
    "uint64_t": (random.randint, (0, 18446744073709551615)),
    "int8_t": (random.randint, (-128, 127)),
    "int16_t": (random.randint, (-32768, 32767)),
    "int32_t": (random.randint, (-2147483648, 2147483647)),
    "int64_t": (random.randint, (-9223372036854775808, 9223372036854775807)),
    "float32_t": (random.uniform, (-3.4e38, 3.4e38)),  # IEEE 754 single-precision
    "float64_t": (random.uniform, (-1.7e308, 1.7e308)),  # IEEE 754 double-precision
    # Commonly treated as 'long double'
    "float128_t": (random.uniform, (-1.1e4932, 1.1e4932)),
    # Assuming a 32-bit double type, non-standard, treated as float
    "double32_t": (random.uniform, (-3.4e38, 3.4e38)),
    # Double precision
    "double64_t": (random.uniform, (-1.7e308, 1.7e308)),
    # Treated as 'long double'
    "double128_t": (random.uniform, (-1.1e4932, 1.1e4932)),
}

random_functions_default = {
    # 32-bit signed
    "int": (random.randint, (-2147483648, 2147483647)),
    # IEEE 754 single-precision
    "float": (random.uniform, (-3.4e38, 3.4e38)),
    # IEEE 754 double-precision
    "double": (random.uniform, (-1.7e308, 1.7e308)),
    # 64-bit signed
    "long": (random.randint, (-9223372036854775808, 9223372036854775807)),
    # Assuming unsigned int, 32-bit
    "unsigned": (random.randint, (0, 4294967295)),
    # 32-bit unsigned
    "unsigned int": (random.randint, (0, 4294967295)),
    # 64-bit unsigned
    "unsigned long": (random.randint, (0, 18446744073709551615)),
    # 64-bit signed
    "long long": (random.randint, (-9223372036854775808, 9223372036854775807)),
    # 64-bit unsigned
    "unsigned long long": (random.randint, (0, 18446744073709551615)),
    # IEEE 754 extended double-precision (commonly 80-bit on x86-64, but up to 128-bit on some systems)
    "long double": (random.uniform, (-1.1e4932, 1.1e4932)),
    # Assuming size_t is 64-bit unsigned
    "size_t": (random.randint, (0, 18446744073709551615)),
    "uint8_t": (random.randint, (0, 255)),
    "uint16_t": (random.randint, (0, 65535)),
    "uint32_t": (random.randint, (0, 4294967295)),
    "uint64_t": (random.randint, (0, 18446744073709551615)),
    "int8_t": (random.randint, (-128, 127)),
    "int16_t": (random.randint, (-32768, 32767)),
    "int32_t": (random.randint, (-2147483648, 2147483647)),
    "int64_t": (random.randint, (-9223372036854775808, 9223372036854775807)),
    "float32_t": (random.uniform, (-3.4e38, 3.4e38)),  # IEEE 754 single-precision
    "float64_t": (random.uniform, (-1.7e308, 1.7e308)),  # IEEE 754 double-precision
    # Commonly treated as 'long double'
    "float128_t": (random.uniform, (-1.1e4932, 1.1e4932)),
    # Assuming a 32-bit double type, non-standard, treated as float
    "double32_t": (random.uniform, (-3.4e38, 3.4e38)),
    # Double precision
    "double64_t": (random.uniform, (-1.7e308, 1.7e308)),
    # Treated as 'long double'
    "double128_t": (random.uniform, (-1.1e4932, 1.1e4932)),
}
