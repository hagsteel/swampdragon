from django.db.models.loading import get_model as get_django_model


def get_property(obj, field):
    field = field.replace('__', '.')
    if '.' in field:
        attr_chain = field.split('.')
        attr = obj
        for elem in attr_chain:
            attr = getattr(attr, elem, None)
            if attr is None:
                return None
        return attr
    try:
        return getattr(obj, field, None)
    except:
        return None


def string_to_list(val):
    return val.replace('[', '').replace(']', '').split(',')


def get_model(model):

    if isinstance(model, str):
        return get_django_model(*model.split('.', 1))
    return model
