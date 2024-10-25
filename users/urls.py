from django.urls import path
from .views import LoginAPIView, RegistrationAPIView, ProfileAPIView, LogoutAPIView

# необходимо указать имя приложения для пространства имён (namespace), чтобы не было ошибки
app_name = 'users'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('registration/', RegistrationAPIView.as_view(), name='api-registration'),
    path('profile/', ProfileAPIView.as_view(), name='api-profile'),
    path('logout/', LogoutAPIView.as_view(), name='api-logout'),
]
