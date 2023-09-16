from django.urls import path
from .views import CreateCheckoutSessionView, SuccessView, CancelView, create_coinbase_payment, coinbase_webhook, stripe_webhook, withdrawal

urlpatterns = [ 
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('coinbase-pay/<pk>/', create_coinbase_payment, name='coinbase-payment'),
    path('webhook', stripe_webhook, name='stripe-webhook'),
    path('coinbasewebhook/',coinbase_webhook),
    path('process_withdrawal', withdrawal, name="process_withdrawal")
    
]