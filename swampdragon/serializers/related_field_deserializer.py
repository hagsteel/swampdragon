

def deserialize_related(serializer, model_instance, key, val):
    ser = getattr(serializer, '{}_serializer'.format(key))()
    if isinstance(val, list):
        for v in val:
            child = ser.deserialize(**v)
            getattr(model_instance, key).add(child)
