import pandas_ta as ta


def ema_cross_above(data, fast, slow):
    """Checks when the fast crosses slow from below to above"""
    cross = ta.cross(data[f"EMA_{fast}"], data[f"EMA_{slow}"], above=True, equal=False)
    return cross.iloc[-2] == 1


def ema_cross_below(data, fast, slow):
    """Checks when the fast crosses slow from above to below"""
    cross = ta.cross(data[f"EMA_{fast}"], data[f"EMA_{slow}"], above=False, equal=False)
    return cross.iloc[-2] == 1