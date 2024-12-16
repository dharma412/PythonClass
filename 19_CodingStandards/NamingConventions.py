# Python's naming conventions are guided by **PEP-8**, which ensures consistency and clarity in your code. Below are the standard naming conventions for Python:
#
# ---
#
# ### **1. Variables**
# - Use **snake_case** for variable names.
# - Start with a lowercase letter and separate words with underscores.
# - Use meaningful and descriptive names.
#
# ```python
# # Example
# user_name = "John"
# total_price = 19.99
# ```
#
# ---
#
# ### **2. Functions**
# - Use **snake_case** for function names.
# - The name should describe what the function does.
#
# ```python
# # Example
# def calculate_total(price, tax):
#     return price + tax
# ```
#
# ---
#
# ### **3. Constants**
# - Use **UPPER_CASE_WITH_UNDERSCORES** for constants.
# - Place constants at the top of the module.
#
# ```python
# # Example
# PI = 3.14159
# MAX_CONNECTIONS = 100
# ```
#
# ---
#
# ### **4. Classes**
# - Use **CamelCase** (PascalCase) for class names.
# - Start with a capital letter and capitalize each word.
#
# ```python
# # Example
# class UserAccount:
#     pass
# ```
#
# ---
#
# ### **5. Modules and Packages**
# - Use **snake_case** for module names (file names).
# - Use **short, lowercase names** for packages.
#
# ```python
# # File: my_module.py
# # Package: mypackage
# ```
#
# ---
#
# ### **6. Method Names**
# - Use **snake_case** for method names.
# - The naming convention is similar to functions.
#
# ```python
# class User:
#     def get_full_name(self):
#         pass
# ```
#
# ---
#
# ### **7. Instance and Class Variables**
# - Use **snake_case** for instance and class variables.
#
# ```python
# class User:
#     first_name = "John"  # Class variable
#
#     def __init__(self, last_name):
#         self.last_name = last_name  # Instance variable
# ```
#
# ---
#
# ### **8. Private Variables and Methods**
# - Prefix the name with a single underscore `_` to indicate a variable or method is intended for internal use.
# - Prefix with double underscores `__` for name mangling (avoiding name collisions in subclasses).
#
# ```python
# class Example:
#     _internal_variable = 42  # Private variable
#     __mangled_variable = 99  # Name-mangled variable
#
#     def _private_method(self):
#         pass
# ```
#
# ---
#
# ### **9. Global Variables**
# - Use **lower_case_with_underscores** for global variables.
# - Avoid using global variables unless necessary.
#
# ```python
# global_variable = "Accessible globally"
# ```
#
# ---
#
# ### **10. Arguments**
# - Use **snake_case** for argument names.
# - Use descriptive names that convey the purpose of the argument.
#
# ```python
# def send_email(to_address, subject, body):
#     pass
# ```
#
# ---
#
# ### **11. Naming Special Methods**
# - Special methods (or "magic methods") use **double underscores** before and after the name.
# - Examples: `__init__`, `__str__`, `__repr__`.
#
# ```python
# class Example:
#     def __init__(self, value):
#         self.value = value
#
#     def __str__(self):
#         return f"Value: {self.value}"
# ```
#
# ---
#
# ### **12. Acronyms in Names**
# - For acronyms, choose one style and be consistent:
#   - **All caps** if the acronym is at the start of the name: `HTTPServer`
#   - **Lowercase** if it appears in the middle: `http_server`
#
# ```python
# class HTTPServer:
#     pass
#
# def parse_http_response():
#     pass
# ```
#
# ---
#
# ### **13. Exceptions**
# - Use **CamelCase** and end with `Error` for exception class names.
#
# ```python
# class CustomError(Exception):
#     pass
# ```
#
# ---
#
# ### **14. Avoid Ambiguous Names**
# - Avoid using `l` (lowercase L), `O` (uppercase O), or `I` (uppercase I) as single-character variable names because they can be easily confused with numbers.
#
# ---
#
# ### **15. Temporary or Loop Variables**
# - Use single characters like `i`, `j`, `k` for simple loop counters.
# - Use descriptive names for more complex loops.
#
# ```python
# # Simple loop
# for i in range(10):
#     print(i)
#
# # Complex loop
# for user in user_list:
#     print(user.name)
# ```
#
# ---
#
# ### Summary Table of Naming Conventions
#
# | Type                | Convention               | Example                   |
# |---------------------|--------------------------|---------------------------|
# | Variable            | snake_case              | `user_name`               |
# | Function            | snake_case              | `get_user_info()`         |
# | Constant            | UPPER_CASE              | `MAX_RETRIES`             |
# | Class               | CamelCase               | `UserProfile`             |
# | Method              | snake_case              | `set_password()`          |
# | Private Variable    | _single_leading_underscore | `_private_var`           |
# | Mangled Variable    | __double_leading_underscore | `__mangled_var`      |
# | Exception Class     | CamelCase, end with `Error` | `ValidationError`   |
#
# By following these conventions, your code will be more readable, maintainable, and aligned with Python's best practices.