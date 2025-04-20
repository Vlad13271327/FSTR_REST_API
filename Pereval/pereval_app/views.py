from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PerevalAdded
from .serializers import PerevalAddedSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class SubmitDataView(APIView):
    @swagger_auto_schema(
         operation_summary="Добавить новый перевал",
         operation_description="Создание нового объекта перевала. "
         "Пользователь передаёт данные перевала, координаты, уровень сложности и изображения.",
         request_body=PerevalAddedSerializer,
         responses={
             200: openapi.Response(description="Успешное добавление", examples={
                 "application/json": {
                     "status": 200,
                     "message": None,
                     "id": 42
                 }
             }),
             400: openapi.Response(description="Ошибка валидации"),
             500: openapi.Response(description="Внутренняя ошибка сервера"),
         }
    )
    def post(self, request):
        try:
            serializer = PerevalAddedSerializer(data=request.data)
            if serializer.is_valid():
                pereval = serializer.save()
                return Response(
                    {
                        "status": 200,
                        "message": None,
                        "id": pereval.id
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        "status": 400,
                        "message": "Ошибка валидации данных",
                        "errors": serializer.errors,
                        "id": None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {
                    "status": 500,
                    "message": f"Ошибка сервера: {str(e)}",
                    "id": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SubmitDataDetailView(APIView):
    @swagger_auto_schema(
         operation_summary="Получить перевал по ID",
         operation_description="Возвращает объект перевала с указанным id. Включает координаты, уровень сложности, пользователя, статус модерации и изображения.",
         responses={
             200: PerevalAddedSerializer,
             404: openapi.Response(description="Запись не найдена"),
         }
    )
    def get(self, request, id):
        try:
            pereval = PerevalAdded.objects.get(id=id)
            serializer = PerevalAddedSerializer(pereval)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PerevalAdded.DoesNotExist:
            return Response(
                {"message": "Запись не найдена", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )


class SubmitDataUpdateView(APIView):
    @swagger_auto_schema(
         operation_summary="Обновить перевал по ID",
         operation_description="Редактировать можно все поля, кроме ФИО, email и телефона, и если статус записи 'new'.",
         request_body=PerevalAddedSerializer,
         responses={
             200: openapi.Response(description="Успешно обновлено"),
             400: openapi.Response(description="Ошибка запроса или нельзя редактировать личные данные"),
             404: openapi.Response(description="Запись не найдена"),
         }
    )
    def patch(self, request, id):
        try:
            pereval = PerevalAdded.objects.get(id=id)
        except PerevalAdded.DoesNotExist:
            return Response(
                {"state": 0, "message": "Запись не найдена."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что запись в статусе "new"
        if pereval.status != PerevalAdded.NEW:
            return Response(
                {"state": 0, "message": "Запись нельзя редактировать, так как она не в статусе 'new'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Убираем поля, которые нельзя редактировать
        if 'user' in request.data:
            del request.data['user']

        # Обновляем запись
        serializer = PerevalAddedSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"state": 1, "message": "Запись успешно обновлена."})
        else:
            return Response(
                {"state": 0, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class SubmitDataListView(APIView):
    @swagger_auto_schema(
         operation_summary="Получить список перевалов по email",
         operation_description="Передай параметр user__email в строке запроса: http://127.0.0.1:8000/api/submitData/?user__email=qwerty@mail.ru"
                               " Возвращает список перевалов, отправленных этим пользователем.",
         manual_parameters=[
             openapi.Parameter(
                 name="user__email",
                 in_=openapi.IN_QUERY,
                 type=openapi.TYPE_STRING,
                 description="Email пользователя, по которому фильтруются перевалы",
                 required=True
             )
         ],
         responses={
             200: PerevalAddedSerializer(many=True),
             400: openapi.Response(description="Не указан email"),
             404: openapi.Response(description="Записи не найдены"),
         }
     )
    def get(self, request):
        # Получаем email из параметров запроса
        email = request.query_params.get('user__email', None)

        # Если email не указан, возвращаем ошибку
        if not email:
            return Response(
                {"message": "Не указан email пользователя", "status": 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Фильтруем записи по email пользователя
            perevals = PerevalAdded.objects.filter(user__email=email)

            # Если записи не найдены, возвращаем пустой список
            if not perevals.exists():
                return Response(
                    {"message": "Нет записей для указанного пользователя", "status": 404},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Сериализуем найденные записи
            serializer = PerevalAddedSerializer(perevals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": f"Ошибка сервера: {str(e)}", "status": 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )