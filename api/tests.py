# Unit Test cases

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Tickets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from user_account.models import User

class TicketsTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass',email='test121@gmail.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_a_row(self):
        """Create a row in the table"""
        Tickets.objects.create(key="VELOCITY-111",title="New ticket title",project_name="Project-1",priority="Medium",updated_date="2023-03-04",ticket_status="To DO",created_date="2023-03-04",creator_email="test121@gmail.com")
        obj=Tickets.objects.filter(key="VELOCITY-111")
        self.assertEqual(obj.count(), 1)

    # def test_create_a_row_with_null_value(self):
    #     """Create a row in the table by passing null value of ticket_status"""
    #     Tickets.objects.create(key="VELOCITY-121",title="New ticket title",project_name="Project-1",priority="Medium",updated_date="2023-03-04",ticket_status=None,created_date="2023-03-04",creator_email="test121@gmail.com")
    #     obj=Tickets.objects.filter(key="VELOCITY-121")
    #     self.assertEqual(obj.count(), 0)
        # Error return: django.db.utils.IntegrityError: (1048, "Column 'ticket_status' cannot be null")


    def test_get_all_tickets_list(self):
        """getting All tickest from Database without refresh"""
        response = self.client.get('/api/get_all_jira_tickets?refresh=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)
        
    def test_get_all_tickets_list_with_refresh(self):
        """getting All tickest from Database with refresh. This API will call jira_script and script will update tickets status"""
        response = self.client.get('/api/get_all_jira_tickets?refresh=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_update_tickets(self):
        """Check for tickets are adding or not"""
        data=[{
            "key":"VELOCITY-10","title":"New ticket title","project_name":"Project-1","priority":"Medium","updated_date":"2023-03-04","created_date":"2023-03-04","creator_email":"test121@gmail.com"
        }]
        response = self.client.post('/api/add_update_tickets',json=data,format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_update_tickets_with_wrong_method(self):
        """Check for tickets are adding or not by passing wrong method it should be return 405 status_code"""
        data=[{
            "key":"VELOCITY-111","title":"New ticket title","project_name":"Project-1","priority":"Medium","updated_date":"2023-03-04","created_date":"2023-03-04","creator_email":"test121@gmail.com"
        }]
        response = self.client.get('/api/add_update_tickets',json=data,format="json")
        self.assertEqual(response.status_code, 405)