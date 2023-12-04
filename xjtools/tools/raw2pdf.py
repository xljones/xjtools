"""
    Script:      tools/raw2pdf.py
    Description: Convert a raw string into a pdf
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        04 Dec 2023
"""

import argparse
import datetime
import os
import sys
from base64 import b64decode
from typing import Optional

_VERSION = "1.0.0"

import math


class Raw2Pdf:
    _raw_data: bytes
    _decoded_data: bytes
    _input_filename: str
    _input_filesize: int
    _output_filename: str
    _output_filesize: int

    def __init__(self, input_filename: str, output_filename: Optional[str]) -> None:
        if not os.path.exists(input_filename):
            raise ValueError(f"input file {input_filename} does not exist")

        self._input_filename = input_filename
        self._input_filesize = os.path.getsize(self._input_filename)

        self._output_filename = (
            output_filename
            or f"raw2pdf_{datetime.datetime.now(datetime.UTC).strftime('%YY-%m-%dT%H:%M:%S')}.pdf"
        )

        self._raw_data = self._read_raw_input(input_filename)
        self._convert_raw_to_pdf()
        self._write_output()

    def _read_raw_input(self, input_filename: str) -> bytes:
        with open(input_filename, "r") as file_in_handle:
            raw_data = file_in_handle.read()
            file_in_handle.close()
            return raw_data

    def _convert_raw_to_pdf(self) -> None:
        self._decoded_data = b64decode(self._raw_data, validate=True)
        if self._decoded_data[0:4] != b"%PDF":
            raise ValueError("Missing the PDF file signature")

    @staticmethod
    def _convert_size(size_bytes: int) -> str:
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def _write_output(self) -> None:
        with open(self._output_filename, "wb") as file_out_handle:
            file_out_handle.write(self._decoded_data)
            file_out_handle.close()
            self._output_filesize = os.path.getsize(self._output_filename)

    def print_result(self) -> None:
        input_filesize_str = self._convert_size(self._input_filesize)
        output_filesize_str = self._convert_size(self._output_filesize)
        print(
            f"Decoded {input_filesize_str} from input file '{self._input_filename}',\n"
            f"written to output file '{self._output_filename}' ({output_filesize_str})"
        )


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="tools/raw2pdf.py (v{0})".format(_VERSION))
    p.add_argument(
        "-i", "--input", help="A text file containing the raw data string", required=True
    )
    p.add_argument("-o", "--output", help="The file name to output to e.g. test.pdf")
    args = p.parse_args()

    r2p = Raw2Pdf(args.input, args.output)
    r2p.print_result()
