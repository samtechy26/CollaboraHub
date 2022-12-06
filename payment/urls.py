from django.urls import path
<<<<<<< HEAD
from .views import CreateCheckoutSessionView, SuccessView
=======
from .views import CreateCheckoutSessionView, SuccessView, CancelView, create_coinbase_payment, coinbase_webhook

>>>>>>> a78dfc8f5286b65d86aad66c6b8f144042cb6658
urlpatterns = [ 
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
<<<<<<< HEAD
=======
    path('coinbase-pay/<pk>/', create_coinbase_payment, name='coinbase-payment'),
    path('webhook/',coinbase_webhook),
>>>>>>> a78dfc8f5286b65d86aad66c6b8f144042cb6658
]