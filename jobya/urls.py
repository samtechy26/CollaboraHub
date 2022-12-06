from django.contrib import admin
from django.urls import path, include
from payment.views import stripe_webhook


urlpatterns = [
    path('admin/', admin.site.urls),
    path('stripe', stripe_webhook, name='stripe_webhook'),
    path('', include('job.urls', namespace='job')),
    path('', include('user.urls')),
    path('', include('chat.urls')),
    path('', include('payment.urls')),
     path('accounts/', include('allauth.urls')),
    path('blog/', include('blog.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
]
