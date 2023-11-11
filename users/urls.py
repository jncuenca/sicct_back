from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserDetailView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('changepassword/', views.ChangePasswordView().as_view()),
]