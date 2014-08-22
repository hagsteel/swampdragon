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


def get_m2m_model_from_field_name(instance, field_name):
    try:
        return getattr(instance, field_name).model
    except:
        return None


def get_field_from_m2m_model_by_model(instance, model):
    """
    Provided an instance and a model, find the
    field name on the instance, where it has an m2m relationship
    to the model
    """
    for field in instance._meta.get_all_field_names():
        if get_m2m_model_from_field_name(instance, field):
            return field
    return None