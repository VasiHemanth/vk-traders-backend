from django.urls import path

from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    

    # Authentication and Authorization
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', views.logout, name='logout'),

    # Vehicle Related Data API's
    path('all-vehicles/', views.all_vehicles, name='all vehicles'),
    path('vehicle-data', views.get_vehicle_data, name='vehicle data + associated trip dates'),
    path('search', views.search, name='search'),
   

    # Trip
    path('create-trip', views.create_trip, name='active vehicles + create trip'),
    path('submit-trip', views.submit_trip, name='submit trip'),
    path('trip-data', views.get_trip_data, name='trip data'),

    # Order
    path('create-order', views.create_order, name='create order'),
    path('submit-order-data', views.submit_order_data, name='submit order data'),
    path('order-data', views.order_data, name='order data'),

    # Truck Dashboard 
    path('all-trucks', views.all_trucks, name="get all trucks"),
    path('truck-vitals', views.truck_vitals, name="get all trucks"),


]