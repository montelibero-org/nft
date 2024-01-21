#!/usr/bin/env python3

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring


from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder


OPERATOR_KP = Keypair.from_secret(
    ''
)

ISSUER_KP = Keypair.from_secret(
    'SAZLFVGFGKWYGTLLLULUFTWCZ7LVNHCBPSV5F7ZQXRGRHC4UXMAJ2BQK'
)
ISSUER_ACCOUNT = (
    ISSUER_KP.public_key
    # GDEYCMUYQ7BHV5UYYBH2BTPCQ3LT3TCYTW6XKKFJCTAS7PK5EQKCGNFT
)

TOKEN_NAMES = [f'UB{a}' for a in [929, 930, 2109, 2116, 2117]]

TOKENS = [Asset(name, ISSUER_ACCOUNT) for name in TOKEN_NAMES]

DISTRIBUTOR_ACCOUNT = 'GDPHAKGLJ3B56BK4CZ2VMTYEDI6VZ2CTHUHSFAFSPGSTJHZEI3ATOKEN'
DISTRIBUTOR_KP = Keypair.from_public_key(DISTRIBUTOR_ACCOUNT)

ATOMIC_TOKEN = '0.0000001'

SERVER = Server("https://horizon.stellar.org")


class TokenBuilder(TransactionBuilder):
    def __init__(self, account_address: str):
        account = SERVER.load_account(account_address)
        super().__init__(account, Network.PUBLIC_NETWORK_PASSPHRASE, 100)

    def create_issuer(self):
        self.append_create_account_op(ISSUER_ACCOUNT, '1')

    def init_issuer(self):
        self.append_set_options_op(
            home_domain='nft.montelibero.org', source=ISSUER_ACCOUNT
        )

    def create_and_init_issuer(self):
        self.create_issuer()
        self.init_issuer()

    def set_issuer_data(self, key, value):
        self.append_manage_data_op(key, value, source=ISSUER_ACCOUNT)

    def trust(self, asset: Asset, account: str = None):
        self.append_change_trust_op(asset, limit=ATOMIC_TOKEN, source=account)

    def mint_to(self, asset: Asset, receiver: str):
        self.trust(
            asset,
            account =
                None
                if receiver == self.source_account.account.account_id
                else receiver,
        )
        self.append_payment_op(
            receiver, asset, ATOMIC_TOKEN, source=ISSUER_ACCOUNT
        )

    def mint(self, asset: Asset):
        self.mint_to(asset, DISTRIBUTOR_ACCOUNT)

    def lock_issuer(self):
        self.append_set_options_op(master_weight=0, source=ISSUER_ACCOUNT)

    def build_and_sign(self, signers):
        transaction = self.build()
        for signer in signers:
            transaction.sign(signer)
        return transaction

    def send(self, asset: Asset, source: str, destination: str):
        self.append_payment_op(destination, asset, ATOMIC_TOKEN, source)

    def send_from_distributor(self, asset: Asset, destination: str):
        self.send(asset, DISTRIBUTOR_ACCOUNT, destination)

    def untrust(self, asset: Asset):
        self.append_change_trust_op(
            asset, limit='0', source=DISTRIBUTOR_ACCOUNT
        )

    def burn(self, asset: Asset, amount: str):
        self.append_payment_op(asset.issuer or '', asset, amount)

    def burn_and_untrust(self, asset: Asset):
        self.send(
            asset, source=DISTRIBUTOR_ACCOUNT, destination = asset.issuer or ''
        )
        self.untrust(asset)


def main():
    builder = TokenBuilder(DISTRIBUTOR_ACCOUNT)
    builder.create_and_init_issuer()
    for token in TOKENS:
        builder.mint(token)
    builder.lock_issuer()

    # transaction = builder.build_and_sign([OPERATOR_KP])
    transaction = builder.build_and_sign([ISSUER_KP, OPERATOR_KP])
    print(transaction.to_xdr())
    # print(SERVER.submit_transaction(transaction))


if __name__ == '__main__':
    main()
