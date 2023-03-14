from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('', views.JobList.as_view(), name='jobs'),
    path('job/<int:pk>/', views.JobDetail.as_view(), name='job'),
    path('job-create/', views.JobCreate.as_view(), name='job-create'),
    path('job-update/<int:pk>', views.JobUpdate.as_view(), name='job-update'),
    path('job-delete/<int:pk>', views.JobDelete.as_view(), name='job-delete'),
]
