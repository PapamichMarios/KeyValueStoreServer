import argparse
import json
import random, string

'''
createData -k keyFile.txt -n 1000 -d 3 -l 4 -m 5

-n indicates the number of lines (i.e. separate data) that we would like to generate (e.g. 1000)
-d is the maximum level of nesting (i.e. how many times in a line a value can have a set of key :
values). Zero means no nesting, i.e. there is only one set of key-values per line (in the value of the
high level key)
-m is the maximum number of keys inside each value.
-l is the maximum length of a string value whenever you need to generate a string. For example 4
means that we can generate Strings of up to length 4 (e.g. “ab”, “abcd”, “a”). We should not generate
empty strings (i.e. “” is not correct). Strings can be only letters (upper and lowercase) and numbers. No
symbols.
-k keyFile.txt is a file containing a space-separated list of key names and their data types that we
can potentially use for creating data. For example:
'''


def random_string(length: int) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def construct_inner(current_level: int, max_level: int) -> dict:
    child = {}
    if max_level == current_level:

        children = random.randint(1, args.m)
        for x in range(0, children):
            child[random_string(args.l)] = random_string(args.l)

        return child

    child[random_string(args.l)] = construct_inner(current_level=current_level + 1, max_level=max_level)
    return child


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process arguments for data creation")
    parser.add_argument('-n', type=int, help="number of lines of the generated file", default=1000)
    parser.add_argument('-d', type=int, help="maximum level of nesting", default=5)
    parser.add_argument('-m', type=int, help="maximum number of keys inside each value", default=5)
    parser.add_argument('-l', type=int, help="maximum length of string generated strings", default=5)
    parser.add_argument('-k', type=str, help="file containing a space separated-list of key names and their data types")

    args = parser.parse_args()
    key_values = {}
    for i in range(0, args.n):

        inner = {}
        children = random.randint(1, args.m)
        for j in range(0, children):
            inner[random_string(args.l)] = construct_inner(current_level=0, max_level=args.d)

        key_values['key_' + str(i)] = inner

    with open('file.txt', 'w') as file:
        file.write(json.dumps(key_values))
