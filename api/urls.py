from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.HelloApiView.as_view(), name='hello-api'),
    path('supabase-data/', views.SupabaseDataView.as_view(), name='supabase-data'),
    # Add API endpoints here
]
