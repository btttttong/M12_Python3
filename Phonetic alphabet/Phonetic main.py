import csv

def load_phonetic_alphabet(filename):
    phonetic_dict = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            phonetic_dict[row['letter'].upper()] = row['code']
    return phonetic_dict

phonetic_dict = load_phonetic_alphabet('phonetic_alphabet.csv')


def read_input(filename):
    with open(filename, 'r') as file:
        input_file = file.read()
    return input_file


def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)


def encode(text):
    words = []

    for char in text.upper():
        if char.isalpha() and char in phonetic_dict:
            words.append(phonetic_dict[char])
        else:
            words.append(char)

    return ' '.join(words)


def decode(ipa_text):
    reverse_phonetic_dict = {v: k for k, v in phonetic_dict.items()}
    words = ipa_text.split()
    characters = []

    for word in words:
        if word in reverse_phonetic_dict:
            characters.append(reverse_phonetic_dict[word])
        else:
            characters.append(word)

    return ''.join(characters)


input_file = read_input('input.txt')
write_to_file('output.txt', encode(input_file))

input_ipa = read_input('output.txt')
write_to_file('output2.txt', decode(input_ipa))
