import uuid

from django.contrib.postgres.indexes import GinIndex
from django.db import models, connection
from django.db.models.signals import pre_save
from django.dispatch import receiver


def get_next_internal_id():
    with connection.cursor() as cursor:
        cursor.execute("CREATE SEQUENCE IF NOT EXISTS chats_internal_id_seq START WITH 1 INCREMENT BY 1")
        cursor.execute("SELECT nextval('chats_internal_id_seq')")
        result = cursor.fetchone()
        return result[0]


def meta_default_value(internal_id_placeholder=None):
    return {"status": "active", "flags": 0, "internal_id": internal_id_placeholder}


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    project_id = models.UUIDField(default=None, null=True)
    account_id = models.UUIDField(default=None, null=True)
    user_id = models.UUIDField(default=None, null=True)
    object_type = models.CharField(max_length=254, null=True)
    object_item = models.UUIDField(default=None, null=True)  # e.g. attachment to a Task object
    object_code = models.CharField(max_length=254, null=True, unique=True)  # e.g. phone # or email for a contact
    name = models.CharField(max_length=254, null=True)
    meta = models.JSONField(default=meta_default_value)
    data = models.JSONField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["data"], name="chats_data_gin"),
            models.Index(fields=["object_item"], name="chats_object_item_idx"),
            models.Index(fields=["created_date"], name="chats_cr_date_idx"),
            models.Index(fields=["modified_date"], name="chats_mod_date_idx"),
            models.Index(fields=["object_item", "object_type"], name="chats_o_item_type_idx"),
            models.Index(fields=["project_id", "account_id", "user_id"], name="chats_p_a_u_ids_idx"),
            models.Index(fields=["account_id", "user_id"], name="chats_a_u_ids_idx"),
            models.Index(fields=["user_id"], name="chats_user_id_idx"),
        ]
        ordering = ["-meta__internal_id"]


@receiver(pre_save, sender=Chat)
def set_meta(sender, instance, **kwargs):
    try:
        Chat.objects.get(id=instance.id)
    except Chat.DoesNotExist:
        if "status" not in instance.meta.keys():
            instance.meta["status"] = "active"
        if "flags" not in instance.meta.keys():
            instance.meta["flags"] = 0
        instance.meta["internal_id"] = get_next_internal_id()
