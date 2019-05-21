
from argparse import ArgumentParser
from json import dumps
from sys import stderr


MODEL_DEFS = {
    'fpiweb.productcategory': [
        ('prod_cat_name', str),
        ('prod_cat_descr', str)
    ],
    'fpiweb.product': [
        ('prod_name', str),
        ('prod_cat', int),
    ],
}


def main(args):

    field_defs = MODEL_DEFS.get(args.model)

    records = []
    with open(args.IN_FILE, 'r') as in_file:
        for i, line in enumerate(in_file):
            line = line.strip()
            if not line:
                continue

            pk, *field_values = line.split('\t')

            if len(field_defs) != len(field_values):
                print(f"Wrong number of fields in line {i}", file=stderr)
                continue

            mappings = zip(field_values, field_defs)
            mappings = [(fv, fd[1], fd[0]) for fv, fd in mappings]

            fields = {}
            for value, converter, dest in mappings:
                fields[dest] = converter(value)

            data = {
                'model': args.model,
                'pk': int(pk),
                'fields': fields,
            }

            records.append(data)

    print(dumps(records))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        'IN_FILE',
        help="Input file to read")
    parser.add_argument(
        'model',
        help="Model class")
    main(parser.parse_args())