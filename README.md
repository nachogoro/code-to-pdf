# Source code to pdf

## Overview
Simple Python script which converts the source code files under a given
directory into a single .pdf file. The resulting .pdf file is text-based and
syntax-highlighted.

## Requirements
The script has been developed for Linux, and makes use of the following tools:
* [wkhtmltopdf](https://wkhtmltopdf.org/)
* [highlight](http://www.andre-simon.de/doku/highlight/en/highlight.php)

They must be installed and be part of the `PATH` for the script to work.

## Installation
Simply install the previous tools using your distro's package manager (`apt`, `yum`, `pacman`...) and execute the following command to install install the [PyPDF2](https://pypi.org/project/PyPDF2/) Python module:

```bash
pip install -r requirements.txt
```

## Usage
```
$ python3 code_to_pdf.py --help
usage: code_to_pdf.py [-h] [-o OUTPUT] [-l] [-f] input_dir

Convert source code into .pdf file

positional arguments:
  input_dir             Root directory of the source code

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output .pdf file
  -l, --line_numbers    Include line numbers
  -f, --force           Overwrite output file
```
