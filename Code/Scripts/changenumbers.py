import math

with open('outtree2', 'r') as file:
    text = file.read()

for i in range(len(text)):
    if text[i] is ':':
        input = text[i+1:i+8]

        if text[i+8] is ',' or text[i-1] is ')':
            number = str(0.01)
        else:
            number = float(input)
            number = math.sqrt(number)
            number = str(number)

        text = text[:i+1] + number + text[i+8:]

with open('outtree2-new', 'w') as output:
    output.write(text)


