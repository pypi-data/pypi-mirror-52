from bitshares.blockchainobject import BlockchainObject
from bitshares.amount import Amount
from bitshares.price import Price
from bitshares.utils import formatTimeFromNow
from .exceptions import *
from .account import Account
from .asset import Asset
from . import cybex_operations

class Nonfungible(BlockchainObject):
    permission_flags = {
        "white_list": 0x01,
        "transfer_restricted": 0x02,
        "charge_market_fee": 0x04,
        "allow_trade": 0x08,
        "allow_override": 0x10
    }

    def __init__(
        self,
        nonfungible_id,
        full = False,
        lazy = False,
        cybex_instance = None
    ):
        super().__init__(
            nonfungible_id,
            lazy = lazy,
            full = full,
            bitshares_instance = cybex_instance
        )

    def refresh(self):
        nonfungible = None
        import re
        if re.match("^1\.18\.[0-9]*$", self.identifier):
            nonfungible = self.bitshares.rpc.get_objects([self.identifier])[0]
        else:
            nonfungible = self.bitshares.rpc.lookup_nonfungible_symbols([self.identifier])[0]

        if not nonfungible:
            raise NonfungibleDoesNotExistsException(self.identifier)
        
        super().__init__(nonfungible)
    
    def display(self):
        symbol = self['symbol']
        issuer = Account(self['issuer'], cybex_instance = self.bitshares)['name']
        dyn_prop = self.bitshares.rpc.get_objects([self['dynamic_nonfungible_data_id']])[0]
        token_count = dyn_prop['token_count']
        current_supply = dyn_prop['current_supply']
        def translate_permission(perm):
            _perm = {val:perm for perm, val in self.permission_flags.items() }
            flag = 1
            while flag <= max(_perm.keys()):
                perm_name = _perm[flag]
                yield '{}:\t{}'.format(perm_name, 'Y' if perm & flag else 'N')
                flag <<= 1

        print("=======================")
        print("Display for nonfungible {}".format(self.identifier))
        print("Symbol: {}".format(symbol))
        print("Issuer: {}".format(issuer))
        print("Max supply: {}".format(self['options']['max_supply']))
        print("Issuer Permissions:")
        for l in translate_permission(self['options']['issuer_permissions']):
            print(" " + l)
        print("Flags:")
        for l in translate_permission(self['options']['flags']):
            print(" " + l)

        print("Whitelist Authorities:")
        for a in self['options']['whitelist_authorities']:
            print(" " + Account(a, cybex_instance = self.bitshares)['name'])
            
        print("Blacklist Authorities:")
        for a in self['options']['blacklist_authorities']:
            print(" " + Account(a, cybex_instance = self.bitshares)['name'])

        print("Whitelist Markets:")
        for a in self['options']['whitelist_markets']:
            print(" " + Asset(a, cybex_instance  = self.bitshares)['symbol'])

        print("Blacklist Markets:")
        for a in self['options']['blacklist_markets']:
            print(" " + Asset(a, cybex_instance  = self.bitshares)['symbol'])
        
        print("Description: {}".format(self['options']['description']))

        print("Token count: {}".format(token_count))
        print("Current supply: {}".format(current_supply))
    
    def whitelist(self, account, **kwargs):
        """ replace some account into nonfungible white list
        """
        if isinstance(account, str):
            account = [account]
        
        assert isinstance(account, list)

        options = self['options']

        options['whitelist_authorities'] = [
            Account(acc, cybex_instance = self.bitshares)['id']
            for acc in account]

        if len(options['whitelist_authorities']) > 0 or len(options['blacklist_authorities']) > 0:
            options['flags'] |= self.permission_flags["white_list"]
        else:
            options['flags'] &= ~self.permission_flags["white_list"]
        
        op = cybex_operations.Update_nonfungible(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "nonfungible_to_update": self["id"],
            "new_options": options
        })

        self.bitshares.finalizeOp(op, self["issuer"], "active", **kwargs)

    def blacklist(self, account, **kwargs):
        """ replace some account into nonfungible black list
        """
        if isinstance(account, str):
            account = [account]
        
        assert isinstance(account, list)

        options = self['options']

        options['blacklist_authorities'] = [
            Account(acc, cybex_instance = self.bitshares)['id']
            for acc in account]

        if len(options['whitelist_authorities']) > 0 or len(options['blacklist_authorities']) > 0:
            options['flags'] |= self.permission_flags["white_list"]
        else:
            options['flags'] &= ~self.permission_flags["white_list"]
        
        op = cybex_operations.Update_nonfungible(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "nonfungible_to_update": self["id"],
            "new_options": options
        })

        self.bitshares.finalizeOp(op, self["issuer"], "active", **kwargs)

    def whitelist_market(self, asset, **kwargs):
        """ replace asset into nonfungible white list asset
        """
        if isinstance(asset, str):
            asset = [asset]

        assert isinstance(asset, list)

        options = self['options']

        options['whitelist_markets'] = [
            Asset(sym, cybex_instance = self.bitshares)['id']
            for sym in asset]
        
        if len(options['whitelist_markets']) > 0 or len(options['blacklist_markets']) > 0:
            options['flags'] |= self.permission_flags["allow_trade"]

        op = cybex_operations.Update_nonfungible(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "nonfungible_to_update": self["id"],
            "new_options": options
        })

        self.bitshares.finalizeOp(op, self["issuer"], "active", **kwargs)

    def blacklist_market(self, asset, **kwargs):
        """ replace asset into nonfungible white list asset
        """
        if isinstance(asset, str):
            asset = [asset]

        assert isinstance(asset, list)

        options = self['options']

        options['blacklist_markets'] = [
            Asset(sym, cybex_instance = self.bitshares)['id']
            for sym in asset]
        
        if len(options['whitelist_markets']) > 0 or len(options['blacklist_markets']) > 0:
            options['flags'] |= self.permission_flags["allow_trade"]

        op = cybex_operations.Update_nonfungible(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "nonfungible_to_update": self["id"],
            "new_options": options
        })

        self.bitshares.finalizeOp(op, self["issuer"], "active", **kwargs)

    def deliver_issuer(self, new_issuer, **kwargs):
        """ deliver issuer of nonfungible to a new one
        """
        new_account = Account(new_issuer, cybex_instance = self.bitshares)
        op = cybex_operations.Update_nonfungible(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": self["issuer"],
            "nonfungible_to_update": self["id"],
            "new_issuer": new_account["id"],
            "new_options": self["options"]
        })

        self.bitshares.finalizeOp(op, self['issuer'], "active", **kwargs)

    def hold_by(self, account):
        """ list tokens held by specific account
        """
        account = Account(account, cybex_instance = self.bitshares)
        tokens = self.bitshares.rpc.list_token_objects(account['id'], [self['id']])
        for t in tokens:
            t['owner'] = Account(t['owner'], cybex_instance = self.bitshares)['name']
            attributes = self.bitshares.rpc.get_objects([t['static_token_data_id']])[0]['attributes']
            d = {}
            for k, v in attributes:
                d[k] = v[1]
            t['attributes'] = d
        return tokens

def generate_selector(type_, selector):
    sdic = {"type": type_}

    def reserve_stack(stack, expr):
        if isinstance(expr, list):
            assert len(expr) == 3
            op_dic = {"eq": 0, "gt": 1, "lt": 2, "ge": 3, "le": 4, "ne": 5}
            op_code = op_dic[expr[1]]
            if isinstance(expr[2], str):
                v = [0, expr[2]]
            elif isinstance(expr[2], int):
                v = [1, expr[2]]
            else:
                raise NotImplementedError("Unknown val type")
            stack.append([1, {'op': op_code, 'key': expr[0], 'val': v}])
        elif isinstance(expr, dict):
            op_dic = {"and": 0, "or": 1}
            op_code = op_dic[expr['op']]
            stack.append([0, op_code])
            reserve_stack(stack, expr['expr1'])
            reserve_stack(stack, expr['expr2'])

    if isinstance(selector, list): # list of token id
        sdic["selector"] = [0, {"id_set": [token_id for token_id in selector]} ]
    elif isinstance(selector, dict):
        if 'max_expiration' in selector:
            selector['max_expiration'] = formatTimeFromNow(selector['max_expiration'])
        if 'min_expiration' in selector:
            selector['min_expiration'] = formatTimeFromNow(selector['min_expiration'])
        filter_ = selector["filter"]
        assert isinstance(filter_, list) or isinstance(filter_, dict)
        selector['stack'] = []
        if len(filter_) > 0:
            reserve_stack(selector['stack'], filter_)
        sdic["selector"] = [1, selector]

    return sdic