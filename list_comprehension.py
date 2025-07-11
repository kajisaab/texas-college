# Function without using list comprehension
def square_numbers_loop(numbers):
    """
    Squares each number in the input list using a for loop.
    """
    result = []
    for num in numbers:
        result.append(num ** 2)
    return result

# List comprehensions in Python provide a concise way to create lists by applying an expression to each item in an iterable (like a list or range), optionally filtering items with a condition.

# Example:

# Pros
# Concise & Readable: Shorter and often clearer than equivalent for-loops.
# Performance: Usually faster than using a for-loop to build a list.
# Functional Style: Encourages thinking in terms of mapping and filtering.
# Cons
# Readability: Can become hard to read if overused or made too complex (especially with nested comprehensions).
# Memory Usage: Always creates a new list in memory, which can be inefficient for very large datasets (consider using generator expressions for large data).
# Not Always Clear: For beginners, the syntax can be confusing at first.
# Summary:
# Use list comprehensions for simple, clear transformations. Avoid them for complex logic or when working with very large data where memory is a concern.

# Function using list comprehension
def square_numbers_comprehension(numbers):
    """
    Squares each number in the input list using list comprehension.
    """
    return [num ** 2 for num in numbers]

# Example usage:
if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5]
    print("Without list comprehension:", square_numbers_loop(nums))
    print("With list comprehension:", square_numbers_comprehension(nums))