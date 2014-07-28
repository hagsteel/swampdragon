from django.db.models import OneToOneField


def _construct_graph(parent_type, child_type, via, is_collection, property_name):
    return {
        'parent_type': parent_type,
        'child_type': child_type,
        'via': via,
        'prop_name': property_name,
        'is_collection': is_collection,
    }


def _get_serializers(serializer, ignore_serializers=None):
    if not ignore_serializers:
        ignore_serializers = []
    serializers = []
    possible_serializers = [k for k in serializer.__dict__.keys() if not k.startswith('_') and not k == 'Meta']
    for attrib in possible_serializers:
        val = getattr(serializer, attrib)
        if hasattr(val, 'serialize') and val not in ignore_serializers:
            serializers.append((val, attrib))
    return serializers


def get_object_map(serializer, include_serializers=None, ignore_serializers=None):
    graph = []
    serializer_instance = serializer()
    m2m_fields = serializer_instance.m2m_fields
    related_fields = serializer_instance.related_fields

    serializers = _get_serializers(serializer, [serializer])
    for related_serializer, field_name in serializers:
        field = getattr(serializer_instance.opts.model, field_name)
        if hasattr(field, 'related'):
            model = field.related.model
            attname = '{}_id'.format(field.related.field.name)
        else:
            model = field.field.related.parent_model
            attname = '{}_id'.format(field.field.related.var_name)
        if ignore_serializers and model in [s._model() for s in ignore_serializers]:
            continue
        graph.append(
            _construct_graph(
                serializer_instance.opts.model._meta.model_name,
                model._meta.model_name,
                attname,
                True,
                field_name
            )
        )
    import ipdb;ipdb.set_trace()

    # for field_name in m2m_fields:
    #     field = getattr(serializer_instance.opts.model, field_name)
    #
    #     if hasattr(field, 'related'):
    #         model = field.related.model
    #         attname = '{}_id'.format(field.related.field.name)
    #     else:
    #         model = field.field.related.parent_model
    #         attname = '{}_id'.format(field.field.related.var_name)
    #     if ignore_serializers and model in [s._model() for s in ignore_serializers]:
    #         continue
    #     graph.append(
    #         _construct_graph(
    #             serializer_instance.opts.model._meta.model_name,
    #             model._meta.model_name,
    #             attname,
    #             True,
    #             field_name
    #         )
    #     )

    for field_name in related_fields:
        field = getattr(serializer_instance.opts.model, field_name)

        is_collection = True
        model = None
        attname = None
        if hasattr(field, 'related'):
            model = field.related.model
            attname = field.related.field.attname
            is_collection = isinstance(field.related.field, OneToOneField) is False
        elif hasattr(field, 'field'):
            model = field.field.related.parent_model
            attname = '{}_id'.format(field.field.related.var_name)
        if ignore_serializers and model in [s._model() for s in ignore_serializers]:
            continue
        graph.append(_construct_graph(
            serializer_instance.opts.model._meta.model_name,
            model._meta.model_name,
            attname,
            is_collection,
            field_name
        ))

    include_serializers = _get_serializers(serializer)

    if include_serializers:
        for s in include_serializers:
            if ignore_serializers and s in ignore_serializers:
                continue
            graph += s.get_object_map(ignore_serializers=[serializer])
    return graph
