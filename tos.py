with open('test.txt') as f:
    content = f.read()

instructions = content.split(';')

for instruction in instructions:
    if instruction[0] = '(':