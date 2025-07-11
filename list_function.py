# Example of map, filter, and lambda in Python

# 1. map() function
# map() applies a function to every item in a list (or any iterable)
numbers = [1, 2, 3, 4, 5]

def double_function(value): 
    return value * 2; 

# Let's double each number in the list using map and a lambda function
# Using map() with lambda to double each number
double_map = list(map(double_function, numbers)); 

print(f" Type of map {type (double_map)}")

# print(f"value of map {next(double_map)}")





doubled_map = list(map(lambda x: x * 2, numbers))
print("Doubled numbers using map:", doubled_map)  # Output: [2, 4, 6, 8, 10]

# Using a normal for loop to double each number
doubled_loop = []
for num in numbers:
    doubled_loop.append(num * 2)
print("Doubled numbers using for loop:", doubled_loop)  # Output: [2, 4, 6, 8, 10]

# Difference:
# - map() with lambda is more concise and functional, good for simple operations.
# - for loop is more explicit and flexible, easier to read for beginners or for more complex logic.

# 2. filter() function
# filter() selects items from a list (or any iterable) based on a condition
# Let's keep only the even numbers from the list
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens)  # Output: [2, 4]

# 3. lambda function vs normal function

# Using a lambda function (anonymous, one-liner)
add_ten_lambda = lambda x: x + 10
print("Using lambda: 5 + 10 =", add_ten_lambda(5))  # Output: 15

# Using a normal function (named, can have multiple lines)
def add_ten_function(x):
    return x + 10

print("Using normal function: 5 + 10 =", add_ten_function(5))  # Output: 15

# Difference:
# - Lambda functions are anonymous, written in a single line, and best for simple operations.
# - Normal functions have a name, can have multiple lines, and are better for complex logic or reuse.
# 4. What does "anonymous" mean in lambda?

# "Anonymous" means the function has no name.
# Lambda functions are called anonymous functions because they are defined without a name.
# Example:
square = lambda x: x * x  # This function has no name, just assigned to 'square'
print("Square of 3 using lambda:", square(3))  # Output: 9

# In contrast, a normal function has a name:
def square_function(x):
    return x * x
print("Square of 3 using normal function:", square_function(3))  # Output: 9

# 5. When to use lambda functions?
# - When you need a simple function for a short period of time.
# - When passing a function as an argument (e.g., to map, filter, sorted).
# - When you don't want to formally define a function with def.

# Example: Sorting a list of tuples by the second item
pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
print("Pairs sorted by second item:", sorted_pairs)  # Output: [(1, 'one'), (3, 'three'), (2, 'two')]



