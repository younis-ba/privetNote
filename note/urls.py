
from django.urls import path
from . import views
urlpatterns = [
    path('',views.createmessage),
    path('show-message/<str:id>/',views.showmeesage),

]
