from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/', views.CreateCheckout.as_view()),
]
