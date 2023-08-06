from graphenebase.types import (
    Uint8, Int16, Uint16, Uint32, Uint64,
    Varint32, Int64, String, Bytes, Void,
    Array, PointInTime, Signature, Bool,
    Set, Fixed_array, Optional, Static_variant,
    Map, Id, VoteId,
    ObjectId as GPHObjectId
)
from .cybex_types import (
    Ripemd160
)

from collections import OrderedDict
from graphenebase.objects import GrapheneObject, isArgsThisClass
from bitsharesbase.account import PublicKey
from bitsharesbase.objects import (
    ObjectId,
    Price,
    Asset
)

from bitshares.utils import formatTimeFromNow
class TransferExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions #############################
        class Vesting_ext(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('vesting_period', Uint64(kwargs['vesting_period'])),
                        ('public_key', PublicKey(kwargs['public_key'], prefix = 'CYB'))
                    ]))

        class Xfer_to_name_ext(GrapheneObject):
            def __init__(self, kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('name', String(kwargs['name'])),
                        ('asset_sym', String(kwargs['asset_sym'])),
                        ('fee_asset_sym', String(kwargs['fee_asset_sym'])),
                        ('hw_cookie1', Uint8(kwargs['hw_cookie1'])),
                        ('hw_cookie2', Uint8(kwargs['hw_cookie2']))
                    ]))
        # End of Extensions definition ###########

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

        a = []

        sorting = sorted(kwargs, key=lambda x: x[0])
        for ext in sorting:
            if ext[0] == 1:
                a.append(Static_variant(
                    Vesting_ext(ext[1]),
                    ext[0])
                )
            elif ext[0] == 4:
                a.append(Static_variant(
                    Xfer_to_name_ext(ext[1]),
                    ext[0])
                )
            else:
                raise NotImplementedError("Extension {} is unknown".format(ext[0]))

        super().__init__(a)

class AssetIssueExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions #############################
        class Vesting_ext(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('vesting_period', Uint64(kwargs['vesting_period'])),
                        ('public_key', PublicKey(kwargs['public_key'], prefix = 'CYB'))
                    ]))
        # End of Extensions definition ###########

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

        a = []

        sorting = sorted(kwargs, key=lambda x: x[0])
        for ext in sorting:
            if ext[0] == 1:
                a.append(Static_variant(
                    Vesting_ext(ext[1]),
                    ext[0])
                )
            else:
                raise NotImplementedError("Extension {} is unknown".format(ext[0]))

        super().__init__(a)

class LimitOrderCreateExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions ############################
        class Order_side_ext(GrapheneObject):
            def __init__(self, kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('is_buy', Bool(kwargs['is_buy']))
                    ]))
        # End of Extensions definition ##########
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

        if len(kwargs) == 0:           
            return super().__init__([])

        a = []
        ext = kwargs[0]
        assert ext[0] == 7
        a.append(Static_variant(
            Order_side_ext(ext[1]),
            ext[0]
        ))
        super().__init__(a)

class LimitOrderCancelExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions ############################
        class Cancel_trx_id_ext(GrapheneObject):
            def __init__(self, kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('trx_id', Ripemd160(kwargs['trx_id']))
                    ]))
        # End of Extensions definition ##########
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

        if len(kwargs) == 0:           
            return super().__init__([])

        a = []
        ext = kwargs[0]
        assert ext[0] == 6
        a.append(Static_variant(
            Cancel_trx_id_ext(ext[1]),
            ext[0]
        ))
        super().__init__(a)

class AssertPredications(Array):
    def __init__(self, *args, **kwargs):
        class Account_name_eq_lit_predicate(GrapheneObject):
            def __init__(self, kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('account_id', ObjectId(kwargs['account_id'], 'account')),
                        ('name', String(kwargs['name']))
                    ]))

        class Asset_symbol_eq_lit_predicate(GrapheneObject):
            def __init__(self, kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('asset_id', ObjectId(kwargs['asset_id'], 'asset')),
                        ('symbol', String(kwargs['symbol']))
                    ]))

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
        a = []

        sorting = sorted(kwargs, key = lambda x: x[0])
        for ext in sorting:
            if ext[0] == 0:
                a.append(Static_variant(
                    Account_name_eq_lit_predicate(ext[1]),
                    ext[0]
                ))
            elif ext[0] == 1:
                a.append(Static_variant(
                    Asset_symbol_eq_lit_predicate(ext[1]),
                    ext[0]
                ))
            else:
                raise NotImplementedError("Extension {} is unknown".format(ext[0]))

        super().__init__(a)

class ExchangeOptionExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions #############################
        class Check_once_amount(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('asset_id', ObjectId(kwargs['asset_id'], "asset")),
                        ('min', Int64(kwargs['min'])),
                        ('max', Int64(kwargs['max']))
                    ]))

        class Check_divisible(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('divisor', Asset(kwargs['divisor']))
                    ]))

        class Check_exchange_amount(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('asset_id', ObjectId(kwargs['asset_id'], "asset")),
                        ('floor', Int64(kwargs['floor'])),
                        ('ceil', Int64(kwargs['ceil']))
                    ]))

        class Vesting_policy_initializer(GrapheneObject):
            # Vesting policy initializer definitions ###############
            # End of Vesting policy initializer definitions ########
                
            def __init__(self, kwargs): 
                class Vesting_policy(Static_variant):
                    def __init__(self, kwargs): 
                        class Linear_vesting_policy_initializer(GrapheneObject):
                            def __init__(self, kwargs): 
                                if isArgsThisClass(self, args):
                                    self.data = args[0].data
                                else:
                                    if len(args) == 1 and len(kwargs) == 0:
                                        kwargs = args[0]
                                    super().__init__(OrderedDict([
                                        ('begin_timestamp', PointInTime(kwargs['begin_timestamp'])),
                                        ('vesting_cliff_seconds', Uint32(kwargs['vesting_cliff_seconds'])),
                                        ('vesting_duration_seconds', Uint32(kwargs['vesting_duration_seconds']))
                                    ]))
                        class Cdd_vesting_policy_initializer(GrapheneObject):
                            def __init__(self, kwargs): 
                                if isArgsThisClass(self, args):
                                    self.data = args[0].data
                                else:
                                    if len(args) == 1 and len(kwargs) == 0:
                                        kwargs = args[0]
                                    super().__init__(OrderedDict([
                                        ('start_claim', PointInTime(kwargs['start_claim'])),
                                        ('vesting_seconds', Uint32(kwargs['vesting_seconds']))
                                    ]))
                        if isArgsThisClass(self, args):
                            self.data = args[0].data
                        else:
                            if len(args) == 1 and len(kwargs) == 0:
                                kwargs = args[0]
                            if kwargs[0] == 0:
                                super().__init__(Linear_vesting_policy_initializer(kwargs[1]), 0)
                            elif kwargs[0] == 1:
                                super().__init__(Cdd_vesting_policy_initializer(kwargs[1]), 1)
                            else:
                                raise NotImplementedError("Vesting policy {} is unknown".format(ext[0]))
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([("policy", Vesting_policy(kwargs["policy"]))]))

        class Vesting_seconds(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('vesting_seconds', Uint32(kwargs['vesting_seconds']))
                    ]))
        
        class Secondary_price(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('rate', Price(kwargs['rate']))
                    ]))
        # End of Extensions definition ###########

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

        a = []

        sorting = sorted(kwargs, key=lambda x: x[0])
        for ext in sorting:
            if ext[0] == 0:
                a.append(Static_variant(Check_exchange_amount(ext[1]), 0))
            elif ext[0] == 1:
                a.append(Static_variant(Check_once_amount(ext[1]), 1))
            elif ext[0] == 2:
                a.append(Static_variant(Check_divisible(ext[1]), 2))
            elif ext[0] == 3: # vesting policy quote
                a.append(Static_variant(Vesting_policy_initializer(ext[1]), 3))
            elif ext[0] == 4: # vesting policy base
                a.append(Static_variant(Vesting_policy_initializer(ext[1]), 4))
            elif ext[0] == 5: # vesting seconds quote
                a.append(Static_variant(Vesting_seconds(ext[1]), 5))
            elif ext[0] == 6: # vesting seconds base
                a.append(Static_variant(Vesting_seconds(ext[1]), 6))
            elif ext[0] == 7: # secondary price
                a.append(Static_variant(Secondary_price(ext[1]), 7))
            else:
                raise NotImplementedError("Extension {} is unknown".format(ext[0]))

        super().__init__(a)

class ExchangeOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('rate', Price(kwargs["rate"])),
                ('owner_permissions', Uint32(kwargs["owner_permissions"])),
                ('flags', Uint32(kwargs["flags"])),
                ('whitelist_authorities',
                    Array([ObjectId(x, "account") for x in kwargs["whitelist_authorities"]])),
                ('blacklist_authorities',
                    Array([ObjectId(x, "account") for x in kwargs["blacklist_authorities"]])),
                ('extensions', ExchangeOptionExtensions(kwargs['extensions'])),
                ('description', String(kwargs["description"]))
            ]))

class NonfungibleOptionExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions #############################
        class First_trade_fee_multi_ext(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('multiple', Uint32(kwargs['multiple']))
                    ]))
        # End of Extensions definition ###########

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

        a = []

        sorting = sorted(kwargs, key=lambda x: x[0])
        for ext in sorting:
            if ext[0] == 0:
                a.append(Static_variant(
                    First_trade_fee_multi_ext(ext[1]),
                    ext[0])
                )
            else:
                raise NotImplementedError("Extension {} is unknown".format(ext[0]))

        super().__init__(a)

class Token_flat_set(Array):
    def __init__(self, d):
        super().__init__(
            sorted(d, key = lambda x: (x.space << 56) + (x.type << 48) + int(x.Id.split('.')[-1]))
        )

class NonfungibleOptions(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('max_supply', Int64(kwargs["max_supply"])),
                ('issuer_permissions', Uint16(kwargs["issuer_permissions"])),
                ('flags', Uint16(kwargs["flags"])),
                ('whitelist_authorities',
                    Token_flat_set([ObjectId(x, "account") for x in kwargs["whitelist_authorities"]])),
                ('blacklist_authorities',
                    Token_flat_set([ObjectId(x, "account") for x in kwargs["blacklist_authorities"]])),
                ('whitelist_markets',
                    Token_flat_set([ObjectId(x, "asset") for x in kwargs["whitelist_markets"]])),
                ('blacklist_markets',
                    Token_flat_set([ObjectId(x, "asset") for x in kwargs["blacklist_markets"]])),
                ('description', String(kwargs["description"])),
                ('extensions', NonfungibleOptionExtensions(kwargs["extensions"]))
            ]))

# replace graphenebase.types.Static_variant with this,
# since token attribute value is not `GrapheneObject`
from graphenebase.types import varint, JsonObj
import json

class Token_static_variant():
    """ Graphene Static_variant type does not support simple data
        such as Uint8/String/Uint64 as variant data
    """
    def __init__(self, d, type_id):
        self.data = d
        self.type_id = type_id

    def __bytes__(self):
        return varint(self.type_id) + bytes(self.data)

    def __str__(self):
        if isinstance(self.data, Uint8):
            return json.dumps([self.type_id, self.data.data])
        elif isinstance(self.data, Uint64):
            return json.dumps([self.type_id, self.data.data])
        elif isinstance(self.data, String):
            return json.dumps([self.type_id, str(self.data)])
        elif isinstance(self.data, GrapheneObject):
            return json.dumps([self.type_id, JsonObj(self.data)])

    def __json__(self):
        return json.loads(self.__str__())

        
class Token_attr_map():    
    def __init__(self, data):
        self.data = data

    def __bytes__(self):
        b = b""
        b += varint(len(self.data))
        for e in self.data:
            b += bytes(e[0]) + bytes(e[1]) 
        return b
                                                                                                                                                 
    def __str__(self):
        r = []
        for e in self.data:                                                                                                                      
            r.append([str(e[0]), JsonObj(e[1])])
        return json.dumps(r)

class TokenAttributes(Token_attr_map):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            r = []
            for k, v in kwargs:
                if v[0] == 0:
                    r.append((String(k), Token_static_variant(String(v[1]), 0)))
                elif v[0] == 1:
                    if int(v[1]) < 0:
                        raise Exception("Cannot use nagtive integer as param value")
                    r.append((String(k), Token_static_variant(Uint64(v[1]), 1)))
                else:
                    raise NotImplementedError("Param type unknown")
            super().__init__(r)

class FilterStack(Array):
    def __init__(self, *args, **kwargs):
        class BooleanExpression(GrapheneObject):
            def __init__(self, *args, **kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    if kwargs['val'][0] == 0:
                        val = Token_static_variant(String(kwargs['val'][1]), 0)
                    elif kwargs['val'][0] == 1:
                        if int(kwargs['val'][1]) < 0:
                            raise Exception("Cannot use nagtive integer as param value")
                        val = Token_static_variant(Uint64(kwargs['val'][1]), 1)
                    else:
                        raise NotImplementedError("Param type unknown")
                    super().__init__(OrderedDict([
                        ('op', Uint8(kwargs['op'])),
                        ('key', String(kwargs['key'])),
                        ('val', val)
                    ]))

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            r = []
            for i in kwargs:
                if i[0] == 0:
                    r.append(Token_static_variant(Uint8(i[1]), 0))
                else:
                    r.append(Token_static_variant(BooleanExpression(i[1]), 1))
            super().__init__(r)

class TokenSelector(GrapheneObject):
    def __init__(self, *args, **kwargs):
        class TokenSelectorVariant(Static_variant):
            def __init__(self, kwargs):
                class TokenIdSelector(GrapheneObject):
                    def __init__(self, *args, **kwargs):
                        if isArgsThisClass(self, args):
                            self.data = args[0].data
                        else:
                            if len(args) == 1 and len(kwargs) == 0:
                                kwargs = args[0]
                            super().__init__(OrderedDict([
                                ('id_set', Token_flat_set([ ObjectId(i) for i in kwargs['id_set'] ]))
                            ]))
                class TokenAttrSelector(GrapheneObject):
                    def __init__(self, *args, **kwargs):
                        if isArgsThisClass(self, args):
                            self.data = args[0].data
                        else:
                            if len(args) == 1 and len(kwargs) == 0:
                                kwargs = args[0]

                            super().__init__(OrderedDict([
                                ('max_count', Uint32(kwargs['max_count'])),
                                ('max_amount', Int64(kwargs['max_amount'])),
                                ('stack', FilterStack(kwargs['stack']))
                            ]))

                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    if kwargs[0] == 0:
                        super().__init__(TokenIdSelector(kwargs[1]), 0)
                    elif kwargs[0] == 1:
                        super().__init__(TokenAttrSelector(kwargs[1]), 1)
                    else:
                        raise NotImplementedError("Unknown selector type {}".format(kwargs[0]))

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('selector', TokenSelectorVariant(kwargs['selector'])),
                ('type', ObjectId(kwargs['type']))
            ]))