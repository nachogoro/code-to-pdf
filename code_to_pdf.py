from PyPDF2 import PdfFileMerger

import argparse
import os
import pathlib
import sys
import tempfile
import subprocess

EXTENSIONS=set((
    # Java files
    'java',
    # C files
    'c',
    'h',
    # C++ files
    'cpp',
    'cxx',
    'hpp',
    # Python files
    'py',
    # Bash files
    'sh'
))


def main(argv):
    # TODO: Make configurable
    INCLUDE_LINES = True

    parser = argparse.ArgumentParser(
        description='Convert source code into .pdf file')
    parser.add_argument('input_dir',
                        help='Root directory of the source code')
    parser.add_argument('-o', '--output',
                        default='output.pdf',
                        type=str,
                        help='Output .pdf file')
    parser.add_argument('-l', '--line_numbers',
                        action='store_true',
                        help='Include line numbers')
    parser.add_argument('-f', '--force',
                        action='store_true',
                        help='Overwrite output file')

    args = parser.parse_args()

    if not args.force and os.path.exists(args.output):
        print('%s would be overwritten. Use option \'-f\' if that\'s desired'
              % args.output)
        return

    src_files = list()

    for ext in EXTENSIONS:
        src_files += list(pathlib.Path(args.input_dir)
                        .glob(os.path.join('**', '*.' + ext)))

    with tempfile.TemporaryDirectory(prefix='code2pdf-') as tmp_dir:
        for index, src_file in enumerate(sorted(src_files)):
            # Create the HTML version of each file using 'highlight' To handle
            # files with the same name living in different directories, name
            # the HTML files sequentially
            command = [
                'highlight',
                '-i', src_file,
                '-o', os.path.join(tmp_dir, '%05d.html' % index),
                '--include-style',
                '%s' % ('--line-numbers' if args.line_numbers else '')]
            subprocess.run(command)

        # All .html files are in the temporary directory, now convert to .pdf
        for html_file in (os.path.join(tmp_dir, f) for f in os.listdir(tmp_dir)):
            subprocess.run(('wkhtmltopdf %s %s'
                            % (html_file,
                            html_file[:-4]+'pdf')).split())

        # Concatenate all .pdf files
        pdf_files = [os.path.join(tmp_dir, f)
                    for f in os.listdir(tmp_dir) if f.endswith('pdf')]

        pdf_merger = PdfFileMerger()

        for pdf in pdf_files:
            pdf_merger.append(pdf)

        pdf_merger.write(args.output)
        pdf_merger.close()


if __name__ == '__main__':
    main(sys.argv)
