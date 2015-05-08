from django.db.models import ForeignKey
from .pubsub_providers.base_provider import PUBACTIONS
from .model_tools import get_property
from .pubsub_providers.model_publisher import publish_model
from .serializers.serializer_importer import get_serializer
from django.db.models.signals import pre_delete, m2m_changed
from django.dispatch.dispatcher import receiver


class SelfPublishModel(object):
    serializer_class = None

    def __init__(self, *args, **kwargs):
        if isinstance(self.serializer_class, str):
            self.serializer_class = get_serializer(self.serializer_class, self)
        self._pre_save_state = dict()
        super(SelfPublishModel, self).__init__(*args, **kwargs)
        self._serializer = self.serializer_class(instance=self)
        self._set_pre_save_state()

    def _set_pre_save_state(self):
        """
        Set the state of the model before any changes are done,
        so it's possible to determine what fields have changed.
        """
        relevant_fields = self._get_relevant_fields()
        for field in relevant_fields:
            val = get_property(self, field)
            if hasattr(self._serializer, field):
                continue
            if val is None:
                self._pre_save_state[field] = None
                continue
            self._pre_save_state[field] = val

    def _get_relevant_fields(self):
        """
        Get all fields that will affect the state.
        This is used to save the state of the model before it's updated,
        to be able to get changes used when publishing an update (so not all fields are published)
        """
        relevant_fields = self._serializer.base_fields

        if 'id' in relevant_fields:
            relevant_fields.remove('id')

        relevant_fields_copy = []

        # check for any foreign keys and include the key to the object instead of the object itself
        # This is to avoid triggering queries to retrieve the foreign object
        for field in self._meta.fields:
            if field.name in relevant_fields:
                if type(field) in (ForeignKey, ):
                    # typically field.attname is field.name + "_id" ie field_id
                    relevant_fields_copy.append(field.attname)
                else:
                    relevant_fields_copy.append(field.name)

        return relevant_fields_copy

        # for field_name in relevant_fields:
        #     field = self._meta.get_field_by_name(field_name)[0]
        #     if isinstance(field, ForeignKey):
        #         relevant_fields.remove(field_name)
        #
        # return relevant_fields

    def get_changed_fields(self):
        changed_fields = []
        for k, v in self._pre_save_state.items():
            val = get_property(self, k)
            if val != v:
                changed_fields.append(k)
        return changed_fields

    def serialize(self):
        return self._serializer.serialize()

    def _publish(self, action, changed_fields=None):
        publish_model(self, self._serializer, action, changed_fields)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.action = PUBACTIONS.created
            self.changed_fields = None
        else:
            self.action = PUBACTIONS.updated
            self.changed_fields = self.get_changed_fields()
        super(SelfPublishModel, self).save(*args, **kwargs)
        self._publish(self.action, self.changed_fields)

        # Set the pre-save state to the current state
        # in case the model is changed again before retrieval
        self._set_pre_save_state()


@receiver(m2m_changed)
def _self_publish_model_m2m_change(sender, instance, action, model, pk_set, **kwargs):
    if not isinstance(instance, SelfPublishModel):
        return
    instance.action = PUBACTIONS.updated
    if action in ['post_add', 'post_clear', 'post_remove']:
        instance._publish(instance.action, instance._serializer.opts.publish_fields)


@receiver(pre_delete)
def _self_publish_model_delete(sender, instance, **kwargs):
    if isinstance(instance, SelfPublishModel):
        instance._publish(PUBACTIONS.deleted)
