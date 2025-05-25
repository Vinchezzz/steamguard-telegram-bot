import hmac
import json
import struct
from base64 import b64decode, b64encode
from hashlib import sha1
from pathlib import Path
from time import time


class AccountManager:
    def __init__(self, accounts_file):
        self.accounts_file = accounts_file
        self.accounts = self.load_accounts()
    
    def load_accounts(self):
        """Loads JSON data"""
        try:
            with open(self.accounts_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def get_code(self, account_id):
        shared_secret = self.accounts[account_id]['shared_secret']
        
        """Returns 2FA code"""
        if account_id not in self.accounts:
            raise ValueError(f"Аккаунт {account_id} не найден")
        
        # Calling get_code()
        if timestamp is None:
            timestamp = int(time())
        time_buffer = struct.pack('>Q', timestamp // 30)  # pack as Big endian, uint64
        time_hmac = hmac.new(b64decode(shared_secret), time_buffer, digestmod=sha1).digest()
        begin = ord(time_hmac[19:20]) & 0xF
        full_code = struct.unpack('>I', time_hmac[begin:begin + 4])[0] & 0x7FFFFFFF  # unpack as Big endian uint32
        chars = '23456789BCDFGHJKMNPQRTVWXY'
        code = ''

        for _ in range(5):
            full_code, i = divmod(full_code, len(chars))
            code += chars[i]

        return code