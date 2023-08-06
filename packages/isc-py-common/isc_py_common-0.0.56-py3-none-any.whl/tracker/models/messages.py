import datetime
import hashlib
import logging

from django.db import transaction
from django.db.models import DateTimeField, UUIDField, CharField
from django.forms import model_to_dict
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from isc_common import setAttr, getAttr, delAttr
from isc_common.auth.models.user import User
from isc_common.fields.description_field import DescriptionField
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_tree_grid_manager import CommonTreeGridManager
from isc_common.models.audit import AuditQuerySet
from isc_common.models.base_ref import Hierarcy
from tracker.models.messages_state import Messages_state
from tracker.models.messages_theme import Messages_theme

logger = logging.getLogger(__name__)


class MessagesQuerySet(AuditQuerySet):

    def create(self, **kwargs):
        # setAttr(kwargs, 'message', f'<pre>{kwargs.get("message")}</pre>')
        setAttr(kwargs, 'checksum', hashlib.md5(kwargs.get('message').encode()).hexdigest())
        return super().create(**kwargs)

    def update(self, **kwargs):
        # setAttr(kwargs, 'message', f'<pre>{kwargs.get("message").replace("<pre>", "").replace("</pre>", "")}</pre>')
        setAttr(kwargs, 'checksum', hashlib.md5(kwargs.get('message').encode()).hexdigest())
        return super().update(**kwargs)

    def delete(self):
        from tracker.models.messages_files_refs import Messages_files_refs
        from tracker.models.messages_files import Messages_files

        with transaction.atomic():
            for message in self:
                for messages_files_refs in Messages_files_refs.objects.filter(message_id=message.id):
                    if Messages_files_refs.objects.filter(messages_file=messages_files_refs.messages_file).count() == 1:
                        id = messages_files_refs.messages_file.id
                        messages_files_refs.delete()
                        Messages_files.objects.filter(id=id).delete()
                    else:
                        messages_files_refs.delete()

                return super().delete()


class MessagesManager(CommonTreeGridManager):

    @staticmethod
    def getRecord(record):
        res = {
            # "date_create": record.date_create.strftime('%d.%m.%Y, %H:%M:%S'),
            "date_create": record.date_create,
            "deliting": record.deliting,
            "editing": record.editing,
            "guid": str(record.guid).upper(),
            "id": record.id,
            "lastmodified": record.lastmodified,
            "message": record.message,
            "parent_id": record.parent_id,
            "state__name": record.state.name,
            "state_id": record.state.id,
            "theme__full_name": record.theme.full_name,
            "theme__name": record.theme.name,
            "theme_id": record.theme.id,
            "to_whom__short_name": record.to_whom.get_short_name,
            "to_whom__username": record.to_whom.username,
            "to_whom_id": record.to_whom.id,
            "user__color": record.user.color if record.user.color != None and record.user.color != 'undefined' else 'black',
            "user__short_name": record.user.get_short_name,
            "user__full_name": record.user.get_full_name,
            "user_id": record.user.id if record.user else None,
        }
        return res

    def get_queryset(self):
        return MessagesQuerySet(self.model, using=self._db)

    def createAutoErrorFromRequest(self, request, printRequest=False, function=None):
        request = DSRequest(request=request)
        data = request.get_data()
        setAttr(data, 'state', Messages_state.objects.get(code="new"))
        setAttr(data, 'theme', Messages_theme.objects.get(code="auto_from_error"))
        setAttr(data, 'to_whom', User.objects.get(username="developer"))
        message = getAttr(data, 'message', None)
        user_id = getAttr(data, 'user_id', None)
        setAttr(data, 'user', User.objects.get(id=user_id))

        if message and isinstance(message, list):
            message = '\n'.join(message)
            setAttr(data, 'message', message)
        return super().create(**data)

    def createFromRequest(self, request, printRequest=False, function=None):
        request = DSRequest(request=request)
        data = request.get_data()
        data_clone = data.copy()
        delAttr(data_clone, 'user__username')
        delAttr(data_clone, 'state__name')
        delAttr(data_clone, 'theme__full_name')
        delAttr(data_clone, 'theme__name')
        delAttr(data_clone, 'isFolder')
        delAttr(data_clone, 'to_whom__username')
        delAttr(data_clone, 'user__short_name')
        delAttr(data_clone, 'to_whom__short_name')
        message = super().create(**data_clone)

        res = model_to_dict(message)
        setAttr(data, 'isFolder', False)
        setAttr(data, 'user__short_name', message.user.get_short_name)
        setAttr(data, 'to_whom__short_name', message.to_whom.get_short_name)
        data.update(res)
        return data

    def updateFromRequest(self, request, printRequest=False):
        request = DSRequest(request=request)
        data = request.get_data()
        data_clone = data.copy()
        delAttr(data_clone, 'user__username')
        delAttr(data_clone, 'to_whom__short_name')

        delAttr(data_clone, 'state__name')

        delAttr(data_clone, 'theme__full_name')
        delAttr(data_clone, 'theme__name')

        delAttr(data_clone, 'id')
        delAttr(data_clone, 'isFolder')
        delAttr(data_clone, 'parent')
        id = request.get_id()
        super().update_or_create(
            id=id,
            defaults=dict(
                message=data_clone.get('message'),
                to_whom_id=data_clone.get('to_whom_id'),
                state_id=data_clone.get('state_id'),
            ))

        return data


class Messages(Hierarcy):
    checksum = CharField(max_length=255)
    guid = UUIDField(blank=True, null=True)
    message = DescriptionField(null=False, blank=False)
    date_create = DateTimeField(verbose_name='Дата записи', db_index=True, default=timezone.now)
    user = ForeignKeyCascade(User, related_name='user_msg_user')
    theme = ForeignKeyProtect(Messages_theme)
    state = ForeignKeyCascade(Messages_state)
    to_whom = ForeignKeyCascade(User, related_name='user_msg_to_whom')

    def __str__(self):
        return f'id: {self.id}, guid: {str(self.guid).upper()}, message: {self.message}, date_create: {self.date_create}, user: [{self.user}], theme: [{self.theme}], state: [{self.state}]'

    objects = MessagesManager()

    class Meta:
        verbose_name = 'Сообщения'
        unique_together = (('guid', 'theme', 'state', 'checksum', 'user', 'to_whom'),)
        ordering = ('date_create',)
