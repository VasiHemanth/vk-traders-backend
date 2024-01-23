
# @api_view(['GET'])
# def generateTotalExpensesAndBalanceWithGST(request):
#     vehicle_id = request.GET.get('vehicle_id')

#     try:
#         trips = list(Trip.objects.filter(vehicle_id=vehicle_id).values())

#         trip_ids = [ trip['id'] for trip in trips]

#         order_to_trips = list(OrderToTripMapping.objects.filter(
#             trip_id__in = trip_ids
#         ).values('trip_id', 'order_id'))

#         order_ids = [order['order_id'] for order in order_to_trips]

#         all_orders = list(Order.objects.filter(id__in=order_ids, order_submit_status=True).values())

#         final_list = []
#         check_ids = []

#         for orderTrips in order_to_trips:
#             for order in all_orders:
#                 if str(order['id']) == str(orderTrips['order_id']):
                    
#                     for final in final_list:
#                         if str(orderTrips['trip_id']) == str(final['trip_id']):
#                             final['total_expenses'] += order['total_expenses']
#                             final['balance_amount_with_gst'] += order['gst_amount']
                   
#                     if orderTrips['trip_id'] not in check_ids:
#                         final_list.append({
#                             'trip_id' : orderTrips['trip_id'],
#                             'total_expenses': order['total_expenses'],
#                             'balance_amount_with_gst': order['gst_amount']
#                         })
#                         check_ids.append(orderTrips['trip_id'])

        
#         if len(final_list) == len(trips):
#             print("All cool")

#         for trip in trips:
#             for final in final_list:
#                 if str(trip['id']) == str(final['trip_id']):
#                     Trip.objects.filter(id=trip['id']).update(
#                         total_expenses = trip['diesel_amount'] + trip['ad_blue'] + final['total_expenses'],
#                         balance_with_gst = trip['balance_amount'] + final['balance_amount_with_gst']
#                     )
#                     # balance_with_gst = trip['balance_amount'] + final['balance_amount_with_gst']
#                     # expenses = trip['diesel_amount'] + trip['ad_blue'] + final['total_expenses']
#                     # print(trip['trip_date'], trip['id'], expenses, balance_with_gst)

#         return Response({'message': 'Generated Succussfully!'}, status=status.HTTP_200_OK)
                             
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# @api_view(['GET'])
# def generateGSTInOrders(request):
#     vehicle_id = request.GET.get('vehicle_id')

#     try: 
#         trips = list(Trip.objects.filter(vehicle_id=vehicle_id).values())

#         trip_ids = [ trip['id'] for trip in trips]

#         order_to_trips = list(OrderToTripMapping.objects.filter(
#             trip_id__in = trip_ids
#         ).values('trip_id', 'order_id'))

#         order_ids = [order['order_id'] for order in order_to_trips]

#         all_orders = list(Order.objects.filter(id__in=order_ids, order_submit_status=True).values())

#         for order in all_orders:
#             Order.objects.filter(id=order['id']).update(
#                 gst = True,
#                 gst_amount=order['freight_amount'] * 0.12
#             )

#         return Response({'message': 'Generated Succussfully!'}, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


