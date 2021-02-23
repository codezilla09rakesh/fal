from django.urls import path
from . import views

urlpatterns = [

    path('plans/', views.PlansView.as_view({'get': 'list', 'post': 'create'}), name='plans_list'),
    path('plans/<str:id>/', views.PlansView.as_view({'get': 'retrieve', 'put': 'update'}), name='plan'),

    path('subscriptions/', views.SubscriptionsView.as_view({'get': 'list'}), name='subscriptions_list'),
    path('subscriptions/<str:id>/', views.SubscriptionsView.as_view({'get': 'retrieve', 'put': 'update'}),
         name='subscription'),

    path('transactions/', views.TransactionsView.as_view({'get': 'list'}), name="transaction_list"),
    path('transactions/<str:id>', views.TransactionsView.as_view({'get': 'retrieve'}), name="transaction"),

    path('bookmarks/', views.BookmarkView.as_view({"post": "create", "get": "list"}), name="bookmark"),
    path('bookmarks/<str:id>/', views.BookmarkView.as_view({"delete": "destroy"}), name="bookmark_destroy"),

    path('offers/', views.OffersView.as_view({'get': 'list'}), name="offer_list"),
    path('offers/<str:id>/', views.OffersView.as_view({'get': 'retrieve'}), name="offer"),
]









