from django.urls import path
from .views import HomeView, JobCreateView, JobListView, JobDetail, UserListView, ContactPageView

app_name = 'job'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('job/new/', JobCreateView.as_view(), name='job-create'),
    path('job/list/', JobListView.as_view(), name='job-list'),
    path('job/<int:pk>/', JobDetail, name='job-detail'),
    path('freelancers', UserListView.as_view(), name='freelancer'),
    path('contact/', ContactPageView.as_view(), name='contact' ),
  
]