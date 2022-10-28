from django.urls import path
from .views import home, JobCreateView, JobListView, JobDetail, UserListView, dashboard_favourites, contact, CategoryView

urlpatterns = [
    path('', home, name='job-home'),
    path('job/new/', JobCreateView.as_view(), name='job-create'),
    path('job/list/', JobListView.as_view(), name='job-list'),
    path('job/<int:pk>/', JobDetail, name='job-detail'),
    path('freelancers', UserListView.as_view(), name='freelancer'),
    path('favourites/', dashboard_favourites, name='dashboard-favourites'),
    path('contact/', contact, name='contact' ),
    path('job/category/<str:slug>/',CategoryView.as_view(),name='task-category'),
    
    
]