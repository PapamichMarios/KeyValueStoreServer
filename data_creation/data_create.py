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


def random_float() -> tuple:
    return random.uniform(0, 100)


def random_int() -> tuple:
    return random.randint(0, 100)


def random_string(length: int) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def random_variable(file: list) -> tuple:
    index = random.randint(0, len(file) - 1)
    return file[index][0], file[index][1]


def return_value(type: string, current_level: int, max_level: int, key_values_file: list, args: object):
    if type == 'int':
        return random_int()
    elif type == 'float':
        return random_float()
    elif type == 'set':
        return construct_inner(current_level=current_level, max_level=max_level, key_values_file=key_values_file,
                               args=args)
    else:
        return random_string(args.l)


def construct_inner(current_level: int, max_level: int, key_values_file: list, args: object) -> dict:
    child = {}
    if max_level == current_level:

        children = random.randint(1, args.m)
        for x in range(0, children):
            value = ''
            while value != 'set':
                (key, value) = random_variable(file=key_values_file)
            child[key] = return_value(type=value, current_level=0, max_level=args.d, key_values_file=key_values_file,
                                      args=args)

        return child

    (key, value) = random_variable(file=key_values_file)
    child[key] = return_value(type=value, current_level=0, max_level=args.d, key_values_file=key_values_file, args=args)
    return child


def main():
    # arg parsing
    parser = argparse.ArgumentParser(description="Process arguments for data creation")
    parser.add_argument('-n', type=int, help="number of lines of the generated file", default=1000)
    parser.add_argument('-d', type=int, help="maximum level of nesting", default=5)
    parser.add_argument('-m', type=int, help="maximum number of keys inside each value", default=5)
    parser.add_argument('-l', type=int, help="maximum length of string generated strings", default=5)
    parser.add_argument('-k', type=str, help="file containing a space separated-list of key names and their data types")

    args = parser.parse_args()

    # read key file
    key_values_file = []
    with open(args.k, 'r') as file:
        key_values_file = [[str(x) for x in line.split()] for line in file]

    key_values = {}
    for i in range(0, args.n):

        inner = {}
        children = random.randint(1, args.m)
        for j in range(0, children):
            (key, value) = random_variable(file=key_values_file)
            inner[key] = return_value(type=value, current_level=0, max_level=args.d, key_values_file=key_values_file,
                                      args=args)

        key_values['key_' + str(i)] = inner

    with open('file.txt', 'w') as file:
        for key, value in key_values.items():
            row = "\"" + key + "\" : " + json.dumps(value) + "\n"
            file.write(row.replace(',', ' ;'))


if __name__ == "__main__":
    main()
