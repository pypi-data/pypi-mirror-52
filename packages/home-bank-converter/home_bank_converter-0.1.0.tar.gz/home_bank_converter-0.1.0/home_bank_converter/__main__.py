import argparse
from home_bank_converter.converter import Converter


def main():
    parser = argparse.ArgumentParser(
        description="Convert a CSV export file from your online banking to a HomeBank compatible CSV format.")
    parser.add_argument("filename", help="The CSV file to convert.")
    args = parser.parse_args()

    csv_parser = Converter(filename=args.filename)
    csv_parser.parse()
    csv_parser.convert_and_write()


if __name__ == '__main__':
    main()
