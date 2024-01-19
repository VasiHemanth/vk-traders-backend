from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import *
from .serializers import * 

from .utils.trip_utils import *
from .utils.helper import get_monthYear_range, get_last_six_monthYear, get_strp_time
# Vercel static files
from datetime import datetime
from django.http import HttpResponse

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from VK Traders!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email 
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_superuser'] = user.is_superuser

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def logout(request):
    # Assuming you are using the simplejwt refresh token approach
    refresh_token = request.GET.get('refresh-token')

    if refresh_token:
        try:
            RefreshToken(refresh_token).blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"message": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_vehicles(request):
    try:
        get_vehicles = list(Vehicle.objects.all().values("registration_number", 'company', 'driver_name', 'status').order_by("registration_number"))
        return Response(get_vehicles, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(e)
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vehicle_data(request):
    vehicle_id = request.GET.get('vehicleId')

    try:
        vehicle_details = Vehicle.objects.get(registration_number=vehicle_id)
        serializer = VehicleSerializer(vehicle_details)
        trip_dates = list(Trip.objects.filter(vehicle_id=vehicle_id).values('id', 'trip_date', 'no_of_trips', 'submit_status').order_by('trip_date'))
        return Response({"vehicle_details": serializer.data, 'trip_dates':trip_dates}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search(request):
    search_string = request.GET.get('search-string')
    try:
        vehicles = list(Vehicle.objects.filter(registration_number__contains=search_string).values(
            'id', 'registration_number', 'company', 'driver_name', 'status'
            ))
        return Response(vehicles, status=status.HTTP_200_OK)
    except Exception as e: 
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_trip_data(request):
    trip_id = request.GET.get('tripId')

    try:
        trip_data = Trip.objects.get(id=trip_id)
        serializer = TripSerializer(trip_data)

        orders_to_trip = list(OrderToTripMapping.objects.filter(trip_id=trip_id).values('order_id')) 
     
        orderIds = [order['order_id'] for order in orders_to_trip]

        orders = list(Order.objects.filter(id__in=orderIds).values('id', 'date', 'order_id', 'order_submit_status')) 
        order_data = []
        order_status = False
        for order in orders:
            order_details = { 
                'id': str(order['id']), 
                'date': order['date'], 
                'order_id': order['order_id'], 
                'order_submit_status': order['order_submit_status']
            }
            if order['order_submit_status']:
                order_status = True
            else:
                order_status = False
            order_data.append(order_details) 

        trip_metrics = trip_data_config(serializer.data)

        return_response = {
            "trip_details": serializer.data, 
            "trip_metrics": trip_metrics,  
            "orders": orders
        }
        return_response['trip_details']['order_submit_status'] = order_status
        return Response(return_response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def create_trip(request):
    try:
        if request.method == 'GET':
            get_vehicles = list(Vehicle.objects.filter(status='Stable').values('registration_number'))
            
            vehicles = []
            for vehicle in get_vehicles:
                vehicles.append({
                    "label": vehicle["registration_number"],
                    "value": vehicle["registration_number"]
                }) 

            return Response(vehicles, status=status.HTTP_200_OK)
    
        elif request.method == 'POST':
            trip_body = request.data
            
            new_trip = Trip.objects.create(
                trip_date=convert_date_time_string_to_datetime(trip_body['date']), 
                trip_type=trip_body['tripType']['value'], 
                no_of_trips=int(trip_body['Trips']),
                vehicle_id=trip_body['selectedVehicle']['value'],
                owner_name=trip_body['ownerName']
            )

            Vehicle.objects.filter(registration_number=trip_body['selectedVehicle']['value']).update(
                status='In Transport'
            )

            return_response = {}
            if new_trip.id:
                return_response['id'] = new_trip.id
                return_response['vehicle_id'] = trip_body['selectedVehicle']['value']
                return_response['message'] = 'New Trip Created'

            return Response(return_response, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# update trip API
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def submit_trip(request):
    trip_body = request.data

    try:

        get_order_ids = list(OrderToTripMapping.objects.filter(trip_id=trip_body['tripId']).values())

        order_ids = [ order['order_id'] for order in get_order_ids ]

        order_expenses_data = list(Order.objects.filter(id__in=order_ids).values('total_expenses', 'freight_amount', 'driver_amount')) 

        amount = multi_orders_expense_calculator(order_expenses_data)

        Trip.objects.filter(id=trip_body['tripId']).update(
            reading= int(trip_body['trip_data']['reading']),
            kilometers= int(trip_body['trip_data']['tripDistance']),
            diesel= float(trip_body['trip_data']['dieselLitres']),
            diesel_per_litre= float(trip_body['trip_data']['dieselPerLitre']),
            diesel_amount= float(trip_body['trip_data']['dieselAmount']),
            mileage= float(trip_body['trip_data']['mileage']),
            ad_blue= float(trip_body['trip_data']['adBlue']),
            # maintanance= float(trip_body['trip_data']['maintanance']),
            # balance_amount= amount - float(trip_body['trip_data']['dieselAmount']) - int(trip_body['trip_data']['adBlue']) - int(trip_body['trip_data']['maintanance']),
            balance_amount= amount - float(trip_body['trip_data']['dieselAmount']) - int(trip_body['trip_data']['adBlue']),
            submit_status=True
        )

        print("Balance amount", amount - float(trip_body['trip_data']['dieselAmount']) - int(trip_body['trip_data']['adBlue']))

        get_vehicle = list(Trip.objects.filter(id=trip_body['tripId']).values('vehicle_id'))

        Vehicle.objects.filter(registration_number=get_vehicle[0]['vehicle_id']).update(
            status="Stable"
        )

        return Response({'message':'Trip submitted successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_order(request):
    order_body = request.data

    try:
        new_order = Order.objects.create(
            date= convert_date_time_string_to_datetime(order_body['order_data']['date']),
            quantity= float(order_body['order_data']['quantity']),
            grade= order_body['order_data']['grade'],
            from_field= order_body['order_data']['fromLocation'],
            to= order_body['order_data']['toLocation'],
            order_id= order_body['order_data']['shipmentNumber'],
            party_name= order_body['order_data']['partyName'],
            advance= order_body['order_data']['advance'],
            order_submit_status= False,
        )

        map_order_to_trip = OrderToTripMapping.objects.create(
            trip_id = order_body['trip_id'],
            order_id = new_order.id
        )

        return Response({ 
            'id': map_order_to_trip.id, 
            'order_id': new_order.id, 
            'message':'Order created successfully!'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated]) 
def submit_order_data(request):

    try:
        if request.method == "GET":
            key = request.GET.get('key')
            
            get_order_quantity = Order.objects.filter(id=key).values('quantity')
            
            return Response(
                {'quantity': get_order_quantity[0]['quantity']},
                status=status.HTTP_200_OK
            )
        
        elif request.method == "POST":
            submit_order_body = request.data

            gst_amount = 0
            if(submit_order_body['order_data']['gst'] == True):
                gst_amount = round(submit_order_body['order_data']['freightAmount']) * 0.12 

            Order.objects.filter(id=submit_order_body['id']).update(
                loading= int(submit_order_body['order_data']['loading']),
                unloading= int(submit_order_body['order_data']['unloading']),
                toll_gate= int(submit_order_body['order_data']['tollGate']),
                rto_pcl= int(submit_order_body['order_data']['pclRto']),
                total_expenses= int(submit_order_body['order_data']['totalExpenses']),
                freight= int(submit_order_body['order_data']['freight']),
                freight_amount=  submit_order_body['order_data']['freightAmount'],
                driver_freight= int(submit_order_body['order_data']['driverFreight']),
                driver_amount= int(submit_order_body['order_data']['driverAmount']),
                order_submit_status= True,
                gst = submit_order_body['order_data']['gst'],
                gst_amount = gst_amount
            )

            get_submitted_order = Order.objects.get(id=submit_order_body['id'])
            serializer = OrderSerializer(get_submitted_order)
          
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def order_data(request):
    order_id = request.GET.get('orderId')

    try:
        order_data = Order.objects.get(id=order_id)
        
        serializer = OrderSerializer(order_data)

        order_details = order_data_config(serializer.data)

        return Response({
            'order_date': serializer.data['date'], 
            'order_submit_status': serializer.data['order_submit_status'],
            'order_data': order_details    
        },status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def all_trucks(request):
    try:
        get_all_trucks = Vehicle.objects.all().values('registration_number').order_by('registration_number')

        # vehicles = []
        # for vehicle in get_all_trucks:
        #     vehicles.append({
        #         "label": vehicle["registration_number"],
        #         "value": vehicle["registration_number"]
        #     }) 

        return Response(get_all_trucks, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def truck_vitals(request):
    vehicle_id = request.GET.get('truck_id')
    monthYear = request.GET.get('monthYear')
    try:
        start_date, end_date = get_monthYear_range(monthYear)
        vitals_from_trip = list(Trip.objects.filter(
            vehicle_id=vehicle_id, 
            trip_date__range=(start_date, end_date),
            submit_status=True).values(
                'id', 
                'vehicle_id', 
                'trip_date', 
                'balance_amount', 
                'diesel_amount',
                'ad_blue',
                'reading'
            ).order_by('trip_date')
        )
        trip_ids = []
        balance = 0
        diesel_amount = 0
        ad_blue = 0
        reading = 0

        for trip in vitals_from_trip:
            trip_ids.append(trip['id'])
            balance += trip['balance_amount']
            diesel_amount += trip['diesel_amount']
            ad_blue += trip['ad_blue']
            reading = trip['reading']

        vehicle_instance = Vehicle.objects.get(registration_number=vehicle_id)
        # print(str(start_date), type(start_date))
        maintenance = list(Maintenance.objects.filter(
            vehicle_id=vehicle_instance,
            maintenance_date__range=(start_date, end_date),
        ).values( 'maintenance_name', 'charges'))

        maintenance_charges, total_maintenance = maintenance_data_config(maintenance)
        
        order_ids_associated_with_trip_ids = list(OrderToTripMapping.objects.filter(
            trip_id__in=trip_ids
        ).values('order_id'))

        order_ids = [order['order_id'] for order in order_ids_associated_with_trip_ids]

        vitals_from_order = list(Order.objects.filter(id__in=order_ids, order_submit_status=True).values(
            'date', 
            'from_field',
            'to',
            'quantity', 
            'freight_amount',
            'loading',
            'unloading',
            'toll_gate',
            'rto_pcl',
            'driver_amount', 
        ).order_by('date'))
        
        quantity = 0
        freight = 0
        loading = 0
        unloading=0
        toll_gate=0
        rto_pcl = 0
        driver_amount=0
        recent_deliveries = []
        for order_detail in vitals_from_order:
            print("order_detials date", order_detail['date'])
            quantity += order_detail['quantity']
            freight += order_detail['freight_amount'] if order_detail['freight_amount'] != None else 0
            loading += order_detail['loading']
            unloading += order_detail['unloading']
            toll_gate += order_detail['toll_gate']
            rto_pcl += order_detail['rto_pcl']
            driver_amount += order_detail['driver_amount']
            recent_deliveries.append({
                'order_date': order_detail['date'],
                'from': order_detail['from_field'],
                'to': order_detail['to'],
                'frieght': order_detail['freight_amount'],
                'quantity': str(order_detail['quantity']) + " tons" 
            })
        # print("vitals", vitals_from_trip, balance, maintanance, quantity, freight)
        
        vitals = vitals_data_config({
            'Frieght Amount':freight,
            'Total Expenditure': loading + unloading + toll_gate + rto_pcl + diesel_amount + ad_blue + driver_amount, 
            'EMI': None,
            'Kilometers': reading,
            'Maintenance': maintenance_charges,
            'Quantity': quantity,
            'Balance': balance - maintenance_charges,
        })
        # print("vitals", vitals)
        total_expenses = expenses_data_config({
            'Loading': loading,
            'UnLoading': unloading,
            'Toll Gate': toll_gate,
            'RTO & PC': rto_pcl,
            'Diesel Amount': diesel_amount,
            'AdBlue': ad_blue,
            'Driver Amount': driver_amount
        })

        return Response([vitals, recent_deliveries, total_expenses, total_maintenance], status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def chartData(request):
    source = request.GET.get('source')
    vehicle_id = request.GET.get('truck_id')
    monthYear = request.GET.get('monthYear')

    try:
        get_six_months = get_last_six_monthYear(monthYear)
        labels = []
        values= []

        for month_year in get_six_months:
            start_date, end_date = get_monthYear_range(month_year)

            if source != "quantity":
                labels.append(get_strp_time(month_year)) 

                # Total Maintenance charges for particular month
                vehicle_instance = Vehicle.objects.get(registration_number=vehicle_id)
                maintenance = list(Maintenance.objects.filter(
                    vehicle_id=vehicle_instance,
                    maintenance_date__range=(start_date, end_date),
                ).values( 'maintenance_name', 'charges'))
                
                maintenance_charges = 0
                for charge in maintenance:
                    maintenance_charges += charge['charges']
                
                if source == "balance_amount":
                    source_data = list(Trip.objects.filter(
                        vehicle_id=vehicle_id,
                        trip_date__range=(start_date, end_date),
                        submit_status=True).values(
                            'id', 
                            'balance_amount'                 
                        ).order_by('trip_date')
                    )

                    column_value = 0
                    for src_data in source_data:
                        column_value += src_data['balance_amount' ]
    
                    values.append(column_value - maintenance_charges)
                elif source == "maintenance":
                    values.append(maintenance_charges)

            else:
                trip_ids = []
                source_data = list(Trip.objects.filter(
                    vehicle_id=vehicle_id,
                    trip_date__range=(start_date, end_date),
                    submit_status=True).values(
                        'id',                  
                    ).order_by('trip_date')
                )
           
                for src_data in source_data:
                    trip_ids.append(src_data['id'])

                order_ids_associated_with_trip_ids = list(OrderToTripMapping.objects.filter(
                    trip_id__in=trip_ids
                ).values('order_id'))
                
                order_ids = [order['order_id'] for order in order_ids_associated_with_trip_ids]

                quantity_from_orders = list(Order.objects.filter(
                    id__in=order_ids, 
                    order_submit_status=True
                ).values(
                    'quantity'
                ))

                quantity = 0
                for order_detail in quantity_from_orders:
                    quantity += order_detail['quantity']

                labels.append(get_strp_time(month_year)) 
                values.append(quantity)

        response = {
            'column': source.capitalize(),
            'labels' : labels,
            'values': values
        }
        
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def maintenance_data(request):
    try:
        if request.method == "GET":
            vehicle_id = request.GET.get('vehicle_id')

            maintenance_details = list(Maintenance.objects.filter(
                vehicle_id__registration_number = vehicle_id
            ).values('id', 'maintenance_date', 'maintenance_name', 'charges').order_by('-maintenance_date'))

            maintenance =  maintenance_config(maintenance_details)

            return Response(maintenance, status=status.HTTP_200_OK)
        elif request.method == "POST":
            maintenance_body = request.data

            print(maintenance_body)

            vehicle_instance = Vehicle.objects.get(registration_number=maintenance_body['vehicle_id'])

            print("instance", vehicle_instance)

            service_name= Maintenance.objects.create(
                vehicle_id= vehicle_instance,
                maintenance_date=maintenance_body['maintenance_date'],
                maintenance_name=maintenance_body['activity_name'],
                charges=maintenance_body['charges']
            )

            return_response = {}
            if service_name.id:
                return_response['id'] = service_name.id
                return_response['message'] = 'New Maintenance activity added'

            return Response(return_response, status=status.HTTP_200_OK)


    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    