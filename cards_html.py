import copy
true=True

browser_response="""<!DOCTYPE html>
                   <html lang="en">
                       <head>
                           <meta charset="UTF-8">
                           <title>Webex Teams Bot served via Flask</title>
                       </head>
                   <body>
                   <p>
                   <strong>Arun Your Flask web server is up and running!</strong>
                   </p>
                   </body>
                   </html>
                """

default_message=[
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
	           {
                   "type": "TextBlock",
                   "text": "Hi ! what would you like to do?",
                   "weight": "Lighter",
                   "color": "Accent"
               }
               ],
        "actions": [
        {
            "type": "Action.Submit",
            "title": "Start Poll",
            "id": "poll_start",
            "data": {
                        "submit_value": "poll_start"
                    }
        },
                {
            "type": "Action.Submit",
            "title": "stop poll",
            "id": "poll_stop",
            "data": {
                        "submit_value": "poll_stop"
                    }
        },
                {
            "type": "Action.Submit",
            "title": "Poll status",
            "id": "poll_status",
            "data": {
                        "submit_value": "poll_status"
                    }            
        }
                  ]
      }
    }
  ] 
  
  
poll_get_question_count=[
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
	           {
                   "type": "TextBlock",
                   "text": "Enter the number of questions:",
                   "weight": "Lighter",
                   "color": "Accent"
               },
               {
                            "type": "Input.Number",
                            "id": "polls_questions_count"
                        }
               ],
        "actions": [
        {
            "type": "Action.Submit",
            "title": "Next>>",
            "id": "poll_count",
            "data": {
                        "submit_value": "poll_count"
                    }
        }
                  ]
      }
    }]
  


poll_form_template = [{
   "contentType":"application/vnd.microsoft.card.adaptive",
   "content":{
      "type":"AdaptiveCard",
      "version":"1.0",
      "body":[
	           {
                   "type": "TextBlock",
                   "text": "Poll / Quiz creation form",
                   "weight": "Lighter",
                   "color": "Accent"
               },
               {
                   "type": "Input.Text",
                   "placeholder": "Enter poll name",
                   "id": "poll_name",
                   "separator": true,
                   "spacing": "ExtraLarge",
                   "maxLength": 50,
                   "value": ""
               },
			   {
                 "type": "Input.Text",
                 "placeholder": "Enter description about the poll",
                 "isMultiline": true,
                 "id": "poll_description"
               },               
			   {
                 "type": "Input.Text",
                 "placeholder": "Enter participants email ids seprated by commas or a teamspace name. Example: abc@de.com , fgh@ij.com or chn-bsft",
                 "isMultiline": true,
                 "id": "poll_participants"
               },
			   {
            "type": "Input.Toggle",
            "title": "Share results with participants",
            "value": "false",
            "wrap": true,
            "id": "share_public",
            "separator": true
        } ,       {
            "type": "Input.Toggle",
            "title": "Anonymous poll. (Participant id is not collected)",
            "value": "false",
            "wrap": true,
            "id": "poll_anonymous",
            "separator": true
        },
	    {
            "type": "TextBlock",
            "text": "Enter poll duration in minutes: (max 4320)",
            "weight": "Lighter",
            "color": "Accent",
            "separator": true
        },        
        {
            "type": "Input.Number",
            "placeholder": "poll duration in minutes",
            "id": "poll_duration"
        }     
             ],
      "actions":[
         {
            "type":"Action.Submit",
            "title":"submit",
            "id":"submit_button",
            "data": {
                        "submit_value": "poll_creator_form"
                    }
         
          }
      
                 ]
   
       }
   }]
   
QA_template={
                   "type": "Input.Text",
                   "placeholder": "your QA here",
                   "id": "QAC"
                }


poll_preview_template=[
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
	           {
                   "type": "TextBlock",
                   "text": "This is Preview form -> click 'Publish' or 'Abort' ",
                   "weight": "Bolder",
                   "color": "Attention"
               },        
	           {
                   "type": "TextBlock",
                   "text": "poll name",
                   "weight": "Bolder",
                   "color": "Accent"
               },
	           {
                   "type": "TextBlock",
                   "text": "poll description",
                   "weight": "Lighter",
                   "color": "Accent"
               }
                ],
        "actions": [
        {
            "type": "Action.Submit",
            "title": "Publish",
            "id": "poll_publish",
            "data": {
                        "submit_value": "poll_publish",
                        "poll_id": "",                        
                    }
        },
        {
            "type": "Action.Submit",
            "title": "Abort",
            "id": "poll_abort",
            "data": {
                        "submit_value": "poll_abort",
                        "poll_id": "",                        
                    }
        }        
                  ]
               }
    }]
  
poll_enduser_form_template=[
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
	           {
                   "type": "TextBlock",
                   "text": "poll name",
                   "weight": "Bolder",
                   "color": "Accent"
               },
	           {
                   "type": "TextBlock",
                   "text": "poll description",
                   "weight": "Lighter",
                   "color": "Accent"
               }
                ],
        "actions": [
        {
            "type": "Action.Submit",
            "title": "submit",
            "id": "poll_count",
            "data": {
                        "submit_value": "poll_enduser_submit",
                        "poll_id": "",                        
                    }
        }
                  ]
               }
    }]
  

def poll_form_generator(poll_qc=2):
    '''based on user input this function inserts 
       the number of question and answers requred to
       the template: QA_template_copy'''       
    QA_template_copy = copy.deepcopy(QA_template)
    poll_form_copy = copy.deepcopy(poll_form_template) 
    
    for i in range(1,poll_qc+1):
      QA_template_copy['placeholder']="Answer" 
      QA_template_copy['id']="A{}".format(poll_qc+1-i)
      poll_form_copy[0]['content']['body'].insert(3,QA_template_copy.copy())
      QA_template_copy['placeholder']="{}: Question".format(poll_qc+1-i) 
      QA_template_copy['id']="Q{}".format(poll_qc+1-i)     
      poll_form_copy[0]['content']['body'].insert(3,QA_template_copy.copy())

    return poll_form_copy

'''
poll_creator_form submitted output ()
  "inputs": {
    "submit_value": "poll_creator_form",
    "poll_participants": "arunman@cisco.com, amani@broadsoft.com, abc@def.com",
    "poll_name": "Team Lunch ",
    "poll_description": "Team Lunch poll description ",	
    "Q1": "what type of food ?",
    "A1": "veg, non-veg, no meals",
    "Q2": "suggest a restraunt",
    "A2": "",
    "share_public": "true",
    "poll_anonymous": "false",
    "poll_duration": "600"
  }
'''  
Q_endform_template = {
       "type": "TextBlock",
       "text": "poll name",
       "weight": "Bolder",
       "color": "Accent"
   }

A_choiceset_template = {                
            "type": "Input.ChoiceSet",
            "placeholder": "Placeholder text",
            "choices": [],
            "style": "expanded",
            "id": "choice1"
        }

A_textinput_template = {
            "type": "Input.Text",
            "placeholder": "Enter text",
            "isMultiline": true,
            "maxLength": 300,
            "id": "A1T"
           }

def textblock_generator(Qtext):
      Q_endform =  Q_endform_template.copy()
      Q_endform['text'] = Qtext
      return Q_endform
 
def A_textinput_generator(k):
     A_textinput_copy = A_textinput_template.copy()
     A_textinput_copy['id'] = k
     return A_textinput_copy
 
def A_choiceset_generator(choiceList,k):
     A_choiceset_copy = copy.deepcopy(A_choiceset_template) 
     A_choiceset_copy['id'] = k
     i=0
     for citems in choiceList:
         i+=1
         A_choiceset_copy['choices'].append({'title':citems,'value':str(i)})
     return A_choiceset_copy

def poll_preview_form_generator(poll_creator_form , poll_id): 
    ''' receives the form submitted by poll creator. Using  this we 
        generate the preview form'''
    poll_preview_form_copy = copy.deepcopy(poll_preview_template)
    poll_creator_form_copy = copy.deepcopy(poll_creator_form)   
    #copy poll name from creator submission form to enduser form
    poll_preview_form_copy[0]['content']['body'][1]['text'] = poll_creator_form_copy['poll_name']
    #copy poll description
    poll_preview_form_copy[0]['content']['body'][2]['text'] = poll_creator_form_copy['poll_description']
    
    #copy poll_id to publish and abort actions of submit button
    poll_preview_form_copy[0]['content']['actions'][0]['data']['poll_id'] = poll_id  
    poll_preview_form_copy[0]['content']['actions'][1]['data']['poll_id'] = poll_id  
    
    #remove all other items except QA items
    rem_list=['submit_value','poll_participants','poll_name','poll_description','share_public','poll_anonymous','poll_duration']
    for rem_key in rem_list:
       poll_creator_form_copy.pop(rem_key)     
    for key in poll_creator_form_copy.keys():
       if "Q" in key:
          question = poll_creator_form_copy.get(key)
          poll_preview_form_copy[0]['content']['body'].append(textblock_generator(question))
       elif "A" in key:
          answer = poll_creator_form_copy.get(key) 
          if ',' in answer:
              multi_choice = answer.split(',')
              poll_preview_form_copy[0]['content']['body'].append(A_choiceset_generator(multi_choice,key))
          else:
              poll_preview_form_copy[0]['content']['body'].append(A_textinput_generator(key))                                 
    return poll_preview_form_copy
     
     
def poll_enduser_form_generator(poll_creator_form,poll_id): 
    ''' receives the form submitted by poll creator. Using  this we 
        generate the end user form'''
    poll_enduser_form_copy = copy.deepcopy(poll_enduser_form_template)
    poll_creator_form_copy = copy.deepcopy(poll_creator_form)
    #copy poll name from creator submission form to enduser form
    poll_enduser_form_copy[0]['content']['body'][0]['text'] = poll_creator_form_copy['poll_name']
    #copy poll description
    poll_enduser_form_copy[0]['content']['body'][1]['text'] = poll_creator_form_copy['poll_description']
    #copy poll_id to publish and abort actions of submit button
    poll_enduser_form_copy[0]['content']['actions'][0]['data']['poll_id'] = poll_id      
    #remove all other items except QA items
    rem_list=['submit_value','poll_participants','poll_name','poll_description','share_public','poll_anonymous','poll_duration']
    for rem_key in rem_list:
       poll_creator_form_copy.pop(rem_key)     
    for key in poll_creator_form_copy.keys():
       if "Q" in key:
          question = poll_creator_form_copy.get(key)
          poll_enduser_form_copy[0]['content']['body'].append(textblock_generator(question))
       elif "A" in key:
          answer = poll_creator_form_copy.get(key) 
          if ',' in answer:
              multi_choice = answer.split(',')
              poll_enduser_form_copy[0]['content']['body'].append(A_choiceset_generator(multi_choice,key))
          else:
              poll_enduser_form_copy[0]['content']['body'].append(A_textinput_generator(key))                                 
    return poll_enduser_form_copy
    
    