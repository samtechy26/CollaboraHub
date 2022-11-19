from django.urls import path
from .views import CreateCheckoutSessionView, SuccessView, CancelView, create_coinbase_payment, coinbase_webhook

urlpatterns = [ 
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('coinbase-pay/<pk>/', create_coinbase_payment, name='coinbase-payment'),
    path('webhook/',coinbase_webhook),
]