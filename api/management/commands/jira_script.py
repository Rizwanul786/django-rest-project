# Author: Rizwan
# date: Feb 2023
# Description: This script will fetch all issues ticket from Jira and add it in DB

import requests
import json
import base64
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser
import logging
import os

"""logging exceptions"""
logging.basicConfig(filename=f"{os.path.dirname(os.path.realpath(__file__))}/jira.log",level=logging.DEBUG)

config = ConfigParser()
with open(f"{os.path.dirname(os.path.realpath(__file__))}/config.cfg", 'r') as configfile:
    config.read_file(configfile)

class Jira:
  def __init__(self):
    """Initialising API Base URI's and tokens"""
    self.jira_url = "https://rizwanfree.atlassian.net/rest/api/3/search"
    self.jira_url_for_update="https://rizwanfree.atlassian.net/rest/api/3/issue/"
    self.jira_api_token = config.get("API Auth", "jira_api_token")
    self.jira_user = config.get("API Auth", "jira_user")
    self.gmail= config.get("API Auth", "gmail")
    self.db_token= config.get("API Auth", "db_token")
    self.auth = HTTPBasicAuth(self.gmail, self.jira_api_token)
    self.headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Basic " + base64.b64encode(f"{self.jira_user}:{self.jira_api_token}".encode()).decode()
    }
    self.base_url="http://127.0.0.1:8000"
    self.db_headers={
      "Authorization":"Token "+self.db_token
    }

  def get_jira_tickets(self):
    """Getting data from Jira API"""
    data=[]
    try:
      response = requests.request("GET",self.jira_url,headers=self.headers,auth=self.auth)
      tickets=json.loads(response.text)
      all_issues=tickets["issues"]

      for issue in all_issues:
        date=issue["fields"]["updated"].split("T")
        created_date=issue["fields"]["created"].split("T")
        dict_obj={
          "key":issue["key"],
          "title":issue["fields"]["summary"],
          "project_name":issue["fields"]["project"]["name"],
          "priority":issue["fields"]["priority"]["name"],
          "updated_date":date[0],
          "ticket_status":issue["fields"]["status"]["name"],
          "creator_email":issue["fields"]["creator"]["emailAddress"],
          "created_date":created_date[0]
        }
        data.append(dict_obj)
      
      return data
    except Exception as e:
      logging.exception(e)

  def add_tickets_to_db(self,data):
    """Add and update ticks in DB's table"""
    API_ENPOINT = self.base_url+"/api/add_update_tickets"
    try:
      r = requests.post(url=API_ENPOINT, json=data, headers=self.db_headers)
      if(r.status_code == 200):
        print("Ticket has been Successful added")
    except Exception as e:
      logging.exception(e)

  def update_ticket_title(self,ticket_id):
    """update tick title"""
    URL=self.jira_url_for_update+ticket_id
    payload=json.dumps({
      "update":{
        "summary": [
          {
            "set": "issue fix v3"
          }
        ]
      }
    })
    try:
      response = requests.request("PUT",URL,data=payload,headers=self.headers,auth=self.auth)
      print(response.text)
    except Exception as e:
      logging.exception(e)

  def get_transition_id(self,ticket_key):
    transition_id= None
    url = "https://rizwanfree.atlassian.net/rest/api/2/issue/"+ticket_key+"/transitions"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url,headers=headers,auth=self.auth)

    # Check if the request was successful
    if response.status_code == 200:
      response_json = json.loads(response.text)
      transitions = response_json['transitions']
      for transition in transitions:
        transition_id=transition['id']
        break
      return transition_id
    else:
        return False

  def mark_ticket_open_to_close(self,ticket_key):
    try:
      """update tick title"""
      # Set the API endpoint and headers
      url = "https://rizwanfree.atlassian.net/rest/api/2/issue/"+ticket_key+"/transitions"
      headers = {
          "Content-Type": "application/json"
      }
      transition_id = self.get_transition_id(ticket_key)
      payload = {
          "transition": {
              "id": str(transition_id)
          }
      }
      # Make the API request to update the ticket status
      response = requests.post(
          url,
          data=json.dumps(payload),
          headers=headers,
          auth=self.auth
      )

      if response.status_code == 204:
        self.close_ticket_with_comment(ticket_key)
        print("Ticket status updated successfully.")
      else:
        print("Error updating ticket status. Status code: {}".format(response.status_code))
    except Exception as e:
      print(e)
    
  def close_ticket_with_comment(self,ticket_id):
    URL="https://rizwanfree.atlassian.net/rest/api/2/issue/"+ticket_id+"/comment"

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    comment = "This ticket has been closed."
    comment_dict = {
        "body": comment
    }

    # Create a JSON payload with the comment list
    payload = {
        "body": comment
    }
    response = requests.post(URL, headers=headers, auth=self.auth, data=json.dumps(payload))

    if response.status_code == 201:
        print("Comment added to Jira issue")
    else:
        print("Failed to add comment to Jira issue")



############ Creating object here ###############
# obj = Jira()
# data=obj.get_jira_tickets()
# obj.add_tickets_to_db(data)
# obj.update_ticket_title('VELOCITY-7')
# obj.close_ticket_with_comment('VELOCITY-6')
# obj.mark_ticket_open_to_close("VELOCITY-5")