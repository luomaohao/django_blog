from django.urls import path, include
from .views import todoView, todojson
app_name = "api"
urlpatterns = [
    path('activities/', todoView.as_view(), name="todo"),
    path('todojson/', todojson, name="todojson"),
    path('activities/<int:id>', todoView.as_view(), name="delete_todo"),
]