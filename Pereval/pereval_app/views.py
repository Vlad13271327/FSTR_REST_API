from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PerevalAdded
from .serializers import PerevalAddedSerializer

class SubmitDataView(APIView):
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