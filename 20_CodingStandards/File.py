# PEP-8 is the official style guide for Python code. It provides conventions for writing clean and readable Python code. Below are the key recommendations of PEP-8:
#
# ---
#
# ### **1. Indentation**
# - Use **4 spaces per indentation level**.
# - Avoid mixing tabs and spaces.
#
# ```python
# def example_function():
#     print("Hello, World!")
# ```
#
# ---
#
# ### **2. Line Length**
# - Limit lines to **79 characters** for code and **72 characters** for comments/docstrings.
#
# ```python
# # This comment is within 72 characters.
# long_string = "This is an example of a string that is split over multiple lines " \
#               "to adhere to the line length limit."
# ```
#
# ---
#
# ### **3. Blank Lines**
# - Use blank lines to enhance readability:
#   - **2 blank lines** around top-level functions and class definitions.
#   - **1 blank line** between methods inside a class.
#
# ```python
# class MyClass:
#     def method_one(self):
#         pass
#
#     def method_two(self):
#         pass
#
#
# def some_function():
#     pass
# ```
#
# ---
#
# ### **4. Imports**
# - Place imports at the top of the file.
# - Group imports in this order:
#   1. Standard library imports
#   2. Third-party imports
#   3. Local application/library imports
# - Use one import per line.
#
# ```python
# import os
# import sys
#
# from third_party import SomeModule
#
# from my_package import my_module
# ```
#
# ---
#
# ### **5. Whitespace**
# - Avoid extra whitespace:
#   - Immediately inside parentheses, brackets, or braces.
#   - Before a comma, semicolon, or colon.
#   - Before the opening parenthesis in a function call or definition.
#
# ```python
# # Correct
# my_list = [1, 2, 3]
# result = some_function(arg1, arg2)
#
# # Incorrect
# my_list = [ 1, 2, 3 ]
# result = some_function( arg1, arg2 )
# ```
#
# ---
#
# ### **6. Naming Conventions**
# - Variables, functions, and methods: **lower_case_with_underscores**
# - Constants: **UPPER_CASE_WITH_UNDERSCORES**
# - Classes: **CamelCase**
# - Avoid single-character names except for counters or iterators (e.g., `i`, `j`).
#
# ```python
# class MyClass:
#     CONSTANT = 42
#
#     def my_function(self):
#         pass
# ```
#
# ---
#
# ### **7. Comments**
# - Write comments in complete sentences.
# - Update comments if the code changes.
# - Use `#` for single-line comments and `"""` for docstrings.
#
# ```python
# # This is a single-line comment.
#
# def example_function():
#     """This function demonstrates the use of docstrings."""
#     pass
# ```
#
# ---
#
# ### **8. Docstrings**
# - Use triple double quotes (`"""`) for docstrings.
# - Describe the purpose, arguments, return values, and exceptions raised.
#
# ```python
# def add_numbers(a, b):
#     """Add two numbers and return the result.
#
#     Args:
#         a (int): First number.
#         b (int): Second number.
#
#     Returns:
#         int: Sum of the numbers.
#     """
#     return a + b
# ```
#
# ---
#
# ### **9. Avoid Trailing Whitespace**
# - Do not leave trailing whitespace at the end of a line.
#
# ---
#
# ### **10. Use `is` or `is not` for Comparisons to None**
# - Use `is` or `is not` instead of `==` or `!=` to compare to `None`.
#
# ```python
# # Correct
# if my_variable is None:
#     pass
#
# # Incorrect
# if my_variable == None:
#     pass
# ```
#
# ---
#
# ### **11. Boolean Values**
# - Use `if foo` rather than `if foo == True` or `if foo is True`.
#
# ```python
# # Correct
# if is_active:
#     pass
#
# # Incorrect
# if is_active == True:
#     pass
# ```
#
# ---
#
# ### **12. Avoid Star Imports**
# - Do not use `from module import *`. Import explicitly to avoid namespace conflicts.
#
# ---
#
# ### **13. Exception Handling**
# - Use `try`-`except` blocks and be specific about the exceptions you catch.
#
# ```python
# # Correct
# try:
#     result = 10 / 0
# except ZeroDivisionError:
#     print("Cannot divide by zero!")
# ```
#
# ---
#
# #
#
