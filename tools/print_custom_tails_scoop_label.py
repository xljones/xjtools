"""
    Script:      tools/print_custom_tails_label.py
    Description: ...
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        17 Sept 2024
"""

import argparse
import json
import random
import string
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import requests

_VERSION = "2.0.0"


class Locale(Enum):
    en_gb = "en_GB"
    de_de = "de_DE"


@dataclass
class ScoopLabel:
    dog_name: str
    barcode: str | None = None


PRINTER_ID = 296
EXTERNAL_ID = "adele-scoop-labels"  # "gb_marketing"
TEMPLATE_NAME = "scoop_label"
LOCALE = Locale.en_gb

SCOOP_LABEL_NAMES = [
    "B1",
    "B2",
    "B3",
    "B4",
    "B5",
    "B6",
    "B7",
    "B8",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "C6",
    "C7",
    "C8",
    "D1",
    "D2",
    "D3",
    "D4",
    "D5",
    "D6",
    "D7",
    "D8",
    "E1",
    "E2",
    "E3",
    "E6",
    "E7",
    "E8",
]
REPEAT = 28


class ScoopLabelService:
    def _generate_random_barcode(self) -> str:
        return "".join(random.choice(string.digits) for _ in range(3))

    def generate_labels(self, execute: bool = False) -> None:
        count = 0
        total_count = len(SCOOP_LABEL_NAMES) * REPEAT

        print(f"=== SCOOP_LABELS\nGenerating {total_count} labels\n")
        for batch in range(REPEAT):
            if execute:
                _ = input(
                    f"🚨 Hit return to print batch {batch} "
                    f"on Printer ID {PRINTER_ID} ..."
                )
            for scoop_label_name in SCOOP_LABEL_NAMES:
                count += 1

                data = {
                    "name": scoop_label_name,
                    "barcode": self._generate_random_barcode(),
                }

                json_str = (
                    json.dumps(
                        data,
                        ensure_ascii=False,
                    )
                    .encode("utf-8")
                    .decode()
                )
                print(f"=== SCOOP LABEL {count} of {total_count}")
                print(json_str)

                if execute:
                    self._send_to_printer(
                        printer_id=PRINTER_ID,
                        data_json_str=json_str,
                        template_name=TEMPLATE_NAME,
                        external_id=EXTERNAL_ID,
                        locale=LOCALE,
                    )

    @staticmethod
    def _send_to_printer(
        printer_id: int,
        data_json_str: str,
        template_name: str,
        locale: Locale,
        external_id: str,
    ) -> None:
        """Use the https://github.com/tailsdotcom/printables-service/blob/main/service/views/printers.py#L240
        endpoint (printables.backyard.tails.com/printers/int:printer_id/render-print) to POST a print request.

        The POST payload will look something like as follows

        {
            "data": "PASTE JSON DUMPED DATA STRING",
            "template_name": "bag_label",
            "locale": "de_DE",
            "external_id": "DE_marketing",
        }
        """

        ENDPOINT = "https://printables.backyard.tails.com/printers/{printer_id}/render-print"
        response = requests.post(
            url=ENDPOINT.format(printer_id=printer_id),
            json={
                "data": data_json_str,
                "template_name": template_name,
                "locale": locale.value,
                "external_id": external_id,
            },
        )
        print(
            f"RESPONSE={response}\n",
            f"CONTENT={response.content}\n",
        )


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description=f"tools/print_custom_tails_scoop_label.py (v{_VERSION})",
    )
    p.add_argument(
        "-e",
        "--execute",
        help=f"send the request to a real printer (id={PRINTER_ID})",
        action="store_true",
    )
    args = p.parse_args()

    sls = ScoopLabelService()
    sls.generate_labels(
        execute=args.execute,
    )
