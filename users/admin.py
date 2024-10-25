from django.contrib import admin
from .models import User


# Создаем action для сброса блокировки
@admin.action(description='Разблокировать выбранных пользователей')
def unlock_users(model_admin, request, queryset):
    for user in queryset:
        # Используем метод сброса блокировки
        user.reset_lock()
        user.save()


# Регистрация модели User с добавленным action
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_locked')
    actions = [unlock_users]

    # Добавляем метод для отображения статуса блокировки
    def is_locked(self, obj):
        return obj.is_locked()

    # Отображение статуса как галочки
    is_locked.boolean = True
