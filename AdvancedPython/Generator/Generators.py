'''Python yield keyword is used to create a generator function.
The yield keyword can be used only inside a function body.
When a function contains yield expression, it automatically becomes a generator function.
The generator function returns an Iterator known as a generator.
The generator controls the execution of the generator function.
When generator next() is called for the first time, the generator function starts its execution.
When the next() method is called for the generator, it executes the generator function to get the next value. The function is executed from where it has left off and doesn’t execute the complete function code.
The generator internally maintains the current state of the function and its variables, so that the next value is retrieved properly.
Generally, we use for-loop to extract all the values from the generator function and then process them one by one.
The generator function is beneficial when the function returns a huge amount of data. We can use the yield expression to get only a limited set of data, then process it and then get the next set of data.
'''

# A simple generator function
def my_gen():
    n = 1
    print('This is printed first')
    # Generator function contains yield statements
    yield n

    n += 1
    print('This is printed second')
    yield n

    n += 1
    print('This is printed at last')
    yield n

a=my_gen()
print(next(a))
