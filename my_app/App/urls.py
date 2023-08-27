from django.urls import path
from . import views
urlpatterns = [
    path('', views.jsonresp, name='process-url-response'),
]