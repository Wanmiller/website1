from django.urls import path

from .views import reply_comment

urlpatterns = [
    path("<int:pk>/reply/", reply_comment, name="reply"),
]
