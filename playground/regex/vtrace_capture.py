import re

# Compile a regex pattern to match vtrace function calls with capturing groups for leading whitespace and the number
pattern = re.compile(r"(\s*)vtrace(\d*)\([^)]*\);")

# Test strings
test_strings = [
    "vtrace1(a, b, c);",
    " vtrace2(t1, 3);",
    "   vtrace10(x, y, z);",
    "vtrace(a);",
    "    vtrace(a, b);",
]

# Find all matches in each test string and print the captured leading whitespace and number
for test_string in test_strings:
    match = pattern.findall(test_string)
    print(f"{test_string} -> {match}")
