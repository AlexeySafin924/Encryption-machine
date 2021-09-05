import argparse
import sys
import string
from collections import defaultdict


low_from = dict()
low_to = dict()
big_from = dict()
big_to = dict()
for i in range(0, len(string.ascii_lowercase)):
    low_from[i] = string.ascii_lowercase[i]
    low_to[string.ascii_lowercase[i]] = i
    big_from[i] = string.ascii_uppercase[i]
    big_to[string.ascii_uppercase[i]] = i


def is_low(symbol):
    return symbol in low_to


def is_big(symbol):
    return symbol in big_to


def change(shift, i):
    if is_low(i):
        to = low_to
        frm = low_from
    elif is_big(i):
        to = big_to
        frm = big_from
    else:
        return i
    return frm[(to[i] + shift + len(frm)) % len(frm)]


def caesar(input_string, shift, sign):
    result = ""
    shift = int(shift)
    for i in input_string:
        result += change(shift * sign, i)
    return result


def vigenere(input_string, word, code):  # code = 1 means encrypt, -1 - decrypt
    result = ""
    j = 0
    for i in input_string:
        result += change(big_to[word[j]] * code, i)
        if is_low(i) or is_big(i):
            j = (j + 1) % (len(word))
    return result


def make_hist(input_string):
    hist = defaultdict(float)
    total_numbers = 0
    for i in input_string:
        if is_big(i) or is_low(i):
            hist[i.upper()] += 1
            total_numbers += 1
    for i in big_to:
        hist[i] /= total_numbers
    return hist


def train_caesar(input_string):
    return make_hist(input_string)


def parse(model):
    t = list(map(str, model[1:-1].split(',')))
    d = dict()
    for i in t:
        k = list(map(str, i.split()))
        d[k[0][1]] = float(k[-1])
    return d


def hack_caesar(input_string, model):
    norm = parse(model)
    hist = make_hist(input_string)
    min_dev = float('inf')
    shift = None
    for y in range(len(big_from)):
        deviation = 0
        for i in hist:
            deviation += (hist[big_from[(big_to[i] + y) % len(big_from)]] - norm[i]) ** 2
        if deviation < min_dev:
            min_dev = deviation
            shift = y
    return caesar(input_string, shift, -1)


def read(args, str):
    if str == "text":
        if args.text_file:
            input_str = args.text_file.read()
        else:
            input_str = sys.stdin.read()
        return input_str
    if args.input_file:
        input_str = args.input_file.read()
    else:
        input_str = sys.stdin.read()
    return input_str


def write(args, result):
    if args.output_file:
        args.output_file.write(result)
    else:
        sys.stdout.write(result)


def encrypt(args):
    input_str = read(args, "input")
    if args.cipher == 'caesar':
        result = caesar(input_str, args.key, 1)
    else:
        result = vigenere(input_str, args.key, 1)
    write(args, result)


def decrypt(args):
    input_str = read(args, "input")
    if args.cipher == 'caesar':
        result = caesar(input_str, args.key, -1)
    else:
        result = vigenere(input_str, args.key, -1)
    write(args, result)


def train(args):
    input_str = read(args, "text")
    result = train_caesar(input_str)
    args.model_file.write(str(dict(result)))


def hack(args):
    input_str = read(args, "input")
    result = hack_caesar(input_str, args.model_file.read())
    write(args, result)


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers()
encode_parser = subparsers.add_parser('encode', help='Help for encode')
encode_parser.set_defaults(solve=encrypt)
encode_parser.add_argument('--cipher', choices=['caesar', 'vigenere'], help='Type of cipher', required=True)
encode_parser.add_argument('--key', help='Cipher key', required=True)
encode_parser.add_argument('--input-file', type=argparse.FileType('r'), help='File for input')
encode_parser.add_argument('--output-file', type=argparse.FileType('w'), help='File for output')

decode_parser = subparsers.add_parser('decode', help='Help for decode')
decode_parser.set_defaults(solve=decrypt)
decode_parser.add_argument('--cipher', choices=['caesar', 'vigenere'], help='Type of cipher', required=True)
decode_parser.add_argument('--key', help='Cipher key', required=True)
decode_parser.add_argument('--input-file', type=argparse.FileType('r'), help='File for input')
decode_parser.add_argument('--output-file', type=argparse.FileType('w'), help='File for output')

train_parser = subparsers.add_parser('train', help='Help for train')
train_parser.set_defaults(solve=train)
train_parser.add_argument('--text-file', type=argparse.FileType('r'), help='File for input')
train_parser.add_argument('--model-file', type=argparse.FileType('w'), help='File for model', required=True)

hack_parser = subparsers.add_parser('hack', help='Help for hack')
hack_parser.set_defaults(solve=hack)
hack_parser.add_argument('--input-file', type=argparse.FileType('r'), help='File for input')
hack_parser.add_argument('--output-file', type=argparse.FileType('w'), help='File for output')
hack_parser.add_argument('--model-file', type=argparse.FileType('r'), help='File for model', required=True)


arguments = parser.parse_args()
arguments.solve(arguments)
