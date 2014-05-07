try:
    from urllib.parse import quote_plus, unquote_plus
except ImportError:
    from urllib import quote_plus, unquote_plus


def term_match_check(term, val, option):
    decoded_val = unquote_plus(val)
    comparer = term_comparison_factory(option)
    return comparer(decoded_val, term)


def standard_compare(term, val):
    if val is None:
        return term is val
    term = type(val)(term)
    return term == (val)


def contains_compare(term, val):
    return term in val


def in_compare(term, val):
    if not val or not term:
        return False
    return val in [type(val)(t) for t in term]


def lt_compare(term, val):
    term = type(val)(term)
    return val < term


def lte_compare(term, val):
    term = type(val)(term)
    return val <= term


def gt_compare(term, val):
    term = type(val)(term)
    return val > term


def gte_compare(term, val):
    term = type(val)(term)
    return val >= term


filter_options = {
    'contains': contains_compare,
    'lt': lt_compare,
    'lte': lte_compare,
    'gt': gt_compare,
    'gte': gte_compare,
    'eq': standard_compare,
    'in': in_compare,
}


def term_comparison_factory(option):
    if option is None:
        return standard_compare
    return filter_options.get(option)
