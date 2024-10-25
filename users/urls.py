from django.urls import path
from .views import LoginAPIView, RegistrationAPIView, ProfileAPIView, LogoutAPIView

# необходимо указать имя приложения для пространства имён (namespace), чтобы не было ошибки
app_name = 'users'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
