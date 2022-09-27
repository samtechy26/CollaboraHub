from django.urls import path
from .views import home, JobCreateView, JobListView, JobDetail, UserListView

urlpatterns = [
    path('', home, name='job-home'),
    path('job/new/', JobCreateView.as_view(), name='job-create'),
    path('job/list/', JobListView.as_view(), name='job-list'),
    path('job/<int:pk>/', JobDetail, name='job-detail'),
    path('freelancers', UserListView.as_view(), name='freelancer'),
    
    
]