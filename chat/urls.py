from django.urls import path
from .views import dashboard_messages

urlpatterns =[
    path('messages/', dashboard_messages, name='dashboard-messages'),
]

