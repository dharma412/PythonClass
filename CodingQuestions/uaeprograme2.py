a = list(encoded[::-1])
a = input()
p = 0
b = []
while p < len(a):
    if int(a[p] + a[p + 1]) == 32 or int(a[p] + a[p + 1]) >= 65:
        b.append(chr(int(a[p] + a[p + 1])))
        p = p + 2
    else:
        b.append(chr(int(a[p] + a[p + 1] + a[p + 2])))
        p = p + 3

print(b)


def arrange(sentence):
    import re

    rgx = re.compile(r'^[A-Z][a-z ]*\.$')
    sentence = str(sentence)
    assert re.match(rgx, sentence)

    words = [
        word.lower()[0:len(word) - 1] if word[-1] == '.' else word.lower()
        for word in re.sub(r'[ ]+', ' ', sentence).split(' ')
    ]

    words.sort(key=len)
    words[0] = f'{words[0][0].upper()}{words[0][1:]}'

    words[-1] = f'{words[-1]}.'
    output = ' '.join(words)
    assert re.match(rgx, output)

    return output


print(arrange("Cats and hats."))

a = "20"

b = Cint(a)

import re

inputstring = "Cats and hats."
rgx = '^[A-Z][a-z ]*\.$'
inputstring = str(inputstring)
match = re.match(rgx, inputstring)
if match:
    ##print(match)
    words = []
    for word in re.sub(r'[ ]+', ' ', inputstring).split(' '):
        if word[-1] == '.':
            word.lower()[0:len(word) - 1]
            words.append(word)
        else:
            word.lower()
            words.append(word)
    # words = [word.lower()[0:len(word)-1] if word[-1] == '.' else word.lower()
    # for word in re.sub(r'[ ]+', ' ', inputstring).split(' ')]
words.sort(key=len)
print(words)
words[0] = words[0].capitalize()
words[-1] = words[-1]
output = ' '.join(words)
# assert re.match(rgx, output)
print(output)

