from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


# Переопределяем дефолтную модель класса AbstractUser из django
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    failed_attempts = models.IntegerField(default=0, verbose_name='Неудачные попытки входа')
    last_failed_login = models.DateTimeField(null=True, blank=True, verbose_name='Последняя неудачная попытка')
    # поле, которое будет хранить время блокирован аккаунта
    lock_until = models.DateTimeField(null=True, blank=True, verbose_name='Время разблокировки')

    def is_locked(self):
        """Метод для проверки блокировки пользователя"""
        if self.lock_until and self.lock_until > now():
            return True
        return False

    def reset_failed_attempts(self):
        """Метод для сброса неудачных попыток входа"""
        self.failed_attempts = 0
        self.last_failed_login = None
        self.save()

    def reset_lock(self):
        """Метод для ручного сброса блокировки, например администратором"""
        self.lock_until = None
        self.failed_attempts = 0
        self.save()

    class Meta:
        # обычно таблицы называют в единственном числе (здесь, как она будет отображаться в БД)
        db_table = 'user'
        # как будет отображаться в админ панели (в единственном числе)
        verbose_name = 'Пользователя'
        # в множественном числе
        verbose_name_plural = 'Пользователи'

    # метод перегрузки для вывода объекта (изменяем отображение каждого пользователя в админ панели)
    def __str__(self):
        return self.username
