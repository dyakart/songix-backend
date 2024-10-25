"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import include, path

# импортируем setting.py из приложения app
from django.conf import settings

# импортируем функцию static для медиа-файлов
from django.conf.urls.static import static

# первый аргумент в path - это адрес конкретной страницы,
# второй аргумент - регистрация представления, которое будет закреплено за этим адресом
# третий аргумент - для тегов в html-документах, чтобы можно было обращаться к этим ссылкам по имени
urlpatterns = [
    path('admin/', admin.site.urls),
    # namespace - имя приложения, к которому относятся url-адреса, когда мы обращаемся к ним в html-шаблонах templates
    # подключаем адреса для приложения users
    path('user/', include('users.urls', namespace='user')),
]

# при отладке (debug = true), будем подключать дополнительный инструмент для более детальной отладки
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
