from decimal import Decimal
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


EMAIL_FILTER = re.compile(r'[^a-z0-9.@-]')
PHONE_FILTER = re.compile(r'[^+0-9]')
PHONE_VALIDATOR = re.compile(r'\+?\d{6,}')
PASSPORT_FILTER = re.compile(r'[^-A-Z0-9]')
STRIP_NON_NUMBERS = re.compile(r'[^0-9]')
IBAN_FILTER = re.compile(r'[^A-Z0-9]')
FI_SSN_FILTER = re.compile(r'[^-A-Z0-9]')
FI_SSN_VALIDATOR = re.compile(r'^\d{6}[+-A]\d{3}[\d\w]$')
FI_COMPANY_REG_ID_FILTER = re.compile(r'[^-0-9]')
SE_SSN_FILTER = re.compile(r'[^-0-9]')
SE_SSN_VALIDATOR = re.compile(r'^\d{6}[-]\d{3}[\d]$')


# ----------------------------------------------------------------
# Common
# ----------------------------------------------------------------


def phone_filter(v: str) -> str:
    return PHONE_FILTER.sub('', v)


def email_filter(v: str) -> str:
    return EMAIL_FILTER.sub('', str(v).lower())


def phone_validator(v: str):
    v = phone_filter(v)
    if not PHONE_VALIDATOR.fullmatch(v):
        raise ValidationError(_('Invalid phone number')+': {}'.format(v), code='invalid_phone')


def passport_filter(v: str) -> str:
    return PASSPORT_FILTER.sub('', v.upper())


def passport_validator(v: str):
    v = passport_filter(v)
    if len(v) < 5:
        raise ValidationError(_('Invalid passport number')+': {}'.format(v), code='invalid_passport')


def iban_filter(v: str) -> str:
    return IBAN_FILTER.sub('', v.upper())


def iban_filter_readable(acct) -> str:
    acct = iban_filter(acct)
    if acct:
        i = 0
        j = 4
        out = ''
        nlen = len(acct)
        while i < nlen:
            if out:
                out += ' '
            out += acct[i:j]
            i = j
            j += 4
        return out
    return acct


def validate_country_iban(v: str, country: str, length: int):
    v = iban_filter(v)
    if len(v) != length:
        raise ValidationError(_('Invalid IBAN account number') + ' ({}.1): {}'.format(country, v), code='invalid_iban')
    if v[0:2] != country:
        raise ValidationError(_('Invalid IBAN account number') + ' ({}.2): {}'.format(country, v), code='invalid_iban')
    digits = '0123456789'
    num = ''
    for ch in v[4:] + v[0:4]:
        if ch not in digits:
            ch = str(ord(ch) - ord('A') + 10)
        num += ch
    x = Decimal(num) % Decimal(97)
    if x != Decimal(1):
        raise ValidationError(_('Invalid IBAN account number') + ' ({}.3): {}'.format(country, v), code='invalid_iban')


# ----------------------------------------------------------------
# Finland
# ----------------------------------------------------------------


def fi_payment_reference_number(num: str):
    """
    Appends Finland reference number checksum to existing number.
    :param num: At least 3 digits
    :return: Number plus checksum
    """
    assert isinstance(num, str)
    assert len(num) >= 3
    weights = [7, 3, 1]
    weighed_sum = 0
    numlen = len(num)
    for j in range(numlen):
        weighed_sum += int(num[numlen - 1 - j]) * weights[j % 3]
    return num + str((10 - (weighed_sum % 10)) % 10)


def fi_iban_validator(v: str):
    validate_country_iban(v, 'FI', 18)


def fi_iban_bank_info(v: str) -> (str, str):
    """
    Returns BIC code and bank name from FI IBAN number.
    :param v: IBAN account number
    :return: (BIC code, bank name) or None if not found
    """
    from jutil.fi_bank_const import FI_BIC_BY_ACCOUNT_NUMBER, FI_BANK_NAME_BY_BIC
    v = iban_filter(v)
    bic = FI_BIC_BY_ACCOUNT_NUMBER.get(v[4:7], None)
    return (bic, FI_BANK_NAME_BY_BIC[bic]) if bic is not None else None


def fi_ssn_filter(v: str) -> str:
    return FI_SSN_FILTER.sub('', v.upper())


def fi_company_reg_id_filter(v: str) -> str:
    return FI_COMPANY_REG_ID_FILTER.sub('', v.upper())


def fi_company_reg_id_validator(v: str) -> str:
    v = fi_company_reg_id_filter(v)
    if v[-2:-1] != '-':
        raise ValidationError(_('Invalid company registration ID')+' (FI.1): {}'.format(v), code='invalid_company_reg_id')
    if len(v) != 9:
        raise ValidationError(_('Invalid company registration ID')+' (FI.2): {}'.format(v), code='invalid_company_reg_id')
    multipliers = (7, 9, 10, 5, 8, 4, 2)
    x = 0
    for i, m in enumerate(multipliers):
        x += int(v[i]) * m
    quotient, remainder = divmod(x, 11)
    if remainder == 1:
        raise ValidationError(_('Invalid company registration ID')+' (FI.3): {}'.format(v), code='invalid_company_reg_id')
    check_digit = str(11 - remainder)
    if check_digit != v[-1:]:
        raise ValidationError(_('Invalid company registration ID')+' (FI.4): {}'.format(v), code='invalid_company_reg_id')


def fi_ssn_validator(v: str):
    v = fi_ssn_filter(v)
    if not FI_SSN_VALIDATOR.fullmatch(v):
        raise ValidationError(_('Invalid personal identification number')+' (FI.1): {}'.format(v), code='invalid_ssn')
    d = int(Decimal(v[0:6] + v[7:10]) % Decimal(31))
    digits = {
        10: 'A', 	11: 'B', 	12: 'C', 	13: 'D', 	14: 'E', 	15: 'F', 	16: 'H',
        17: 'J', 	18: 'K', 	19: 'L', 	20: 'M', 	21: 'N', 	22: 'P', 	23: 'R',
        24: 'S', 	25: 'T', 	26: 'U', 	27: 'V', 	28: 'W', 	29: 'X', 	30: 'Y',
    }
    ch = str(d)
    if d in digits:
        ch = digits[d]
    if ch != v[-1:]:
        raise ValidationError(_('Invalid personal identification number')+' (FI.2): {}'.format(v), code='invalid_ssn')


# ----------------------------------------------------------------
# Sweden
# ----------------------------------------------------------------


def se_iban_validator(v: str):
    validate_country_iban(v, 'SE', 24)


def se_ssn_filter(v: str) -> str:
    return SE_SSN_FILTER.sub('', v.upper())


def se_ssn_validator(v: str):
    v = se_ssn_filter(v)
    if not SE_SSN_VALIDATOR.fullmatch(v):
        raise ValidationError(_('Invalid personal identification number')+' (SE.1): {}'.format(v), code='invalid_ssn')
    v = STRIP_NON_NUMBERS.sub('', v)
    dsum = 0
    for i in range(9):
        x = int(v[i])
        if i & 1 == 0:
            x += x
        # print('summing', v[i], 'as', x)
        xsum = x % 10 + int(x/10) % 10
        # print(v[i], 'xsum', xsum)
        dsum += xsum
    # print('sum', dsum)
    rem = dsum % 10
    # print('rem', rem)
    checksum = 10 - rem
    if checksum == 10:
        checksum = 0
    # print('checksum', checksum)
    if int(v[-1:]) != checksum:
        raise ValidationError(_('Invalid personal identification number')+' (SE.2): {}'.format(v), code='invalid_ssn')
