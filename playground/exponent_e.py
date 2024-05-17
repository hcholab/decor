import math

# Any number can be used here
number = 5000  # This number wouldn't naturally convert to a string with "e" in it

# Manually format the number to scientific notation
formatted_number = "{:.1e}".format(number)

# Now, split the formatted number to extract the exponent
parts = formatted_number.split("e")
exponent = int(parts[1])

# Calculating 10 to the power of the exponent
result = math.pow(10, exponent)

print(f"The original number: {number}")
print(f"Formatted in scientific notation: {formatted_number}")
print(f"The extracted part is 10^{exponent} = {result}")
