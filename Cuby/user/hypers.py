import re

# choices
GENDER_CHS = (
    ('0', '未知'),
    ('1', '男'),
    ('2', '女'),
)
IDENTITY_CHS = (
    ('user', '普通用户'),
    ('vip', '会员'),
    ('admin', '管理员'),
)

# constants
MINI_MAX_LEN = 32
BASIC_MAX_LEN = 64
EXT_MAX_LEN = 256
TEL_LEN = 11

# checker lambdas
_EMAIL_REG = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
_PRINTABLE_UNICODES_WITHOUT_BLANK = lambda s: s.isprintable() and ' ' not in s
_PRINTABLE_ASCIIS_WITHOUT_BLANK = lambda s: _PRINTABLE_UNICODES_WITHOUT_BLANK(s) and all(ord(c) < 128 for c in s)

CHECK_NAME = lambda n: all([
    0 < len(n) <= MINI_MAX_LEN,
    _PRINTABLE_UNICODES_WITHOUT_BLANK(n),
])

_CHECK_EMAIL = lambda e: all([
    6 <= len(e) <= MINI_MAX_LEN,
    _PRINTABLE_ASCIIS_WITHOUT_BLANK(e),
    re.match(_EMAIL_REG, e),
])

_CHECK_TEL = lambda tel: len(tel) == TEL_LEN and all(c.isnumeric() for c in tel)

CHECK_ACC = lambda acc: _CHECK_EMAIL(acc) if '@' in acc else _CHECK_TEL(acc)

CHECK_PWD = lambda pwd: all([
    6 <= len(pwd) <= MINI_MAX_LEN,
    _PRINTABLE_ASCIIS_WITHOUT_BLANK(pwd),
    any(c.isupper() for c in pwd)
    + any(c.islower() for c in pwd)
    + any(c.isnumeric() for c in pwd)
    + any(not c.isalnum() for c in pwd)
    >= 2
])
