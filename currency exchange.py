#Autor: Lir Goffer, ID:209103274
class Coin:
    """
    class represent a coin
    """
    def __init__(self, amount):
        self.__amount = amount

    @property
    def get_amount(self):
        """
        origin amount coin
        :return:
        """
        return self.__amount

    def __str__(self):
        return f"{self.__amount}"


class Euro(Coin):
    """
    class represent euro coin
    """
    def __str__(self):
        return Coin.__str__(self) + "€"

    def __repr__(self):
        return f"Euro({self.get_amount})"

    def amount(self):
        """
        convert to shekel
        :return: amount in shekel
        """
        global rates
        return rates[('euro', 'nis')] * self.get_amount

    def __add__(self, other):
        """
        add value of same coin
        :param other: value
        :return: cal result
        """
        return add(self, other)


class Dollar(Coin):
    """
    class represent dollar coin
    """
    def __str__(self):
        return Coin.__str__(self) + "$"

    def __repr__(self):
        return f"Dollar({self.get_amount})"

    def amount(self):
        """
        convert to shekel
        :return: amount in shekel
        """
        global rates
        return rates[('dollar', 'nis')] * self.get_amount

    def __add__(self, other):
        """
        add value of same coin
        :param other: value
        :return: cal result
        """
        return add(self, other)


class Shekel(Coin):
    """
    class represent shekel coin
    """
    def __str__(self):
        return Coin.__str__(self) + "nis"

    def __repr__(self):
        return f"Shekel({self.get_amount})"

    def amount(self):
        return self.get_amount

    def __add__(self, other):
        """
        add value of same coin
        :param other: value
        :return:
        """
        return add(self, other)


############################################################
def type_tag(x):
    return type_tag.type_dict[type(x)]


type_tag.type_dict = {Shekel: 'nis', Dollar: 'dollar', Euro: 'euro'}


def add(m1, m2):
    """
    add two types of coin
    :param m1: type coin
    :param m2: type coin
    :return: call the dict
    """
    types = (type_tag(m1), type_tag(m2))
    return add.implementations[types](m1, m2)


def add_dollar_euro(d, e):
    global rates
    return Dollar(d.get_amount + rates[('euro', 'dollar')] * e.get_amount)


def add_euro_dollar(e, d):
    global rates
    return Euro(e.get_amount + (1 / rates[('euro', 'dollar')]) * d.get_amount)


def add_dollar_shekel(d, s):
    global rates
    return Dollar(d.get_amount + (1 / rates[('dollar', 'nis')]) * s.get_amount)


def add_euro_shekel(e, s):
    global rates
    return Euro(e.get_amount + (1 / rates[('euro', 'nis')]) * s.get_amount)


add.implementations = {}

add.implementations[('nis', 'nis')] = lambda x, y: Shekel(x.amount() + y.amount())
add.implementations[('nis', 'euro')] = add.implementations[('nis', 'nis')]
add.implementations[('nis', 'dollar')] = add.implementations[('nis', 'nis')]

add.implementations[('dollar', 'euro')] = add_dollar_euro
add.implementations[('dollar', 'nis')] = add_dollar_shekel
add.implementations[('dollar', 'dollar')] = lambda x, y: Dollar(x.get_amount + y.get_amount)

add.implementations[('euro', 'dollar')] = add_euro_dollar
add.implementations[('euro', 'nis')] = add_euro_shekel
add.implementations[('euro', 'euro')] = lambda x, y: Euro(x.get_amount + y.get_amount)


def sub(m1, m2):
    """
    sub two types of coin
    :param m1: type coin
    :param m2: type coin
    :return: dict with types
    """
    types = (type_tag(m1), type_tag(m2))
    return sub.implementations[types](m1, m2)


def sub_dollar_euro(d, e):
    global rates
    return Dollar(d.get_amount - rates[('euro', 'dollar')] * e.get_amount)


def sub_euro_dollar(e, d):
    global rates
    return Euro(e.get_amount - (1 / rates[('euro', 'dollar')]) * d.get_amount)


def sub_dollar_shekel(d, s):
    global rates
    return Dollar(d.get_amount - (1 / rates[('dollar', 'nis')]) * s.get_amount)


def sub_euro_shekel(e, s):
    global rates
    return Euro(e.get_amount - (1 / rates[('euro', 'nis')]) * s.get_amount)


sub.implementations = {}

sub.implementations[('nis', 'nis')] = lambda x, y: Shekel(x.amount() - y.amount())
sub.implementations[('nis', 'euro')] = sub.implementations[('nis', 'nis')]
sub.implementations[('nis', 'dollar')] = sub.implementations[('nis', 'nis')]

sub.implementations[('dollar', 'euro')] = sub_dollar_euro
sub.implementations[('dollar', 'nis')] = sub_dollar_shekel
sub.implementations[('dollar', 'dollar')] = lambda x, y: Dollar(x.get_amount - y.get_amount)

sub.implementations[('euro', 'dollar')] = sub_euro_dollar
sub.implementations[('euro', 'nis')] = sub_euro_shekel
sub.implementations[('euro', 'euro')] = lambda x, y: Euro(x.get_amount - y.get_amount)


def apply(func, m1, m2):
    """
    sent to the key dict the dict with the request operation
    :param func: type of operation
    :param m1: type coin
    :param m2: type coin
    :return: dict with the request operation
    """
    func_dict = {'add': add, 'sub': sub}
    return func_dict[func](m1, m2)



#########################################################

coercions = {}
coercions[('dollar', 'nis')] = lambda d: Shekel(d.amount())
coercions[('euro', 'nis')] = lambda e: Shekel(e.amount())

def coerce_apply(func, x, y):
    tx, ty = type_tag(x), type_tag(y)
    if tx != 'nis':
        x = coercions[(tx, 'nis')](x)
        tx = 'nis'
    if ty != 'nis':
        y = coercions[(ty, 'nis')](y)
        ty = 'nis'
    return coerce_apply.implementations[func](x, y)

coerce_apply.implementations = {}
coerce_apply.implementations['add'] = add.implementations[('nis', 'nis')]
coerce_apply.implementations['sub'] = sub.implementations[('nis', 'nis')]

