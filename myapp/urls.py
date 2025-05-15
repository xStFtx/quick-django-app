from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('market-data/', views.market_data_view, name='market-data'),
    path('market_data', views.market_data_view, name='market_data'),
    path('market-data/<int:pk>/', views.market_data_detail, name='market-data-detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
]