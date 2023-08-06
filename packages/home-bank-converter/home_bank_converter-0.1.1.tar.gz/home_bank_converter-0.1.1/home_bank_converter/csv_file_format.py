import csv
from typing import List

from home_bank_converter.csv_dialects import DialectVB, DialectDKB
from home_bank_converter.home_bank_fields import *


class CsvFileFormat:
    header_pattern: str = None

    def matches(self, first_document_lines: str) -> bool:
        import re
        return re.match(self.header_pattern, str(first_document_lines)) is not None

    @property
    def number_header_lines(self):
        return self.header_pattern.count("\n")

    csv_fields: HomeBankFields = None

    dialect: csv.Dialect = None

    def __init__(self):
        assert self.header_pattern is not None
        assert self.csv_fields is not None
        assert self.dialect is not None


class CsvFileFormatDkbVisa(CsvFileFormat):
    header_pattern = '"Kreditkarte:";"\d+[*]+\d+";\n' \
                     '\n' \
                     '"Von:";"[\d,.]+";\n' \
                     '"Bis:";"[\d,.]+";\n' \
                     '"Saldo:";"[\w,.,\s]+";\n' \
                     '"Datum:";"[\d,.]+";\n' \
                     '\n'

    dialect = DialectDKB()

    csv_fields = DKBVisaFields()


class CsvFileFormatDkbGiro(CsvFileFormat):
    header_pattern = '"Kontonummer:";"\w+\d+ / \w+";\n' \
                     '\n' \
                     '"Von:";"[\w.]+";\n' \
                     '"Bis:";"[\d.]+";\n"' \
                     'Kontostand vom [\d.]+:";"[\d.,]+ \w+";\n' \
                     '\n'

    dialect = DialectDKB()

    csv_fields = DKBGiroFields()


class CsvFileFormatVBGiro(CsvFileFormat):
    header_pattern = '"Vereinigte Volksbank eG"\n' \
                     '\n' \
                     '"Umsatzanzeige"\n' \
                     '\n' \
                     '"BLZ:";"\d+";;"Datum:";"[\d,.]+"\n' \
                     '"Konto:";"\d+";;"Uhrzeit:";"[\d,:]+"\n' \
                     '"Abfrage von:";"[\w,\s]+";;"Kontoinhaber:";"[\w,\s]+"\n' \
                     '\n' \
                     '"Zeitraum:";[\w,\s,\d,.,"]*;"von:";[\d,.,\s,"]*;"bis:";[\d,.,\s"]*\n' \
                     '"Betrag in EUR:"[",;,\w,:\s]+\n' \
                     '"Sortiert nach:";"\w+";"\w+"\n' \
                     '\n'

    csv_fields = VBGiroFields()

    dialect = DialectVB()


class CsvFileFormatRegistry:
    registry: List[CsvFileFormat] = list()

    def register(self, csv_file_format: CsvFileFormat):
        self.registry.append(csv_file_format)

    def find_matching_format(self, header_lines: List[str]) -> CsvFileFormat:
        header_lines_str = ''.join(header_lines)

        for csv_file_format in self.registry:
            if csv_file_format.matches(header_lines_str):
                return csv_file_format

        raise RuntimeError("Unknown header format!")


csv_file_format_registry = CsvFileFormatRegistry()
csv_file_format_registry.register(CsvFileFormatDkbVisa())
csv_file_format_registry.register(CsvFileFormatDkbGiro())
csv_file_format_registry.register(CsvFileFormatVBGiro())
