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
    for f, ignore in instance._meta.get_all_related_m2m_objects_with_model():
        if f.model == model:
            return f.get_accessor_name()

    for f in instance._meta.get_all_field_names():
        try:
            field = instance._meta.get_field_by_name(f)[0]
            if hasattr(field, 'get_accessor_name'):
                name = field.get_accessor_name()
            else:
                name = field.name
            if get_m2m_model_from_field_name(instance, name):
                return name
        except:
            continue
    return None