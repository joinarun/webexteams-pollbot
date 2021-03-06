#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
import re
import time

#custom modules
from ngrok_webhook import *
from db_handler import *

__author__ = "Arun Kumar Mani"
__author_email__ = "arunman@cisco.com"
__contributors__ = [" "]
__copyright__ = "Copyright (c) 2016-2019 Cisco and/or its affiliates."
__license__ = "MIT"

# Initialize the environment
# Create the web application instance
flask_app = Flask(__name__)

# Create the Webex Teams API connection object

#api = WebexTeamsAPI(access_token='your access token here')

#Delete previous webhooks. If local ngrok tunnel, create a webhook
delete_webhooks_with_name(api, name=WEBHOOK_NAME)
delete_webhooks_with_name(api, name="pollbot_ngrok_attachementwebhook")
public_url = get_ngrok_public_url()
if public_url is not None:
   create_ngrok_webhook(api, public_url)
   create_ngrok_attachementwebhook(api, public_url)

# Core bot functionality
              
# Your Webex Teams webhook should point to http://<serverip>:5050/attachements
@flask_app.route('/events', methods=['GET', 'POST'])
def webex_teams_webhook_events():
    """Processes incoming requests to the '/events' URI."""
    if request.method == 'GET':
        return (browser_response)
    elif request.method == 'POST':
        """Respond to inbound webhook JSON HTTP POST from Webex Teams."""

        # Get the POST data sent from Webex Teams
        json_data = request.json
        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(json_data)
        print("\n")


        try:
          # Create a Webhook object from the JSON data
          webhook_obj = Webhook(json_data)
          # Get the room details
          room = api.rooms.get(webhook_obj.data.roomId)
          # Get the message details
          message = api.messages.get(webhook_obj.data.id)
           
          # Get the sender's details
          person = api.people.get(message.personId)
          
          print("NEW MESSAGE IN ROOM '{}'".format(room.title))
          print("FROM '{}'".format(person.displayName))
          print("person========",person)
          print("MESSAGE '{}'\n".format(message.text))
          
          # This is a VERY IMPORTANT loop prevention control step.
          # If you respond to all messages...  You will respond to the messages
          # that the bot posts and thereby create a loop condition.
          me = api.people.me()
          if message.personId == me.id:
              # Message was sent by me (bot); do not respond.
              return 'OK'        
          else:
              # Message was sent by someone else; parse message and respond.
              if "/CAT" in message.text:
                  print("FOUND '/CAT'. Now sending adaptive card")
                  # Get a cat fact
                  #cat_fact = get_catfact()
                  #print("SENDING CAT FACT '{}'".format(cat_fact))
                  # Post the fact to the room where the request was received
                  api.messages.create(room.id, 
                                      text="my adaptive card", 
                                      attachments= default_message
                                      )
              else:
                  #default message
                  api.messages.create(room.id, 
                                      text="This client doesnt support Adaptive cards", 
                                      attachments= default_message
                                     )                
              return 'OK'
        except:
          print("Couldnt retreive message")
          return 'OK'          
            
            
# Your Webex Teams webhook should point to http://<serverip>:5050/attachements
@flask_app.route('/attachements', methods=['GET', 'POST'])
def webex_teams_webhook_attachements():
    """Processes incoming requests to the '/attachements' URI."""
    if request.method == 'POST':
        """Respond to inbound webhook JSON HTTP POST from Webex Teams."""

        # Get the POST data sent from Webex Teams
        json_data = request.json
        print("\n")
        print("Attachement POST RECEIVED:")
        print(json_data)
        print("\n")

        # Create a Webhook object from the JSON data
        webhook_obj = Webhook(json_data)
        # Get the room details
        room = api.rooms.get(webhook_obj.data.roomId)
        # Get the sender's details
        person = api.people.get(webhook_obj.data.personId) 
        
        if webhook_obj.data.type == "submit":
            # Get the message details
            submit_json = api.attachment_actions.get(webhook_obj.data.id)       
            print("NEW MESSAGE IN ROOM '{}'".format(room.title))
            print("FROM '{}'".format(person.displayName))
            print(" Email id: ",person.emails[0])
            print("Input values from submit '{}'\n".format(submit_json))
            
            #bug in webexteamssdk\models\mixins\attachment_action.py", line 73, has to be fixed
            #only then this function works:  submit_json.inputs
            print(submit_json.inputs['submit_value'])
            print(dict(submit_json.inputs))           
            if submit_json.inputs['submit_value'] == "poll_start":
                print("poll_start received")
                api.messages.create(room.id, 
                                    text='Get number of questions', 
                                    attachments= poll_get_question_count
                                   )                
            elif submit_json.inputs['submit_value'] == "poll_count":
                print("poll questions count received:") 
                polls_qc = int(submit_json.inputs['polls_questions_count'])
                print(polls_qc)
                print(poll_form_generator(polls_qc))
                api.messages.create(room.id, 
                                    text='Poll form creator', 
                                    attachments= poll_form_generator(polls_qc)
                                    )                 
            elif submit_json.inputs['submit_value'] == "poll_creator_form":
                print("poll_creator_form submission received, sending preview form:")
                #saves end user form  in db, this function also returns the form
                #this end user fomr is used to publish the poll after preview                   
                preview_form = save_formdetails(room,person,submit_json) 
                print(preview_form)                
                api.messages.create(room.id, 
                                    text='Poll preview form', 
                                    attachments= preview_form
                                    )               
            elif submit_json.inputs['submit_value'] == "poll_publish":
                print("poll_publish received, sending end user  form to all participants")
                #get enduser form
                end_user_form = fetch_end_user_form(submit_json.inputs['poll_id'])
                #get the list of participants
                participants_list = get_poll_participants(submit_json.inputs['poll_id'])
                #remove leading and trailing whitespace
                participants_list = [x.strip() for x in participants_list]
                print("stripped list:",participants_list)
                #remove duplicate entries
                participants_list = list(set(participants_list))
                #get the list of all rooms this Bot is part of
                all_rooms = api.rooms.list(type="group")
                all_room_title = [room.title for room in all_rooms]
                print ("all_room_title: ",all_room_title)
                #validate email ids and rooms
                regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
                participant_check = True                
                for participant in participants_list:
                   if(re.search(regex,participant)):  
                       print(participant,"Valid Email")
                   elif [c for c in all_room_title if c in participant]:  
                       #if its not email id then it should be room title , validate it from all_rooms
                       print(participant, " is valid room")
                   else:
                       participant_check = False
                       error_msg = "email or Team Space: \"" + participant + "\" is invalid. Cannot publish. Start over"
                       print(error_msg)                       
                       api.messages.delete(webhook_obj.data.messageId)
                       poll_abort_db(submit_json.inputs['poll_id'])
                       api.messages.create(room.id, text=error_msg)  
                       break       
                          
                if participant_check:
                   #create a new table 
                   create_enduser_table(submit_json.inputs['poll_id'])
                   for participant in participants_list:
                     email_id = "default"
                     room_name = "default"
                     if(re.search(regex,participant)):                     
                        print("Sending enduser form to email: ",  participant)
                        email_id = participant
                        rsp_msg = api.messages.create(toPersonEmail=participant, 
                                                      text='Poll end user form sent to all participants', 
                                                      attachments= end_user_form)
                        msg_id = rsp_msg.id
                        
                     else:
                          room_id = [room.id for room in all_rooms if room.title in participant]
                          room_name = participant
                          print("Sending enduser form to team space: ",participant , "with room_id: ", room_id[0])
                          rsp_msg = api.messages.create(room_id[0], 
                                              text='Poll end user form sent to all participants', 
                                              attachments= end_user_form)
                          msg_id = rsp_msg.id
                     print("msg_id-------",msg_id)     
                     #save_msg_id(poll_id_value, msg_id , email_id, room_name)
                     save_msg_id(submit_json.inputs['poll_id'] , msg_id,str(email_id) ,str(room_name))
                                  
            elif submit_json.inputs['submit_value'] == "poll_abort":
                print("poll_abort received, removing entry from db")
                poll_abort_db(submit_json.inputs['poll_id'])
                api.messages.delete(webhook_obj.data.messageId)
                api.messages.create(room.id, 
                                    text='poll canceled. Start again',) 
            elif submit_json.inputs['submit_value'] == "poll_enduser_submit":
                print("poll_enduser_submit received, adding entry into db")
                response_val = save_enduser_inputs(submit_json,str(person.emails[0]),str(room.title))
                #api.messages.delete(webhook_obj.data.messageId)
                api.messages.create(room.id, 
                                    text=response_val, 
                                    )                                            
            elif submit_json.inputs['submit_value'] ==  "poll_stop":
                print("poll_stop received")                 
            elif submit_json.inputs['submit_value'] == "poll_status":
                print("poll_status received")                
    return 'OK'       

    
if __name__ == '__main__':
    # Start the Flask web server
    flask_app.run(host='0.0.0.0', port=5050,debug=False)
