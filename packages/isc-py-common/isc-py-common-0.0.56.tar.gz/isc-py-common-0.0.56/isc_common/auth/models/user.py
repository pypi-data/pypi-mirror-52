import logging

from isc_common.auth.managers.user_manager import UserManager
from isc_common.auth.models.abstract_user import AbstractUser
from isc_common.fields.code_field import CodeField

logger = logging.getLogger(__name__)


class User(AbstractUser):
    color = CodeField(null=True, blank=True)

    @staticmethod
    def admin_user():
        admin_user, _ = User.objects.get_or_create(username='admin', defaults=dict(password='admin'))
        return admin_user

    def __str__(self):
        return f"id: {self.id}, username: {self.username}, full_name: ({self.first_name} {self.middle_name} {self.last_name})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        swappable = 'AUTH_USER_MODEL'


