#!/usr/bin/env python3

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring


from argparse import ArgumentParser, Namespace
from decimal import Decimal
from typing import Optional

from stellar_sdk import Asset, Server
import yaml


SERVER = Server("https://horizon.stellar.org")


SMITHY_ACCOUNT = "GDPHAKGLJ3B56BK4CZ2VMTYEDI6VZ2CTHUHSFAFSPGSTJHZEI3ATOKEN"


def get_account():
    return SERVER.accounts().account_id(SMITHY_ACCOUNT).call()


def get_holder(code: str, issuer: str) -> Optional[str]:
    accounts = (
        SERVER.accounts().for_asset(Asset(code, issuer)).call()["_embedded"]["records"]
    )
    holders = [
        account["id"]
        for account in accounts
        for balance in account["balances"]
        if balance["balance"] == "0.0000001"
        and balance["asset_code"] == code
        and balance["asset_issuer"] == issuer
    ]
    return holders[0] if holders else None


def parse_args() -> Namespace:
    arp = ArgumentParser()
    arp.add_argument("-i", "--issuer", action="store_true", help="Show token issuers")
    arp.add_argument("-o", "--other", action="store_true", help="Show other holders")
    return arp.parse_args()


def check_insert(adict: dict[str, str], k: str, value: str) -> None:
    if k in adict:
        raise ValueError("Asset code conflict")
    adict[k] = value


def main() -> None:
    args = parse_args()

    smithy = get_account()
    balances = smithy["balances"]
    trust: dict[str, str] = {}
    hold: dict[str, str] = {}
    for asset in balances:
        if asset["asset_type"] == "native":
            continue
        code = asset["asset_code"]
        balance_raw = int(Decimal(asset["balance"]) * Decimal(10_000_000))
        issuer = asset["asset_issuer"]
        if balance_raw == 0:
            check_insert(trust, code, issuer)
        elif balance_raw == 1:
            check_insert(hold, code, issuer)
        else:
            raise NotImplementedError
    print(
        yaml.dump(
            {
                "Smithy trusts": ", ".join(
                    (f"{code}-{issuer}" for code, issuer in trust.items())
                    if args.issuer
                    else trust.keys()
                ),
                "Smithy holds": ", ".join(
                    (f"{code}-{issuer}" for code, issuer in hold.items())
                    if args.issuer
                    else hold.keys()
                ),
            }
        )
    )

    if args.other:
        print("Other holders:")
        for code, issuer in trust.items():
            asset = f"{code}-{issuer}" if args.issuer else code
            print(f"  {asset} is held by ", end="")
            print(get_holder(code, issuer))


if __name__ == "__main__":
    main()
