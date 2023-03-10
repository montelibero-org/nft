#!/usr/bin/env python3

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring


from collections import defaultdict
from decimal import Decimal
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder
import yaml


SERVER = Server("https://horizon.stellar.org")

TOKEN = Asset(
    'BP1369p12a4', 'GDDTITOAZSV6OFHQJ5H2BALN7SNF4RGKZLSEIUA4RTJK44VCWTXEPNFT'
)


def get_offers():
    return SERVER.offers().for_buying(TOKEN).call()['_embedded']['records']


def buying_price(offer):
    selling_price = offer['price_r']
    return selling_price['d'] / selling_price['n']


KNOWN_ASSETS = {
    'EURMTL-GACKTN5DAZGWXRWB2WLM6OPBDHAMT6SJNGLJZPQMEZBUR4JUGBX2UK7V': 'EURMTL'
}


def selling_asset(offer):
    asset = '{asset_code}-{asset_issuer}'.format(**offer['selling'])
    return KNOWN_ASSETS.get(asset, asset)


def main():
    print(
        yaml.dump(
            sorted(
                [
                    {
                        'amount_stellar':
                            str(offer['amount']) + ' ' + selling_asset(offer),
                        'price_full':
                            str(Decimal(offer['amount']) * 100) + ' '
                            + selling_asset(offer) ,
                        'buyer': offer['seller'],
                        # 'offer': offer,
                    }
                    for offer in get_offers()
                ],
                key = lambda x: x['price_full'],
                reverse = True,
            )
        ),
        end='',
    )


if __name__ == '__main__':
    main()
