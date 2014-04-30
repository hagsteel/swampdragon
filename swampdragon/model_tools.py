def get_property(obj, field):
    field = field.replace('__', '.')
    if '.' in field:
        attr_chain = field.split('.')
        attr = obj
        for elem in attr_chain:
            try:
                attr = getattr(attr, elem, None)
            except:
                return None
        return attr
    try:
        return getattr(obj, field, None)
    except:
        return None


def string_to_list(val):
    return val.replace('[','').replace(']','').split(',')
