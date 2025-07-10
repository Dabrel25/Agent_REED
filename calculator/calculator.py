import math

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Cannot divide by zero"
    return x / y

def sqrt(x):
    if x < 0:
        return "Cannot calculate square root of negative number"
    return math.sqrt(x)

if __name__ == "__main__":
    print(f"add(2, 3) = {add(2, 3)}")
    print(f"subtract(5, 2) = {subtract(5, 2)}")
    print(f"multiply(4, 3) = {multiply(4, 3)}")
    print(f"divide(10, 2) = {divide(10, 2)}")
    print(f"sqrt(9) = {sqrt(9)}")
    print(f"sqrt(-9) = {sqrt(-9)}")