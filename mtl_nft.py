#!/usr/bin/env python3

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring


from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder


OPERATOR_KP = Keypair.from_secret(
    ''
)

ISSUER_KP = Keypair.from_secret(
    'SBDEK5W6N75AC6Q4WB6DTJNJTJHNBWTE4HWTRPUFLTXY3XBFCSQKQYJN'
)
ISSUER_ACCOUNT = (
    ISSUER_KP.public_key
    # GA6I6NJ2U5N7TSSPT6W6E6S46FGX5BJNKQOCPW4ADRA227PUVLQVYNFT
)

# TOKEN_NAMES = [f'BP1369p{a}' for a in range(40, 41)]

# TOKENS = [Asset(name, ISSUER_ACCOUNT) for name in TOKEN_NAMES]

DISTRIBUTOR_ACCOUNT = 'GDPHAKGLJ3B56BK4CZ2VMTYEDI6VZ2CTHUHSFAFSPGSTJHZEI3ATOKEN'
DISTRIBUTOR_KP = Keypair.from_public_key(DISTRIBUTOR_ACCOUNT)

ATOMIC_TOKEN = '0.0000001'

SERVER = Server("https://horizon.stellar.org")

MTLCITY_ACCOUNT = 'GDUI7JVKWZV4KJVY4EJYBXMGXC2J3ZC67Z6O5QFP4ZMVQM2U5JXK2OK3'
MTLCITY_SHARE = Asset('MTLCITY', MTLCITY_ACCOUNT)

TOKENS = {
    3:  Asset('BP1363p3',  'GDLYDZJAWYJXI5C2VGZGPYOWX3TUPR3AFMBMG5PTRGW2O2OK7MJQPNFT'),
    1:  Asset('BP1369p1',  'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    2:  Asset('BP1369p2',  'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    10: Asset('BP1369p10', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    13: Asset('BP1369p13', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    14: Asset('BP1369p14', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    15: Asset('BP1369p15', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    16: Asset('BP1369p16', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    17: Asset('BP1369p17', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    18: Asset('BP1369p18', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    19: Asset('BP1369p19', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    20: Asset('BP1369p20', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    23: Asset('BP1369p23', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    25: Asset('BP1369p25', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    28: Asset('BP1369p28', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    29: Asset('BP1369p29', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    34: Asset('BP1369p34', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    35: Asset('BP1369p35', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    36: Asset('BP1369p36', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    37: Asset('BP1369p37', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    38: Asset('BP1369p38', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    39: Asset('BP1369p39', 'GC2ZK7OONSYECUWI42A5KXG2M7XIGEC2CIBOD4BJ4EHWYJWV6BHC6NFT'),
    40: Asset('BP1369p40', 'GA6I6NJ2U5N7TSSPT6W6E6S46FGX5BJNKQOCPW4ADRA227PUVLQVYNFT'),
}


class TokenBuilder(TransactionBuilder):
    def __init__(self, account_address: str = None):
        account = SERVER.load_account(account_address or OPERATOR_KP)
        super().__init__(account, Network.PUBLIC_NETWORK_PASSPHRASE, 11_000)

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
    common_plots = [
        3,
        1,
        10,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        2,
        20,
        39,
        40,
    ]
    builder = TokenBuilder(MTLCITY_ACCOUNT)
    for plot_num in common_plots:
        builder.trust(TOKENS[plot_num])
        builder.append_payment_op(
            destination=MTLCITY_ACCOUNT,
            asset=TOKENS[plot_num],
            amount=ATOMIC_TOKEN,
            source=DISTRIBUTOR_ACCOUNT,
        )

    # for (client_account, (plots, price)) in CLIENTS.items():
    #     builder = TokenBuilder(client_account)
    #     builder.burn(MTLCITY, price)
    #     for plot in plots:
    #         builder.trust(TOKENS[plot])
    #         builder.append_payment_op(
    #             client_account, TOKENS[plot], ATOMIC_TOKEN, DISTRIBUTOR_ACCOUNT
    #         )
    #     transaction = builder.build_and_sign([OPERATOR_KP])
    #     print(client_account, transaction.to_xdr())

    # builder.create_and_init_issuer()
    # for token in TOKENS:
    #     builder.mint(token)
    # builder.lock_issuer()

    transaction = builder.build_and_sign([OPERATOR_KP])
    # transaction = builder.build_and_sign([ISSUER_KP, OPERATOR_KP])
    print(transaction.to_xdr())
    # print(SERVER.submit_transaction(transaction))


if __name__ == '__main__':
    main()
