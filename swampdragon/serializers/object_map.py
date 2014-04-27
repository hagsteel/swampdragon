from django.db.models import OneToOneField


def _construct_graph(parent_type, child_type, via, is_collection, property_name):
    return {
        'parent_type': parent_type,
        'child_type': child_type,
        'via': via,
        'prop_name': property_name,
        'is_collection': is_collection,
    }


def get_object_map(cls, include_serializers=None, ignore_serializers=None):
        graph = []
        serializer_instance = cls()
        m2m_fields = cls._get_publish_m2m_fields()
        related_fields = cls.get_related_fields()

        for field_name in m2m_fields:
            field = getattr(cls._model(), field_name)

            if hasattr(field, 'related'):
                model = field.related.model
                attname = '{}_id'.format(field.related.field.name)
            else:
                model = field.field.related.parent_model
                attname = '{}_id'.format(field.field.related.var_name)
            if ignore_serializers and model in [s._model() for s in ignore_serializers]:
                continue
            graph.append(_construct_graph(serializer_instance._get_type_name(), model._meta.model_name, attname, True, field_name))

        for field_name in related_fields:
            if field_name in m2m_fields:
                continue
            field = getattr(cls._model(), field_name)

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
                serializer_instance._get_type_name(),
                model._meta.model_name,
                attname,
                is_collection,
                field_name
            ))

        if include_serializers:
            for s in include_serializers:
                if ignore_serializers and s in ignore_serializers:
                    continue
                graph += s.get_object_map(ignore_serializers=[cls])
        return graph
