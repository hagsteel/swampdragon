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
