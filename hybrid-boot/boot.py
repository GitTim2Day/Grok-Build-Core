"""Hybrid boot. No floats. Digit strings only. Truncate, never round."""

SKILL = "shared-library"
MEM = "seat-memory-plus-shared-user"
NUMMODE = "string-then-convert"


def load():
    return {"skill": SKILL, "mem": MEM, "nummode": NUMMODE}


def trunc_div(numer: str, denom: str) -> str:
    if any(c in numer + denom for c in ".eE"):
        raise ValueError("float refused")
    n = int(numer)
    d = int(denom)
    if d == 0:
        raise ValueError("divide by zero refused")
    # Toward zero. Python // floors, so do not use it on a negative pair.
    q = abs(n) // abs(d)
    if (n < 0) != (d < 0):
        q = -q
    return str(q)



def cut_decimal(value: str) -> str:
    """Drop the far-right decimal place. Digit string only. No float."""
    if any(c in value for c in "eE"):
        raise ValueError("exponent token refused; pass a fixed digit string")
    sign = ""
    body = value
    if body.startswith("-"):
        sign, body = "-", body[1:]
    if "." not in body:
        raise ValueError("no decimal place to cut")
    whole, frac = body.split(".", 1)
    if not whole.isdigit() or not frac.isdigit() or len(frac) < 1:
        raise ValueError("need a digit string with a decimal place")
    if len(frac) == 1:
        raise ValueError("last decimal place refused; would store an empty fraction")
    return sign + whole + "." + frac[:-1]


def recheck(state: dict) -> dict:
    if state.get("skill") != SKILL or state.get("nummode") != NUMMODE:
        return load()
    return state


def run():
    state = load()
    state = recheck(state)
    return state


if __name__ == "__main__":
    print(run())
