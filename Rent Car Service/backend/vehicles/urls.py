from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle-create'),
    path('vehicles/<int:pk>/update/', views.VehicleUpdateView.as_view(), name='vehicle-update'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle-delete'),
    path('categories/', views.VehicleCategoryListView.as_view(), name='category-list'),
    path('cities/', views.CityListView.as_view(), name='city-list'),
]
