from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User
from django.utils.timezone import now
from datetime import timedelta


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_locked():
                raise serializers.ValidationError(f"Аккаунт заблокирован до {user.lock_until}. Попробуйте позже.")

            if user.is_active:
                # Сбрасываем счетчик при успешной аутентификации
                user.reset_failed_attempts()
                return user
            else:
                raise serializers.ValidationError("Аккаунт отключён. Обратитесь к администратору.")

        # Если пользователь не найден или пароль неверный
        user = User.objects.filter(username=username).first()
        if user:
            user.failed_attempts += 1
            user.last_failed_login = now()
            user.save()

            # Устанавливаем лимит попыток (15)
            if user.failed_attempts >= 15:
                # Блокируем на 5 минут
                user.lock_until = now() + timedelta(minutes=5)
                user.save()
                raise serializers.ValidationError(f"Аккаунт заблокирован до {user.lock_until}. Попробуйте позже.")
            user.save()

        raise serializers.ValidationError("Неверные учетные данные!")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Это имя пользователя уже занято!")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже зарегистрирован!")
        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают!")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        # Правильное хеширование пароля
        user.set_password(validated_data['password1'])
        # сохраняем пользователя
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image', 'first_name', 'last_name', 'username', 'email']

    def validate_image(self, value):
        # Проверяем размер изображения
        # Ограничение: 2MB
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Размер изображения не должен превышать 2MB.")
        return value
