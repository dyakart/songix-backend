from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from .serializers import LoginSerializer, UserRegistrationSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
# для предотвращения частых попыток входа в систему (brute-force атаки)
from rest_framework.exceptions import Throttled, NotAuthenticated
from rest_framework.throttling import UserRateThrottle
from users.models import User


class LoginAPIView(APIView):
    # Ограничиваем частоту запросов
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            auth.login(request, user)
            if user.first_name:
                return Response({'message': f'{user.first_name}, Вы вошли в аккаунт'}, status=status.HTTP_200_OK)
            return Response({'message': 'Добро пожаловать в Songix!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):
        """Переопределим обработку троттлинга для лучшего UX"""
        if isinstance(exc, Throttled):
            return Response({
                'error': 'Слишком много попыток. Попробуйте через некоторое время.',
                'available_in': exc.wait
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        return super().handle_exception(exc)


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            auth.login(request, user)
            return Response({'message': 'Добро пожаловать в Songix!'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        # Получаем новый пароль, текущий пароль, new_email (если переданы)
        new_password = request.data.get('new_password')
        current_password = request.data.get('current_password')
        new_email = request.data.get('email')

        # Проверяем, что email уникален, если он передан, исключаем текущего пользователя из проверки
        if new_email and User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            return Response(
                {'error': 'Этот email уже используется другим пользователем.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfileSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            # Сохраняем данные профиля
            serializer.save()

            # Если передан новый пароль, устанавливаем его
            if new_password:
                if not current_password or not request.user.check_password(current_password):
                    return Response(
                        {'error': 'Текущий пароль указан неверно.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                request.user.set_password(new_password)
                request.user.save()

            return Response({
                'message': 'Профиль и пароль успешно обновлены'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):
        if isinstance(exc, NotAuthenticated):
            return Response({'error': 'Необходимо войти в систему для доступа к профилю.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)


class LogoutAPIView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'message': 'Вы уже вышли из аккаунта.'}, status=status.HTTP_200_OK)

        auth.logout(request)
        return Response({'message': 'Вы вышли из аккаунта'}, status=status.HTTP_200_OK)
