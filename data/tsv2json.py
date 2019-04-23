
from argparse import ArgumentParser
from json import dumps
from sys import stdout


MODEL_DEFS = {
    'fpiweb.productcategory': [
        ('prod_cat_name', str),
        ('prod_cat_descr', str)
    ]
}






def main(args):

    records = []
    with open(args.IN_FILE, 'r') as in_file:
        for i, line in enumerate(in_file):
            line = line.strip()
            if not line:
                continue

            pk, *field_values = line.split('\t')



            data = {
                'model': args.model,
                'pk': int(pk),
                'fields': [],
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