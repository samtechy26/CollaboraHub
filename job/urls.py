from django.urls import path
from .views import HomeView, JobCreateView, JobListView, JobDetail, UserListView, ContactView, JobUpdateView, JobDeleteView, HomeSearch

app_name = 'job'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('job/new/', JobCreateView.as_view(), name='job-create'),
    path('job/update/<int:pk>', JobUpdateView.as_view(), name='job-update'),
    path('job/delete/<int:pk>', JobDeleteView.as_view(), name='job-delete'),
    path('job/list/', JobListView.as_view(), name='job-list'),
    path('job/<int:pk>/', JobDetail, name='job-detail'),
    path('freelancers', UserListView.as_view(), name='freelancer'),
    path('contact/', ContactView.as_view(), name='contact' ),
    path('search', HomeSearch.as_view(), name='home-search'),
  
]