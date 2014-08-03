from collections import namedtuple
from django.db.models.fields.related import ForeignKey
from django.db.models.related import RelatedObject
from django.db.models.fields.related import ManyToManyField


class FieldType(namedtuple('FieldType', 'field, model, fk, m2m')):
    '''
    Determine if a field is an m2m, reverse m2m, fk or reverse fk
    '''
    @property
    def is_m2m(self):
        return self.fk is False and self.m2m is True and isinstance(self.field, RelatedObject)

    @property
    def is_reverse_m2m(self):
        return self.fk is True and self.m2m is True and isinstance(self.field, ManyToManyField)

    @property
    def is_fk(self):
        return self.fk is True and self.m2m is False and isinstance(self.field, ForeignKey)

    @property
    def is_reverse_fk(self):
        return self.fk is False and self.m2m is False and isinstance(self.field, RelatedObject)


def get_serializer_relationship_field(serializer, related_serializer):
    if isinstance(serializer, type):
        model = serializer().opts.model
    else:
        model = serializer.opts.model
    if isinstance(related_serializer, type):
        related_model = related_serializer().opts.model
    else:
        related_model = related_serializer.opts.model

    for field_name in related_model._meta.get_all_field_names():
        field_type = FieldType(*related_model._meta.get_field_by_name(field_name))
        field = field_type.field

        # Foreign key
        if field_type.is_fk and field.rel.to is model:
            return field.verbose_name

        # Reverse foreign key
        if field_type.is_reverse_fk and field.model is model:
            return field.var_name

        # M2m fields
        if field_type.is_m2m and field.model is model:
            return field.var_name

        # Reverse m2m field
        if field_type.is_reverse_m2m and field.rel.to is model:
            return field.attname


def get_id_mappings(serializer):
    if not serializer.instance:
        return {}

    data = {}
    for field_name in serializer.opts.publish_fields:
        if not hasattr(serializer, field_name):
            continue
        serializable_field = getattr(serializer, field_name)
        if not hasattr(serializable_field, 'serialize'):
            continue

        field_type = FieldType(*serializer.opts.model._meta.get_field_by_name(field_name))
        field = field_type.field

        if field_type.is_fk:
            val = getattr(serializer.instance, field_name)
            if val:
                data['{}_id'.format(field.verbose_name)] = [val.pk]

        if field_type.is_reverse_fk:
            # Check if this is a one 2 one field first
            try:
                val = getattr(serializer.instance, field_name)
            except field.model.DoesNotExist:
                continue

            if hasattr(val, 'all'):
                qs = val.all()
                data['{}_id'.format(field.var_name)] = [v[0] for v in qs.values_list('pk')]

        if field_type.is_m2m:
            qs = getattr(serializer.instance, field_name).all()
            data['{}_id'.format(field.var_name)] = [v[0] for v in qs.values_list('pk')]

        if field_type.is_reverse_m2m:
            qs = getattr(serializer.instance, field_name).all()
            data['{}_id'.format(field.attname)] = [v[0] for v in qs.values_list('pk')]

    return data
