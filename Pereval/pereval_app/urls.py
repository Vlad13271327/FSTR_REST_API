from django.urls import path
from .views import SubmitDataView, SubmitDataDetailView, SubmitDataUpdateView, SubmitDataListView

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit_data'),
    path('submitData/<int:id>/', SubmitDataDetailView.as_view(), name='submit_data_detail'),
    path('submitData/<int:id>/edit/', SubmitDataUpdateView.as_view(), name='submit_data_update'),
    path('submitData/list/', SubmitDataListView.as_view(), name='submit_data_list')
]
