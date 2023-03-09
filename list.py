#!/usr/bin/env python3

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring


from collections import defaultdict
from decimal import Decimal
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder
import yaml


SERVER = Server("https://horizon.stellar.org")


SMITHY_ACCOUNT = 'GDPHAKGLJ3B56BK4CZ2VMTYEDI6VZ2CTHUHSFAFSPGSTJHZEI3ATOKEN'


def get_account():
    return SERVER.accounts().account_id(SMITHY_ACCOUNT).call()


def main():
    smithy = get_account()
    balances = smithy['balances']
    trust = defaultdict(set)
    hold = defaultdict(set)
    for asset in balances:
        if asset['asset_type'] == 'native':
            continue
        code = asset['asset_code']
        balance_raw = int(Decimal(asset['balance']) * Decimal(10_000_000))
        issuer = asset['asset_issuer']
        if balance_raw == 0:
            trust[code].add((code, issuer))
        elif balance_raw == 1:
            hold[code].add((code, issuer))
        else:
            raise NotImplementedError
    for asset in trust.values():
        if len(asset) != 1:
            raise ValueError('asset code conflict', asset)
    for asset in hold.values():
        if len(asset) != 1:
            raise ValueError('asset code conflict', asset)
    print(
        yaml.dump({
            'trust': ', '.join(trust.keys()), 'hold': ', '.join(hold.keys())
        })
    )


if __name__ == '__main__':
    main()
