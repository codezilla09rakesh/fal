from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.Register.as_view()),
    path('verify/', views.Verify.as_view()),

    path("login/", views.Token.as_view()),
    path("password/", views.ChangePasswordView.as_view()),
    path("profile/", views.ProfileView.as_view()),
    path("token/refresh/", views.RefreshToken.as_view()),
    path("token/revoke/", views.RevokeToken.as_view()),

    path("countries/", views.Countries.as_view({"get":"list"})),


]
