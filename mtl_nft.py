# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring


from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder


OPERATOR_KP = Keypair.from_secret('')

ISSUER_KP = Keypair.from_secret('SBDEK5W6N75AC6Q4WB6DTJNJTJHNBWTE4HWTRPUFLTXY3XBFCSQKQYJN')
ISSUER_ACCOUNT = ISSUER_KP.public_key  # GA6I6NJ2U5N7TSSPT6W6E6S46FGX5BJNKQOCPW4ADRA227PUVLQVYNFT

TOKEN_NAMES = [f'BP1369p{a}' for a in range(40, 41)]

TOKENS = [Asset(name, ISSUER_ACCOUNT) for name in TOKEN_NAMES]

DISTRIBUTOR_KP = Keypair.from_public_key('GDPHAKGLJ3B56BK4CZ2VMTYEDI6VZ2CTHUHSFAFSPGSTJHZEI3ATOKEN')

ATOMIC_TOKEN = '0.0000001'

SERVER = Server("https://horizon.stellar.org")


class TokenBuilder(TransactionBuilder):
    def __init__(self):
        operator = SERVER.load_account(OPERATOR_KP)
        super().__init__(operator, Network.PUBLIC_NETWORK_PASSPHRASE, 100)

    def create_issuer(self):
        self.append_create_account_op(ISSUER_ACCOUNT, '1')

    def init_issuer(self):
        self.append_set_options_op(
            home_domain='mtl.montelibero.org', source=ISSUER_ACCOUNT
        )

    def create_and_init_issuer(self):
        self.create_issuer()
        self.init_issuer()

    def set_issuer_data(self, key, value):
        self.append_manage_data_op(key, value, source=ISSUER_ACCOUNT)

    def mint_to(self, asset: Asset, receiver: str):
        self.append_change_trust_op(
            asset,
            limit=ATOMIC_TOKEN,
            source=
                None
                if receiver == self.source_account.account.account_id
                else receiver
        )
        self.append_payment_op(
            receiver, asset, ATOMIC_TOKEN, source=ISSUER_ACCOUNT
        )

    def mint(self, asset: Asset):
        self.mint_to(asset, DISTRIBUTOR_KP.public_key)

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
        self.send(
            asset, source=DISTRIBUTOR_KP.public_key, destination=destination
        )

    def untrust(self, asset: Asset):
        self.append_change_trust_op(
            asset, limit='0', source=DISTRIBUTOR_KP.public_key
        )

    def burn_and_untrust(self, asset: Asset):
        self.send(
            asset,
            source=DISTRIBUTOR_KP.public_key,
            destination = asset.issuer or '',
        )
        self.untrust(asset)


def main():
    builder = TokenBuilder()
    builder.create_and_init_issuer()
    for token in TOKENS:
        builder.mint(token)
    builder.lock_issuer()

    transaction = builder.build_and_sign([ISSUER_KP, OPERATOR_KP])
    print(transaction.to_xdr())
    print(SERVER.submit_transaction(transaction))


if __name__ == '__main__':
    main()
