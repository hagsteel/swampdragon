def _construct_graph(parent_type, child_type, via, is_collection, property_name):
    return {
        'parent_type': parent_type,
        'child_type': child_type,
        'via': via,
        'prop_name': property_name,
        'is_collection': is_collection,
    }


def _serializer_is_ignored(serializer, related_serializer, ignore_serializer_pairs):
    if not ignore_serializer_pairs:
        return False
    if (serializer, related_serializer) in ignore_serializer_pairs:
        return True
    return False


def get_object_map(serializer, ignore_serializer_pairs=None):
    """
    Create an object map from the serializer and it's related serializers.

    For each map created, ignore the pair of serializers that are already mapped
    """
    graph = []
    serializer_instance = serializer()
    if ignore_serializer_pairs is None:
        ignore_serializer_pairs = []

    serializers = serializer.get_related_serializers()

    for related_serializer, field_name in serializers:
        if _serializer_is_ignored(serializer, related_serializer, ignore_serializer_pairs):
            continue

        field = getattr(serializer_instance.opts.model, field_name)
        if hasattr(field, 'related'):
            model = field.related.model
            attname = '{}_id'.format(field.related.field.name)
            is_collection = True
        else:
            model = field.field.related.parent_model
            attname = '{}_id'.format(field.field.related.var_name)
            is_collection = False
        graph.append(
            _construct_graph(
                serializer_instance.opts.model._meta.model_name,
                model._meta.model_name,
                attname,
                is_collection,
                field_name
            )
        )
        ignore_serializer_pairs.append((serializer, related_serializer))
        graph += get_object_map(related_serializer, ignore_serializer_pairs)
    return graph
