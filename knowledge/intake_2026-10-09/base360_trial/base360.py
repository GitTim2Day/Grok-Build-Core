"""Exact base-360 positional conversion. Numeric digits are integers 0..359.
No binary floats. Exact source ratio is retained alongside any finite output.
"""
from fractions import Fraction


def integer(n,low,high,name):
    if type(n) is not int or not low<=n<=high:raise ValueError(name)


def encode(value,base=360,digits=12,accuracy=None):
    if not isinstance(value,Fraction):raise ValueError('Fraction required')
    integer(base,2,360,'base');integer(digits,0,1000,'digits')
    if accuracy is not None and (not isinstance(accuracy,Fraction) or accuracy<=0):
        raise ValueError('positive exact accuracy required')
    sign=-1 if value<0 else 1;n=abs(value.numerator);d=value.denominator
    whole,remainder=divmod(n,d);parts=[];scale=1
    # Stop before computing more digits if the supplied criterion already holds.
    while remainder and len(parts)<digits and (accuracy is None or Fraction(remainder,d*scale)>accuracy):
        digit,remainder=divmod(remainder*base,d)
        parts.append(digit);scale*=base
    record={'base':base,'sign':sign,'whole':whole,'digits':parts,
            'source_ratio':[value.numerator,d],'exact':remainder==0,
            'absolute_error':[remainder,d*scale],
            'accuracy_met':None if accuracy is None else Fraction(remainder,d*scale)<=accuracy}
    return record


def decode(record):
    base=record['base'];integer(base,2,360,'base')
    integer(record['sign'],-1,1,'sign')
    if record['sign']==0:raise ValueError('invalid sign')
    integer(record['whole'],0,10**1000,'whole')
    n=record['whole'];scale=1
    for digit in record['digits']:
        integer(digit,0,base-1,'digit');n=n*base+digit;scale*=base
    return record['sign']*Fraction(n,scale)


def terminating_digits(value,base=360):
    from math import gcd
    integer(base,2,360,'base');d=value.denominator;count=0
    while d!=1:
        common=gcd(d,base)
        if common==1:return None
        d//=common;count+=1
    return count


def format_digits(record):
    # Tokens avoid confusing one base-360 digit with one decimal character.
    prefix='-' if record['sign']<0 else ''
    tail=':'.join(f'{x:03d}' for x in record['digits'])
    return prefix+str(record['whole'])+(('.'+tail) if tail else '')


def guard_then_remove(value,places,base=360):
    integer(places,0,999,'places')
    r=encode(value,base,places+1)
    # Exact short outputs are padded solely for fixed-width presentation.
    tokens=[f'{x:03d}' for x in r['digits']]+['000']*(places+1-len(r['digits']))
    stored=':'.join(tokens[:-1])
    result=dict(r,digits=[int(t) for t in tokens[:-1]])
    output=decode(result)
    return {'stored_fractional_tokens':stored,'retained_ratio':[output.numerator,output.denominator],
            'exact_source_ratio':[value.numerator,value.denominator],
            'absolute_error':[(abs(value-output)).numerator,(abs(value-output)).denominator]}
