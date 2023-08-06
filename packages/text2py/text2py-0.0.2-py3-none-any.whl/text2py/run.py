import sys
import argparse

import yaml

import text2py


def run():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--template', help='template file')
    arg_parser.add_argument('-i', '--input', help='input file')
    arg_parser.add_argument('-o', '--output', help='output file')
    arg_parser.add_argument('-l', '--log', help='log file')
    args = arg_parser.parse_args()

    template_file = open(args.template)
    template = yaml.load(template_file, yaml.SafeLoader)
    template_file.close()

    parser = text2py.Parser(template)

    input_file = open(args.input, "r")
    output = parser.parse(input_file)
    input_file.close()

    if args.output is not None:
        output_file = open(args.output, "w")
    else:
        output_file = sys.stdout
    output_text = yaml.dump(output)
    output_file.write(output_text)
    output_file.close()

    return 0


if __name__ == "__main__":
    exit(run())
