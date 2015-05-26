from django.db.models.fields.related import ReverseSingleRelatedObjectDescriptor, SingleRelatedObjectDescriptor, \
    ForeignRelatedObjectsDescriptor, ManyRelatedObjectsDescriptor, ReverseManyRelatedObjectsDescriptor


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

        field_type = getattr(serializer_instance.opts.model, field_name)
        is_fk = isinstance(field_type, ReverseSingleRelatedObjectDescriptor)
        is_o2o = isinstance(field_type, SingleRelatedObjectDescriptor)
        is_reverse_fk = isinstance(field_type, ForeignRelatedObjectsDescriptor)
        is_m2m = isinstance(field_type, ManyRelatedObjectsDescriptor)
        is_reverse_m2m = isinstance(field_type, ReverseManyRelatedObjectsDescriptor)

        if is_fk:
            # Django 1.8:
            # the related.parent_model is related.model in Django 1.8
            if hasattr(field_type.field.related, 'parent_model'):
                model = field_type.field.related.parent_model
            else:
                model = field_type.field.related.model
            is_collection = False

            if hasattr(field_type.field.related, 'var_name'):
                attname = field_type.field.related.var_name
            else:
                attname = field_type.field.rel.name

        if is_o2o:
            # Django 1.8:
            # the related.model is related.related_model in Django 1.8
            if hasattr(field_type.related, 'related_model'):
                model = field_type.related.related_model
            else:
                model = field_type.related.model
            is_collection = False
            attname = field_type.related.field.name

        if is_reverse_fk:
            # Django 1.8:
            # the related.model is related.related_model in Django 1.8
            if hasattr(field_type.related, 'related_model'):
                model = field_type.related.related_model
            else:
                model = field_type.related.model
            is_collection = True
            attname = field_type.related.field.name

        if is_m2m:
            # Django 1.8:
            # the related.model is related.related_model in Django 1.8
            if hasattr(field_type.related, 'related_model'):
                model = field_type.related.related_model
            else:
                model = field_type.related.model
            is_collection = True
            attname = field_type.related.field.name

        if is_reverse_m2m:
            # Django 1.8:
            # the related.parent_model is related.model in Django 1.8
            if hasattr(field_type.field.related, 'parent_model'):
                model = field_type.field.related.parent_model
            else:
                model = field_type.field.related.model
            is_collection = True

            if hasattr(field_type.field.related, 'var_name'):
                attname = field_type.field.related.var_name
            else:
                attname = field_type.field.rel.name

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
