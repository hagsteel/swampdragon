from django.db.models.signals import pre_delete, m2m_changed
from django.dispatch.dispatcher import receiver
from .pubsub_providers.base_provider import PUBACTIONS
from .model_tools import get_property, get_field_from_m2m_model_by_model
from .pubsub_providers.model_publisher import publish_model
from .serializers.serializer_importer import get_serializer


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
        # update_fields = list(self._serializer.opts.update_fields)
        # publish_fields = list(self._serializer.opts.publish_fields)
        # relevant_fields = set(update_fields + publish_fields)
        relevant_fields = self._serializer.base_fields

        if 'id' in relevant_fields:
            relevant_fields.remove('id')

        return relevant_fields

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


@receiver(m2m_changed)
def _self_publish_model_m2m_change(sender, instance, action, model, pk_set, **kwargs):
    if not isinstance(instance, SelfPublishModel):
        return

    instance.action = PUBACTIONS.updated
    if action is 'post_clear':
        print('post clear')
        instance.changed_fields = instance.get_changed_fields()
        instance._publish(instance.action, instance.changed_fields)

    if action is 'post_add':
        related_instances = model.objects.filter(pk__in=pk_set)
        for ri in related_instances:
            ri._publish(PUBACTIONS.updated, ri._serializer.opts.publish_fields)

    if action is 'post_remove':
        field_name = get_field_from_m2m_model_by_model(instance, model)
        instance.changed_fields = [field_name]
        instance._publish(instance.action, instance.changed_fields)


@receiver(pre_delete)
def _self_publish_model_delete(sender, instance, **kwargs):
    if isinstance(instance, SelfPublishModel):
        instance._publish(PUBACTIONS.deleted)
