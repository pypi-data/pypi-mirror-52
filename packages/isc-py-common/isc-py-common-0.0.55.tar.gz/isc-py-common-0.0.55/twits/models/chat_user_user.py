import logging

from bitfield import BitField
from django.db import transaction
from django.db.models import PositiveIntegerField
from django.forms import model_to_dict

from isc_common import setAttr, ws
from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.ws.webSocket import WebSocket
from tracker.models.messages_theme import Messages_theme

logger = logging.getLogger(__name__)


class Chat_user_userQuerySet(AuditQuerySet):
    def create(self, **kwargs):
        from twits.models.chat_user_user_theme import Chat_user_user_theme

        user_sender = User.objects.get(id=kwargs.get('user_sender_id'))
        user_reciver = User.objects.get(id=kwargs.get('user_reciver_id'))

        if user_sender.id == user_reciver.id:
            raise Exception(f'Чат с самим собою не допускается.')

        try:
            common_id = self.model.objects.get(user_sender=user_reciver, user_reciver=user_sender).common_id
        except self.model.DoesNotExist:
            common_id = user_sender.id + user_reciver.id + 10000000

        setAttr(kwargs, 'common_id', common_id)

        with transaction.atomic():
            theme, created = Messages_theme.objects.get_or_create(
                code=f'tetatet_{user_sender.get_short_name}_{user_reciver.get_short_name}',
                defaults=dict(
                    name=f'Чат: {user_sender.get_short_name} : {user_reciver.get_short_name}',
                    creator=User.admin_user(),
                    editing=False,
                    deliting=False,
                    parent=Messages_theme.tetatet_chats_theme(),
                    description='Группа создана автоматически'))

            chat_user_user = super().create(**kwargs)
            Chat_user_user_theme.objects.get_or_create(theme=theme, chat_user_user=chat_user_user)
        return chat_user_user

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Chat_user_userManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'common_id': record.common_id,
            'user_sender_id': record.user_sender.id,
            'user_reciver_id': record.user_reciver.id,
            'user_reciver__username': record.user_reciver.username,
            'user_reciver__first_name': record.user_reciver.first_name,
            'user_reciver__last_name': record.user_reciver.last_name,
            'user_reciver__email': record.user_reciver.email,
            'user_reciver__middle_name': record.user_reciver.middle_name,
            'user_reciver__last_login': record.user_reciver.last_login,
        }
        return res

    def get_queryset(self):
        return Chat_user_userQuerySet(self.model, using=self._db)

    def deleteFromRequest(self, request, removed=None, function=None):
        request = DSRequest(request=request)
        qty = 0
        res = 0
        tuple_ids = request.get_tuple_ids()
        with transaction.atomic():
            for id, mode in tuple_ids:
                if mode == 'hide':
                    super().filter(id=id).soft_delete()
                else:
                    chat_user_user = Chat_user_user.objects.get(id=id)

                    WebSocket.send_message(
                        host=ws.WS_HOST,
                        port=ws.WS_PORT,
                        channel=f'common_{chat_user_user.user_reciver.username}',
                        message=dict(
                            type='reload_browser1',
                            user_id=chat_user_user.user_reciver.id
                        ), logger=logger)

                    WebSocket.send_message(
                        host=ws.WS_HOST,
                        port=ws.WS_PORT,
                        channel=f'common_{chat_user_user.user_sender.username}',
                        message=dict(
                            type='reload_browser1',
                            user_id=chat_user_user.user_sender.id
                        ), logger=logger)

                    qty, _ = super().filter(id=id).delete()
                res += qty
            return res

    def updateFromRequest(self, request, removed=None, function=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()

        with transaction.atomic():
            props = data.get('props')
            if data.get('compulsory_reading') == True:
                props |= Chat_user_user.props.compulsory_reading
            else:
                props &= ~Chat_user_user.props.compulsory_reading
            _data = dict()
            setAttr(_data, 'props', props)

            res, _ = super().update_or_create(id=data.get('id'), defaults=_data)
            WebSocket.send_message(
                host=ws.WS_HOST,
                port=ws.WS_PORT,
                channel=f'common_{res.user_reciver.username}',
                message=dict(
                    type='reload_browser1',
                    user_id=res.user_reciver.id
                ), logger=logger)

            WebSocket.send_message(
                host=ws.WS_HOST,
                port=ws.WS_PORT,
                channel=f'common_{res.user_sender.username}',
                message=dict(
                    type='reload_browser1',
                    user_id=res.user_sender.id
                ), logger=logger)

            return data

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        user_ids = data.get('user_ids', None)
        context_ids = data.get('context_ids', None)
        _data = []

        with transaction.atomic():
            if user_ids and context_ids:
                if not isinstance(user_ids, list):
                    user_ids = [user_ids]

                if not isinstance(context_ids, list):
                    context_ids = [context_ids]

                for user_id in user_ids:
                    for user_sender_id in context_ids:
                        res, _ = super().get_or_create(user_reciver_id=user_id, user_sender_id=user_sender_id)
                        res, _ = super().get_or_create(user_reciver_id=user_sender_id, user_sender_id=user_id)

                        WebSocket.send_message(
                            host=ws.WS_HOST,
                            port=ws.WS_PORT,
                            channel=f'common_{res.user_reciver.username}',
                            message=dict(
                                type='reload_browser1',
                                user_id=res.user_reciver.id
                            ), logger=logger)

                        WebSocket.send_message(
                            host=ws.WS_HOST,
                            port=ws.WS_PORT,
                            channel=f'common_{res.user_sender.username}',
                            message=dict(
                                type='reload_browser1',
                                user_id=res.user_sender.id
                            ), logger=logger)

                        _data.append(model_to_dict(res))

            return data


class Chat_user_user(AuditModel):
    user_sender = ForeignKeyCascade(User, related_name='user_sender_user')
    user_reciver = ForeignKeyCascade(User, related_name='user_reciver_user')
    common_id = PositiveIntegerField()
    props = BitField(flags=(
        ('compulsory_reading', 'Обязательное прочтение'),  # 1
    ), default=0, db_index=True)

    objects = Chat_user_userManager()

    def __str__(self):
        return f'id: {self.id}, common_id: {self.common_id}, user_sender: [{self.user_sender}], user_reciver: [{self.user_reciver}]'

    class Meta:
        verbose_name = 'Чаты личной переписки'
        unique_together = (('user_sender', 'user_reciver', 'common_id'),)
