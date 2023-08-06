# home_bank_converter

Converter for various online banking transaction files to be able to import them to HomeBank (http://homebank.free.fr). 

HomeBank is a great tool to gain insight into your expenses. Most online banking apps provide a CSV file export for your transactions. As each online banking app uses a different file format, HomeBank might not be able to import them.

This library is inspired by https://github.com/hamvocke/dkb2homebank 

## Features

 - Automatically detect the CSV file format
 - Supported online banking apps:
   - Volksbank
   - Deutsche Kreditbank (DKB)
   

## Design principles

 - Modular design to easily extend the supported CSV file formats
   
## How to use

home_bank_converter is a python library. 

### Installation

Download the repo and install it

      git clone ...
      pip install home_bank_converter

### Usage

      python -m home_bank_converter [filename] 
 
 a file with a *_HomeBank* suffix will be created alongside your original transaction file.
 
 ## Contribution
 
 ### How to add support for new transaction formats
 
 1) Create an anonymized version of your transaction file. 
 2) Create an issue (tag it with 'new transaction file format') and attach your file.
 3) Extend csv_file_format.py (you don't need to touch any existing code ...)
     - add a new class which is derived from CsvFileFormat
     - add an instance to the registry at the bottom of the file
