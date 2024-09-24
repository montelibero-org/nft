#!/usr/bin/env python3

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring


from typing import Optional

from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder


OPERATOR_KP = Keypair.from_secret(open("/tmp/a").read().strip())

ISSUER_KP = Keypair.from_secret(
    "SCGZP5RWVGLZ6HQHF4ANMZHRSQANRZ2SVJEHFWEDN5P6WQUAWA7FWGIW"
)
ISSUER_ACCOUNT = (
    ISSUER_KP.public_key
    # GBGWJMXGISX5YXQMTWOPJT6QZADQLFJPHREXDTM7JJCSOZWC7BVM3NFT
)

TOKEN_NAMES = ["Hub1369p13"]
TOKENS_TO_MINT = [Asset(name, ISSUER_ACCOUNT) for name in TOKEN_NAMES]
TOKENS_TO_BURN = []

TOKEN_HOLDER = "GBJ3HT6EDPWOUS3CUSIJW5A4M7ASIKNW4WFTLG76AAT5IE6VGVN47TIC"
# TOKEN_HOLDER = "GCOJHUKGHI6IATN7AIEK4PSNBPXIAIZ7KB2AWTTUCNIAYVPUB2DMCITY"

DISTRIBUTOR_ACCOUNT = "GDPHAKGLJ3B56BK4CZ2VMTYEDI6VZ2CTHUHSFAFSPGSTJHZEI3ATOKEN"
DISTRIBUTOR_KP = Keypair.from_public_key(DISTRIBUTOR_ACCOUNT)

ATOMIC_TOKEN = "0.0000001"

SERVER = Server("https://horizon.stellar.org")


class TokenBuilder(TransactionBuilder):
    issuer_address: str

    def __init__(self, source_address: str, issuer_address: str):
        self.issuer_address = issuer_address
        source_account = SERVER.load_account(source_address)
        super().__init__(source_account, Network.PUBLIC_NETWORK_PASSPHRASE, 100)

    def create_issuer(self):
        self.append_create_account_op(self.issuer_address, "1")

    def init_and_lock_issuer(self):
        self.append_set_options_op(
            home_domain="nft.montelibero.org",
            master_weight=0,
            source=self.issuer_address,
        )

    def create_and_init_issuer(self):
        self.create_issuer()
        self.init_issuer()

    def set_issuer_data(self, key, value):
        self.append_manage_data_op(key, value, source=self.issuer_address)

    def trust(self, asset: Asset, source: Optional[str] = None):
        self.append_change_trust_op(asset, limit=ATOMIC_TOKEN, source=source)

    def mint_to(self, asset: Asset, receiver: str):
        self.trust(
            asset,
            source=(
                None if receiver == self.source_account.account.account_id else receiver
            ),
        )
        self.append_payment_op(
            receiver, asset, ATOMIC_TOKEN, source=self.issuer_address
        )

    def mint(self, asset: Asset):
        self.mint_to(asset, DISTRIBUTOR_ACCOUNT)

    def build_and_sign(self, signers):
        transaction = self.build()
        for signer in signers:
            transaction.sign(signer)
        return transaction

    def send(self, asset: Asset, source: str, destination: str):
        self.append_payment_op(destination, asset, ATOMIC_TOKEN, source)

    def send_from_distributor(self, asset: Asset, destination: str):
        self.send(asset, DISTRIBUTOR_ACCOUNT, destination)

    def untrust(self, asset: Asset, source: Optional[str] = None):
        self.append_change_trust_op(asset=asset, limit="0", source=source)

    def burn(
        self, asset: Asset, amount: str = ATOMIC_TOKEN, source: Optional[str] = None
    ):
        self.append_payment_op(
            destination=asset.issuer or "",
            asset=asset,
            amount=amount,
            source=source,
        )

    def burn_and_untrust(self, asset: Asset, source: str):
        self.send(asset=asset, source=source, destination=asset.issuer or "")
        self.untrust(asset, source)


def main():
    builder = TokenBuilder(
        source_address=DISTRIBUTOR_ACCOUNT, issuer_address=ISSUER_ACCOUNT
    )
    builder.add_text_memo("+Hub13")

    # builder.create_issuer()
    # for token in TOKENS_TO_MINT:
    #     # builder.trust(token, DISTRIBUTOR_ACCOUNT)
    #     builder.mint_to(token, TOKEN_HOLDER)
    # builder.init_and_lock_issuer()

    # correct mistakes
    builder.untrust(
        Asset("BP1369p13", "GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT")
    )
    builder.trust(
        Asset("BP1369p14", "GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT")
    )
    builder.untrust(
        Asset("Hub1369p14", "GCTE2BR4WYD73Y3KRC6JOX2LYFH5WKAWO7VYCZXVZ5XLNWMYCIQFDNFT")
    )
    builder.trust(
        Asset("Hub1369p13", "GBGWJMXGISX5YXQMTWOPJT6QZADQLFJPHREXDTM7JJCSOZWC7BVM3NFT")
    )

    # for token in TOKENS_TO_BURN:
    #     builder.burn(token)
    #     builder.untrust(token)

    # transaction = builder.build()
    transaction = builder.build_and_sign([OPERATOR_KP])
    print(transaction.to_xdr())
    print(SERVER.submit_transaction(transaction))


if __name__ == "__main__":
    main()
