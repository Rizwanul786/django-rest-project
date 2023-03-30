from django.contrib import admin
from django.urls import path,include
# from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from .views import (ProductData,MyAsyncView)
from .views import (add_update_tickets,get_all_jira_tickets,async_api)

urlpatterns = [
    # Functional based API
    path('add_update_tickets',add_update_tickets,name='add_update_tickets' ),
    path('get_all_jira_tickets',get_all_jira_tickets,name='get_all_jira_tickets' ),
    
    # Class based API
    path('get_products',ProductData.as_view(),name="get_products"),
    path('add_update_product',ProductData.as_view(),name="add_update_product"),

    # async API
    path('async_api',async_api,name="async_api"),
    path('my-async-view/', MyAsyncView.as_view(), name='my-async-view'),
]