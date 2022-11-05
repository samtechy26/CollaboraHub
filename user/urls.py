from email import message
from pyexpat.errors import messages
from django.urls import path
from .views import dashboard, register, profile, profileUpdate, reviews, dashboard_task, dashboard_bidders, dashboard_mybids, bid_update, activate, manage_offer
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('profile/<int:id>', profile, name='profile'),
    path('managebidders/job/<int:id>', dashboard_bidders, name='manage-bidders'),
    path('my_bids/', dashboard_mybids, name='my_bids'),
    path('bid_update/<int:id>', bid_update, name='bid_update'),
    path('manage_offer/<int:id>', manage_offer, name='manage_offer'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/task', dashboard_task, name='dashboard-task'),
    path('reviews/', reviews, name='reviews'),
    path('profile_update/', profileUpdate, name='profile-update'),
    path('activate/<uidb64>/<token>', activate, name='activate')
    
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)