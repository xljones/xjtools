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


class BagSize(Enum):
    small = "small"
    medium = "medium"
    large = "large"
    xlarge = "xlarge"


@dataclass
class BagLabel:
    dog_name: str
    size: BagSize
    weight: int
    scoop_setting: str = "1-E"
    scoop_count: int = 10
    date: str = datetime.now().strftime("%Y-%m-%d")
    working_dog: bool = False
    barcode: str | None = None


PRINTER_ID = 672
LOCALE = Locale.en_gb
EXTERNAL_ID = "mdcw-testing"  # "gb_marketing"
TEMPLATE_NAME = "bag_label"

BAG_LABELS: list[BagLabel] = [
    # Small
    BagLabel(dog_name="S1", size=BagSize.small, weight=330, barcode="94033423529129905"),
    BagLabel(
        dog_name="S2", size=BagSize.small, weight=3000, barcode="86536386636289686"
    ),
    BagLabel(dog_name="S3", size=BagSize.small, weight=1000, barcode="26254985132455490"),
    BagLabel(dog_name="S4", size=BagSize.small, weight=1300, barcode="50553610702541825"),
    BagLabel(dog_name="S6", size=BagSize.small, weight=3200, barcode="32829864735805169"),
    BagLabel(dog_name="S5", size=BagSize.small, weight=2800, barcode="15141789047622718"),
    # # Medium
    # BagLabel(dog_name="M1", size=BagSize.medium, weight=5000, barcode="94113813139676424"),
    # BagLabel(dog_name="M2", size=BagSize.medium, weight=3000, barcode="26203416556651751"),
    # BagLabel(dog_name="M3", size=BagSize.medium, weight=1800, barcode="01394995683597540"),
    # BagLabel(
    #     dog_name="M4", size=BagSize.medium, weight=5200, barcode="08073722474147516"
    # ),
    # BagLabel(
    #     dog_name="M6", size=BagSize.medium, weight=5100, barcode="75546903167324262"
    # ),
    # BagLabel(dog_name="M7", size=BagSize.medium, weight=5000, barcode="49849200534290748"),
    # BagLabel(dog_name="M5", size=BagSize.medium, weight=4350, barcode="15448728842926606"),
    # # Large
    # BagLabel(
    #     dog_name="L1", size=BagSize.large, weight=4500, barcode="20404462822907787"
    # ),
    # BagLabel(dog_name="L2", size=BagSize.large, weight=8000, barcode="83279765104733553"),
    # BagLabel(
    #     dog_name="L3", size=BagSize.large, weight=6500, barcode="38191923849359106"
    # ),
    # BagLabel(
    #     dog_name="L4", size=BagSize.large, weight=8000, barcode="26159654678902564"
    # ),
    # BagLabel(dog_name="L6", size=BagSize.large, weight=6450, barcode="44250801294981151"),
    # BagLabel(
    #     dog_name="L5", size=BagSize.large, weight=7300, barcode="87759524032086891"
    # ),
    # Extra Large
    # BagLabel(
    #     dog_name="XL1", size=BagSize.xlarge, weight=7000, barcode="03594946419021667"
    # ),
    BagLabel(
        dog_name="XL2", size=BagSize.xlarge, weight=11500, barcode="45409938656216582"
    ),
    # BagLabel(dog_name="XL3", size=BagSize.xlarge, weight=9000, barcode="37473912511064270"),
    # BagLabel(dog_name="XL4", size=BagSize.xlarge, weight=11500, barcode="05027428312488885"),
    # BagLabel(dog_name="XL6", size=BagSize.xlarge, weight=10800, barcode="46475080202752031"),
    # BagLabel(dog_name="XL5", size=BagSize.xlarge, weight=10300, barcode="11369496475359253"),
]


class BagLabelService:
    def _get_translated_claims(self, locale: Locale) -> dict:
        match locale:
            case Locale.en_gb:
                return {
                    "Healthy skin & coat": "Healthy skin & coat",
                    "Mobility & joint care": "Mobility & joint care",
                    "Tailor-made kibble design": "Tailor-made kibble design",
                }
            case Locale.de_de:
                return {
                    "Healthy skin & coat": "Gesunde Haut & gesundes Fell",
                    "Mobility & joint care": "Mobilität & Gelenkpflege",
                    "Tailor-made kibble design": "Massgeschneiderte Trockenfuttergrösse",
                }
            case _:
                raise Exception(f"locale {locale} is not supported")

    def _generate_random_barcode(self) -> str:
        return "".join(random.choice(string.digits) for _ in range(17))

    def generate_labels(self, execute: bool = False) -> None:
        count = 0
        total_count = len(BAG_LABELS)

        print(f"=== BAG_LABELS\nGenerating {total_count} labels")

        for bag_label in BAG_LABELS:
            print(f"\n=== {bag_label} ===")
            count += 1

            data = {
                "bag": bag_label.size.value,
                "name": bag_label.dog_name,
                "label_dt": bag_label.date,
                "label_barcode": bag_label.barcode or self._generate_random_barcode(),
                "working_dog": bag_label.working_dog,
                "weight": bag_label.weight,
                "gender": "female",
                "scoop_setting": bag_label.scoop_setting,
                "scoop_count": bag_label.scoop_count,
                "customer_id": 5998234,
                "pet_id": 5724196,
                "language": LOCALE.value,
                "claims": [
                    "Healthy digestion",
                    "Healthy skin & coat",
                    "Joint support",
                ],
                "translated_claims": self._get_translated_claims(LOCALE),
            }

            json_str = (
                json.dumps(
                    data,
                    ensure_ascii=False,
                )
                .encode("utf-8")
                .decode()
            )
            print(f"=== BAG LABEL {count} of {total_count}")
            print(json_str)

            if execute:
                _ = input(
                    f"🚨 Hit return to print label above on Printer ID {PRINTER_ID} ..."
                )
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

        ENDPOINT = (
            "https://printables.backyard.tails.com/printers/{printer_id}/render-print"
        )
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
        description=f"tools/print_custom_tails_label.py (v{_VERSION})",
    )
    p.add_argument(
        "-e",
        "--execute",
        help=f"send the request to a real printer (id={PRINTER_ID})",
        action="store_true",
    )
    args = p.parse_args()

    bls = BagLabelService()
    bls.generate_labels(
        execute=args.execute,
    )
