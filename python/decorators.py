### Decorator - modifying behavior of function - takes function as input, returns modified form of function as output
### "Functional" programming

# Decorator
# Takes f - function as input, returns modified function
def announce(f):
    def wrapper():
        print("About to run the function ...")
        f()
        print("Done with the function.")
    return wrapper

### Use announce decorator
@announce
def hello():
    print("Hello World")

hello()