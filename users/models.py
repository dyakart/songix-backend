from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager


# Кастомный менеджер пользователя, который убирает username из обязательных полей для создания пользователя и
# суперпользователя.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError({"message": "Введите email!"})
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError({"message": "Суперпользователь должен иметь is_staff=True."})
        if extra_fields.get('is_superuser') is not True:
            raise ValueError({"message": "Суперпользователь должен иметь is_superuser=True."})

        return self.create_user(email, password, **extra_fields)


# Переопределяем дефолтную модель класса AbstractUser из django
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    failed_attempts = models.IntegerField(default=0, verbose_name='Неудачные попытки входа')
    last_failed_login = models.DateTimeField(null=True, blank=True, verbose_name='Последняя неудачная попытка')
    # поле, которое будет хранить время блокирован аккаунта
    lock_until = models.DateTimeField(null=True, blank=True, verbose_name='Время разблокировки')
    # указываем Django, что email теперь должен быть полем для аутентификации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Привязываем кастомный менеджер
    objects = CustomUserManager()

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
