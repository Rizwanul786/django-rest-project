from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import APIException

import os, time
from datetime import timedelta
from datetime import datetime
from django.db.models import Q, F
from .models import (Tickets,Product)
from .serializers import (ProductSerializer)

from django.http import JsonResponse
from asgiref.sync import sync_to_async
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Scripts and custom class.
from api.management.custom_class.add_bulk import BulkCreateManager
from api.management.commands.jira_script import Jira

# Test that adding a ticket to the DB results in the ticket being stored in the DB.
# Test that updating a ticket in the DB results in the ticket being updated in the DB.
# Test that the correct error message is returned if the ticket data is invalid.
@permission_classes([IsAuthenticated, ])
@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
def add_update_tickets(request):
    data=request.data
    update_tickets_list=[]
    bulk_mgr = BulkCreateManager(chunk_size=5000)
    key_id_list=[obj["key"] for obj in data]
    try:
        # Here getting all existing tickets according to key_id list
        tickets=Tickets.objects.filter(key__in=key_id_list)
        found_ticket=[]
        if len(tickets)>0:
            found_ticket=tickets.values_list('key',flat=True)
        for ticket in data:
            if ticket["key"] in found_ticket:
                update_tickets_list.append(ticket)
            else:
                bulk_mgr.add(Tickets(**ticket))
        # Here adding new tickest
        bulk_mgr.done()
        
        # Here update tickest status title and updated date if ticket is already exist
        if len(update_tickets_list)>0:
            try:
                for ticket in tickets:
                    res=next(item for item in update_tickets_list if item["key"]==ticket.key)
                    try:ticket.title=res["title"]
                    except:pass
                    try:ticket.ticket_status=res["ticket_status"]
                    except:pass
                    try:ticket.updated_date=res["updated_date"]
                    except:pass
                Tickets.objects.bulk_update(tickets,fields=['title','ticket_status','updated_date'])
            except Exception as ex:
                raise APIException(ex)
        else:pass
        return Response({"message":"Successful added tickets"})
    except Exception as e:
        raise APIException(e)

# If an user call with refresh=false.
# All data will respond
# If an user call this api with refresh=true this api will call jira_script and that script will fetch all the new tickets and old ticket
# new tickets will add in the database and old tickest update
@permission_classes([IsAuthenticated, ])
@api_view(['GET'])
@authentication_classes([TokenAuthentication, ])
def get_all_jira_tickets(request):
    refresh=request.query_params.get('refresh','')
    if refresh=='true':
        obj = Jira()
        data=obj.get_jira_tickets()
        obj.add_tickets_to_db(data)
    else:pass
    try:
        tickets=Tickets.objects.all().values('key','title','ticket_status','updated_date')
        return Response(tickets)
    except Exception as e:
        raise APIException(e)


# @permission_classes([IsAuthenticated, ])
# @api_view(['POST'])
# @authentication_classes([TokenAuthentication, ])
# def add_new_products(request):
#     bulk_mgr = BulkCreateManager(chunk_size=5000)
#     data=request.data
#     for product in data:
#         try:
#             bulk_mgr.add(Product(**product))
#         except Exception as e:
#             return Response({"Error":e})
#     bulk_mgr.done()
#     return Response({"message":"Successful add products"})

# @permission_classes([IsAuthenticated, ])
# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication, ])
# def update_products(request):
#     data=request.data
#     pid_list=[obj["pid"] for obj in data]
#     products=Product.objects.filter(pid__in=pid_list)
#     try:
#         for product in products:
#             res=next(item for item in data if item["pid"]==product.pid)
#             try:product.price=res["price"]
#             except:pass
#             try:product.active=res["active"]
#             except:pass
#         Product.objects.bulk_update(products,fields=['price','active'])
#         return Response({"message":"Successful update products"})
#     except Exception as e:
#         raise APIException(e)



##################################### Class based API creating ##############################################
@permission_classes([IsAuthenticated, ])
class ProductData(APIView):
    def get(self,request):
        search=request.query_params.get('title','')
        try:
            # Here getting all products
            products=Product.objects.all()
            # Here filtering products according to title if title params is not empty
            if search:
                products=products.filter(name__icontains=search)
            # Here getting relevant columns
            data = products.values()
            return Response(data)
        except Exception as e:
            raise APIException(e)
    def put(self,request):
        try:
            obj=Product.objects.get(pid=request.data["pid"])
            obj.product_image=request.data["product_image"]
            obj.save()
            return Response({"message":"Success"})
        except Product.DoesNotExist as e:
            return Response("Product Not Exist")
    def post(self,request):
        try:
            serializer = ProductSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message":"Successful added product"})
        except Exception as e:
            raise APIException(e)


#################################### async API ########################################################

class MyAsyncView(View):
    @method_decorator(csrf_exempt)
    async def dispatch(self, request, *args, **kwargs):
        return await super().dispatch(request, *args, **kwargs)

    async def get(self, request):
        my_model = await sync_to_async(Tickets.objects.get)(id=1)
        data = {
                "id": my_model.id,
                "key": my_model.key,
            }
            
        return JsonResponse(data, safe=False)

@permission_classes([IsAuthenticated, ])
@api_view(['GET'])
async def async_api(request):
    id =request.query_params.get('id','')
    try:
        # Define the ORM query to fetch rows
        query = Tickets.objects.gey(id=2)

        # Execute the ORM query asynchronously using sync_to_async
        rows = await sync_to_async(query)

        # Return the fetched rows as a JSON response
        return JsonResponse({'data': {'id': rows.id, 'username': rows.key}}, status=200)
    except Exception as e:
        raise APIException(e)