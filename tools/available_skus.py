"""
Script:      tools/available_skus.py
Description: ...
Author:      Xander Jones (xander@xljones.com)
Web:         xljones.com
Date:        07 Aug 2025
"""

import argparse
import requests

_VERSION = "1.0.0"


def _get_blocked_skus(site_id: int) -> list[int]:
    """
    Fetches the list of blocked SKUs from the specified URL.
    """
    url = f"https://warehouse-service.backyard.tails.com/warehouses/{site_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["data"]
        blocked_skus_str = data.get("blocked_skus", [])
        return [int(sku) for sku in blocked_skus_str if sku.isdigit()]
    else:
        print(f"Error fetching blocked SKUs: {response.status_code}")
        return []


def _get_machines(site_id: int) -> list[dict]:
    """
    Fetches the list of all machines from the specified URL.
    """
    url = f"https://api.adamm.backyard.tails.com//api/machines?site_id={site_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["data"]
        return data
    else:
        print(f"Error fetching machines: {response.status_code}")
        return {}


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="tools/available_skus.py (v{0})".format(_VERSION)
    )
    p.add_argument("-s", "--site-id", help="", default=1)
    p.add_argument("-l", "--limit", help="", default=825)

    args = p.parse_args()

    blocked_skus = _get_blocked_skus(site_id=args.site_id)
    print(f"Site {args.site_id} Blocked SKUs: {blocked_skus}")

    machines = _get_machines(site_id=args.site_id)

    for machine in machines:
        machine_id = machine["machine_id"]
        active_skus = machine["active_skus"]
        supported_stores = machine["supported_stores"]
        available_skus = [sku for sku in active_skus if sku not in blocked_skus]
        print()
        print("Machine ID:", machine_id)
        print(f"Machine {machine_id} Active SKUs:    {active_skus}")
        print(f"Machine {machine_id} available SKUs: {available_skus}")
        print(
            f"query_str: /adamm/packages?limit={args.limit}&"
            f"{'&'.join(f'store={store}' for store in supported_stores)}&"
            f"{'&'.join(f'blocked_sku={sku}' for sku in blocked_skus)}&"
            f"{'&'.join(f'kibble_sku={sku}' for sku in active_skus)}"
        )
