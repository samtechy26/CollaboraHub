from email import message
from pyexpat.errors import messages
from django.urls import path
from .views import UserDashboard, profile, profileUpdate, Reviews, UserTaskList, dashboard_bidders, dashboard_mybids, bid_update, manage_offer, UserFavourites, BidPaymentView, UserLibraryView, review, message, CreateTestimonial
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('profile/<int:id>', profile, name='profile'),
    path('managebidders/job/<int:id>', dashboard_bidders, name='manage-bidders'),
    path('favourites/', UserFavourites.as_view(), name='dashboard-favourites'),
    path('my_bids/', dashboard_mybids, name='my_bids'),
    path('bid_update/<int:id>', bid_update, name='bid_update'),
    path('bid_detail/<int:id>', manage_offer, name='bid_detail'),
    path('dashboard/', UserDashboard, name='dashboard'),
    path('library/', UserLibraryView.as_view(), name='library'),
    path('dashboard/task', UserTaskList.as_view(), name='dashboard-task'),
    path('reviews/<int:user_id>', Reviews.as_view(), name='reviews'),
    path('review/<int:review_id>', review, name='review-details'),
    path('bid_payment/<int:pk>', BidPaymentView.as_view(), name='bid_payment'),
    path('profile_update/', profileUpdate, name='profile-update'),
    path('contact-user/', message, name='contact-user'),
    path('appreview/', CreateTestimonial.as_view(), name='app-review'),
   
    
    
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)