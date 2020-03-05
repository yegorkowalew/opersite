from django.urls import path, include

from face.views import OrderList

urlpatterns = [
    path('start/', OrderList.as_view()),
]