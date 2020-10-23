import re


def prac(filename):
    with open(filename) as f:
        re.findall('"([^"]*)"', f)


if __name__ == '__main__':
    lc = [line.upper().split('"') for line in open('yaml.txt') ]
    [print(x[1].replace(" ", "_").join(',')) for x in lc]

    s = [x[1].replace(" ", "_") for x in lc]
    v = ','.join(s)

    print(v)
