from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("logout/", views.logout_view, name="logout"),   
]




