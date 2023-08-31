import sys

code = input()

original_stdout = sys.stdout

with open('output.txt', 'w') as output_file:
    sys.stdout = output_file

    exec(code)

sys.stdout = original_stdout
