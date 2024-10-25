from django.urls import path
from .views import LoginAPIView, RegistrationAPIView, ProfileAPIView, LogoutAPIView

# необходимо указать имя приложения для пространства имён (namespace), чтобы не было ошибки
app_name = 'users'

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/registration/', RegistrationAPIView.as_view(), name='api-registration'),
    path('api/profile/', ProfileAPIView.as_view(), name='api-profile'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),
]
