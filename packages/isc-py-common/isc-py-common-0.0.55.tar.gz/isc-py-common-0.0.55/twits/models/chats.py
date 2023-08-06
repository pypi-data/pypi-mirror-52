import logging

from bitfield import BitField

from isc_common.models.base_ref import BaseRef, BaseRefManager, BaseRefQuerySet

logger = logging.getLogger(__name__)


class ChatsQuerySet(BaseRefQuerySet):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class ChatsManager(BaseRefManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
        }
        return res

    def get_queryset(self):
        return ChatsQuerySet(self.model, using=self._db)


class Chats(BaseRef):
    objects = ChatsManager()

    def __str__(self):
        return f"id : {self.code}, code : {self.code}, name : {self.name}, code : {self.description},"

    class Meta:
        verbose_name = 'Групповые чаты'
