from home_bank_converter.csv_file_format import csv_file_format_registry

from datetime import datetime
import csv
from typing import List

import locale
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


def convert_date(date_string):
    date = datetime.strptime(date_string, "%d.%m.%Y")
    return date.strftime('%d-%m-%Y')


class Converter(object):
    max_header_lines = 13

    def __init__(self, filename: str):
        self.filename = filename

    def parse(self):
        with open(self.filename, 'r', encoding='iso-8859-1') as csvfile:
            csv_lines = csvfile.readlines()

            potential_header_lines = csv_lines[:self.max_header_lines]
            self.csv_file_format = csv_file_format_registry.find_matching_format(potential_header_lines)

            self.transaction_header_line = csv_lines[self.csv_file_format.number_header_lines]
            self.transaction_lines = csv_lines[(self.csv_file_format.number_header_lines + 1):]  # skip header row

    @property
    def output_filename(self):
        from os.path import splitext
        return "{}_HomeBank{}".format(*splitext(self.filename))

    homebank_field_names = ["date",
                            "paymode",
                            "info",
                            "payee",
                            "memo",
                            "amount",
                            "category",
                            "tags"]

    def convert_and_write(self):
        # dialect = csv.Sniffer().sniff(self.csv_file.read(1024))
        fieldnames = self.transaction_header_line.replace('"', '').replace("\n", "").split(';')

        reader = csv.DictReader(self.transaction_lines, dialect=self.csv_file_format.dialect, fieldnames=fieldnames)

        with open(self.output_filename, 'w') as outfile:
            fields = self.csv_file_format.csv_fields

            writer = csv.DictWriter(outfile, dialect='dkb', fieldnames=self.homebank_field_names)

            for row in reader:
                row: List[str]

                def soll_haben_sign(var):
                    return {"S": -1.0, "H": 1.0}[var]

                sign = soll_haben_sign(row[fields.SIGN]) if fields.SIGN else 1.0

                amount_str = row[fields.AMOUNT].replace(".", "").replace(",", ".")  # 1.000,00 -> 1000.00
                amount = float(amount_str)

                amount *= sign

                writer.writerow(
                    {
                        'date': convert_date(row[fields.DATE]),
                        'paymode': 8,
                        'info': None,
                        'payee': row[fields.PAYEE].replace("\n", " ") if fields.PAYEE else None,
                        'memo': row[fields.MEMO].replace("\n", " "),
                        'amount': amount,
                        'category': None,
                        'tags': None
                    })
