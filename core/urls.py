from django.urls import path

from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)


urlpatterns = [
    
    # Authentication and Authorization
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='verify token'),
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

    # Maintenance
    path('maintenance-data', views.maintenance_data, name='maintenance data'),

    # EMI
    path('emi-data', views.emi_data, name='emi data'),

    # Truck Dashboard 
    path('all-trucks', views.all_trucks, name="get all trucks"),
    path('truck-vitals', views.truck_vitals, name="trucks vitals"),
    path('chart-data', views.chartData, name="Chart data"),

    # Generate API's
    # path('generate-expenses', views.generateTotalExpensesAndBalanceWithGST, name="total expenses balance with gst"),
    # path('generate-gst', views.generateGSTInOrders, name="Generate GST in orders")
]
