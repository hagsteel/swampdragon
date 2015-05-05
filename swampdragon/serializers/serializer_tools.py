from collections import namedtuple
from django.db.models.fields.related import ForeignKey, ReverseSingleRelatedObjectDescriptor, \
    ManyRelatedObjectsDescriptor, ReverseManyRelatedObjectsDescriptor, ForeignRelatedObjectsDescriptor, \
    SingleRelatedObjectDescriptor
# from django.db.models.related import RelatedObject
from django.db.models.fields.related import ForeignObjectRel
from django.db.models.fields.related import ManyToManyField


class FieldType(namedtuple('FieldType', 'field, model, fk, m2m')):
    '''
    Determine if a field is an m2m, reverse m2m, fk or reverse fk
    '''
    @property
    def is_m2m(self):
        return self.fk is False and self.m2m is True and isinstance(self.field, ForeignObjectRel)

    @property
    def is_reverse_m2m(self):
        return self.fk is True and self.m2m is True and isinstance(self.field, ManyToManyField)

    @property
    def is_fk(self):
        return self.fk is True and self.m2m is False and isinstance(self.field, ForeignKey)

    @property
    def is_reverse_fk(self):
        return self.fk is False and self.m2m is False and isinstance(self.field, ForeignObjectRel)


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

        serializable_field = serializer._get_related_serializer(field_name)
        if not hasattr(serializable_field, 'serialize'):
            continue

        field_type = getattr(serializer.opts.model, field_name)
        is_fk = isinstance(field_type, ReverseSingleRelatedObjectDescriptor)
        is_o2o = isinstance(field_type, SingleRelatedObjectDescriptor)
        is_reverse_fk = isinstance(field_type, ForeignRelatedObjectsDescriptor)
        is_m2m = isinstance(field_type, ManyRelatedObjectsDescriptor)
        is_reverse_m2m = isinstance(field_type, ReverseManyRelatedObjectsDescriptor)

        try:
            val = getattr(serializer.instance, field_name)
        except:
            continue

        if not val:
            continue

        if is_fk or is_o2o:
            data['{}'.format(field_name)] = val.pk
            continue

        if is_reverse_fk or is_m2m or is_reverse_m2m:
            data['{}'.format(field_name)] = list(val.all().values_list('pk', flat=True))
            continue

    return data
