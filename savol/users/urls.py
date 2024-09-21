from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('user/', UserDetailView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify/', VerifyEmail.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path("dashboard/", DashboardView.as_view()),
    path("follow-list/", UsersToFollow.as_view()),
    path("<str:username>/", UserInfoView),    
]