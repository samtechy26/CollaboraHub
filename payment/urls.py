from django.urls import path
from .views import CreateCheckoutSessionView, SuccessView
urlpatterns = [ 
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]