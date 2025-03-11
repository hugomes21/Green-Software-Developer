import sys

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fibR.py <number_of_terms>")
        sys.exit(1)

    n = int(sys.argv[1])
    print(f"Fibonacci number at position {n} is {fibonacci(n)}")