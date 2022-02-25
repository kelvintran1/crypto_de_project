import requests
import pymysql
from eth_wallet_queries import INSERT_WALLET_BALANCE, INSERT_TOKEN_INFO, INSERT_WALLET_HOLDINGS, INSERT_TRANSACTIONS
from connect.mysql_config import HOST, PORT, USER, PASSWORD, DB
from datetime import datetime
from connect.wallet_addresses import WALLETS

ETHPLORER_API_KEY = ''
ETHPLORER_URL = ''


class WalletInfoParser:

    def __init__(self, wallet_address=None, owner=None):
        self.info_dict = {}
        self.token_info = {}
        self.wallet_address = wallet_address
        self.wallet_id = None
        self.owner = owner
        self.conn = pymysql.connect(host=HOST, user=USER, port=PORT, passwd=PASSWORD, db=DB)
        self.cursor = self.conn.cursor()

    def get_wallet_info(self):
        endpoint = 'getAddressInfo/'
        balance_url = ETHPLORER_URL + endpoint + self.wallet_address + '?apiKey=' + ETHPLORER_API_KEY
        response = requests.get(balance_url)
        response_json = response.json()
        self.info_dict['address'] = response_json['address']
        self.info_dict['transaction_count'] = response_json['countTxs']
        self.info_dict['eth_holdings'] = response_json['ETH']['balance']
        self.info_dict['eth_current_price'] = response_json['ETH']['price']['rate']
        try:
            self.info_dict['tokens'] = response_json['tokens']
        except KeyError:
            self.info_dict['tokens'] = []

    def load_wallet_balance(self):
        self.cursor.execute(INSERT_WALLET_BALANCE,
                            (self.info_dict['address'], self.owner, self.info_dict['transaction_count'],
                             self.info_dict['eth_holdings'], self.info_dict['transaction_count'],
                             self.info_dict['eth_holdings']))
        self.conn.commit()

    def load_token_info(self):
        for token in self.info_dict['tokens']:
            self.token_info['token_address'] = token['tokenInfo']['address']
            self.token_info['name'] = token['tokenInfo'].get('name', None)
            self.token_info['price'] = None if not token['tokenInfo']['price'] else token['tokenInfo']['price']['rate']
            self.token_info['symbol'] = token['tokenInfo'].get('symbol', None)
            self.token_info['balance'] = token['balance']
            self.cursor.execute(INSERT_TOKEN_INFO,
                                (self.token_info['token_address'], self.token_info['name'], self.token_info['price'],
                                 self.token_info['symbol'], self.token_info['price']))
            self.load_wallet_holding()

        self.conn.commit()

    def load_wallet_holding(self):
        self.cursor.execute("SELECT id FROM `wallet` WHERE address=%s", self.info_dict['address'])
        self.wallet_id = self.cursor.fetchone()
        self.cursor.execute("SELECT id FROM `token` WHERE address=%s", self.token_info['token_address'])
        token_id = self.cursor.fetchone()
        self.cursor.execute(INSERT_WALLET_HOLDINGS,
                            (self.wallet_id, token_id, self.token_info['balance'], self.token_info['balance']))

    def get_transactions(self):
        endpoint = 'getAddressTransactions/'
        balance_url = ETHPLORER_URL + endpoint + self.wallet_address + '?apiKey=' + ETHPLORER_API_KEY
        params = {'limit': 1000}

        transactions = requests.get(balance_url, params=params).json()
        self.cursor.execute("SELECT id FROM `wallet` WHERE address=%s", self.wallet_address)
        self.wallet_id = self.cursor.fetchone()
        for transaction in transactions:
            self.cursor.execute(INSERT_TRANSACTIONS,
                                (self.wallet_id,
                                 datetime.fromtimestamp(transaction['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                                 transaction['from'], transaction['to'], transaction['hash'], transaction['value'],
                                 1 if transaction['success'] else 0,
                                 'IN' if transaction['to'] == self.wallet_address else 'OUT', transaction['hash']))
        self.conn.commit()


if __name__ == '__main__':
    for wallet in WALLETS.items():
        celeb_wallet = WalletInfoParser(wallet[1], wallet[0])
        celeb_wallet.get_transactions()
        celeb_wallet.get_wallet_info()
        celeb_wallet.load_wallet_balance()
        celeb_wallet.load_token_info()
        print('Finished with', wallet[0])
