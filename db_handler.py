import sqlite3
import secrets
import time
import datetime
import json
from cards_html import *

db_name = 'poll_bot.db'
datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'

#functions for SQL queries
def sql_query(col,tab,key,val):
   '''b,c,d,e = "end_user_form","pollmaster","poll_id","SDFW342SC"
        a = sql_query(b,c,d,e)    
        print(a)
        this might seem to pose security risk but in this app 
        we dont get query from end user'''
   conn = sqlite3.connect(db_name)
   cur = conn.cursor()   
   val="\""+val+"\""
   tab="\""+tab+"\""
   #SELECT poll_name FROM pollmaster WHERE share_public="true"
   qry = 'SELECT {} FROM {} WHERE {}={}'.format(col,tab,key,val)
   print(qry)
   cur.execute(qry)
   rows = cur.fetchall()
   conn.close()
   return rows
   
def sql_query2(query,var):
   conn = sqlite3.connect(db_name)
   #conn.row_factory =sqlite3.Row
   cur = conn.cursor() 
   cur.execute(query,var)
   rows = cur.fetchall()
   conn.close()
   return rows

def sql_query3(query):
   conn = sqlite3.connect(db_name)
   #conn.row_factory =sqlite3.Row
   cur = conn.cursor() 
   cur.execute(query)
   rows = cur.fetchall()
   conn.close()
   return rows

def sql_query4(query,var):
   conn = sqlite3.connect(db_name)
   #conn.row_factory =sqlite3.Row
   cur = conn.cursor() 
   cur.execute(query,var)
   rows = cur.fetchone()
   conn.close()
   return rows
   
def sql_edit(query,var):
   conn = sqlite3.connect(db_name)
   conn.row_factory =sqlite3.Row
   cur = conn.cursor()
   cur.execute(query,var)
   conn.commit() 
   conn.close()
   
def sql_create(query):
   conn = sqlite3.connect(db_name)
   conn.row_factory =sqlite3.Row
   cur = conn.cursor() 
   cur.execute(query)
   rows = cur.fetchall()
   conn.commit()   
   conn.close() 
   

# Create table
# create_tbl = '''CREATE TABLE IF NOT EXISTS pollmaster                       
             # (poll_id  TEXT PRIMARY KEY  NOT NULL, 
             # poll_participants TEXT NOT NULL ,
             # room TEXT NOT NULL, 
             # poll_owner TEXT NOT NULL,             
             # poll_name TEXT, 
             # share_public TEXT NOT NULL,  
             # poll_anonymous TEXT NOT NULL, 
             # poll_duration TEXT NOT NULL, 
             # creation_time TEXT NOT NULL, 
             # table_pollid TEXT NOT NULL,
             # end_user_form TEXT NOT NULL)''' 

create_tbl = '''CREATE TABLE IF NOT EXISTS pollmaster                       
             ("SNO"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             poll_id NOT NULL, 
             poll_participants TEXT  ,
             room TEXT , 
             poll_owner TEXT ,             
             poll_name TEXT, 
             share_public TEXT ,  
             poll_anonymous TEXT , 
             poll_duration TEXT , 
             creation_time TEXT , 
             table_pollid TEXT ,
             end_user_form JSON )'''
             
sql_create(create_tbl)
             
def save_formdetails(room_name,person_name,submit_json):
    room = str(room_name.title)
    poll_id = str(secrets.token_urlsafe(8))
    poll_owner = str(person_name.displayName)
    poll_participants = str(submit_json.inputs['poll_participants'])
    poll_name = str(submit_json.inputs['poll_name'])
    share_public = str(submit_json.inputs['share_public'])
    poll_anonymous = str(submit_json.inputs['poll_anonymous'])
    poll_duration = str(submit_json.inputs['poll_duration'])
    creation_time = str(int(time.time()))
    table_pollid = str("table_" + poll_id)
    
    preview_form = poll_preview_form_generator(submit_json.inputs , poll_id)
    enduser_form = json.dumps(poll_enduser_form_generator(submit_json.inputs , poll_id) )
    qry = '''
        INSERT INTO pollmaster (poll_id, poll_participants, room,
                                poll_owner, poll_name, share_public, 
                                poll_anonymous, poll_duration, creation_time,
                                table_pollid,end_user_form) VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?) '''
                        
    sql_edit(qry,(poll_id, poll_participants, room,poll_owner,
                  poll_name, share_public,poll_anonymous, poll_duration, 
                  creation_time,table_pollid,enduser_form))
                 
    print("entry added in database")
    return preview_form
    
def poll_abort_db(poll_id):
    qry = '''DELETE FROM pollmaster WHERE poll_id=?'''
    sql_edit(qry,(poll_id,))
    print("poll id: ", poll_id, " removed from db")
    

def fetch_end_user_form(poll_id_value):
    euf = sql_query("end_user_form","pollmaster","poll_id",poll_id_value)
    #print("============",json.loads(euf))
    return json.loads(euf[0][0])
    
def get_poll_participants(poll_id_value):
    participants = sql_query("poll_participants","pollmaster","poll_id",poll_id_value)
    return  participants[0][0].split(",")
         
def create_enduser_table(poll_id_value):
    #columns poll_id , msg_id , time_stamp, room_person_name, A1, A2, A3
    #extract choices value and store in array
    polltable = sql_query("table_pollid","pollmaster","poll_id",poll_id_value)
    create_tbl = '''CREATE TABLE IF NOT EXISTS "''' + polltable[0][0]                  
    create_tbl = create_tbl + '''" ("SNO" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 poll_id NOT NULL, 
                 msg_id NOT NULL,
                 room_name TEXT  ,
                 email_id TEXT  ,
                 rcvd_time TEXT  '''
                 
    #get the number of answers
    euf_dump = sql_query("end_user_form","pollmaster","poll_id",poll_id_value)
    euf_dump = json.loads(euf_dump[0][0])
    ans_count = int((len(euf_dump[0]['content']['body']) - 2) / 2 ) 
    ans_column = ""
    for i in range(ans_count):
       ans_column = ans_column + ", A" + str(i+1) + " TEXT"
    create_tbl = create_tbl +  ans_column + ")"
    print("Table created: ", polltable[0][0])
    sql_create(create_tbl) 
    
def save_msg_id(poll_id_value, msg_id , email_id, room_name):
    polltable = sql_query("table_pollid","pollmaster","poll_id",poll_id_value)
    qry = '''INSERT INTO "''' + str(polltable[0][0]) 
    qry = qry + '''" (poll_id, msg_id, room_name, email_id, rcvd_time) VALUES 
                    (?,?,?,?,?) '''
    rcvd_time = str(datetime.datetime.now())   
    print("==========",qry,poll_id_value, msg_id, room_name,email_id,rcvd_time)    
    sql_edit(qry,(poll_id_value, msg_id,room_name, email_id,rcvd_time))  

def save_enduser_inputs(submit_json,email_id,room_name):
    poll_id = submit_json.inputs['poll_id']
    msg_id = submit_json.messageId
    poll_id_exists = sql_query4('SELECT 1 FROM pollmaster WHERE poll_id=? LIMIT 1', (poll_id,))
    if poll_id_exists is not None:
       polltable = sql_query("table_pollid","pollmaster","poll_id",poll_id) 
       polltable = str(polltable[0][0])
       user_exists = sql_query(1,polltable,"email_id",email_id)
       inputs_copy = copy.deepcopy(submit_json.inputs)
       inputs_copy.pop("poll_id")
       inputs_copy.pop("submit_value")
       update_query = '''UPDATE "''' + polltable + '''" SET '''
       insert_query = '''INSERT INTO "''' + polltable + '''" ('''
       ins_qry_cn = "poll_id, msg_id, room_name, email_id, rcvd_time, "
       rcvd_time = str(datetime.datetime.now())
       ins_qry_val = '''"''' + poll_id + '''",''' + '''"''' + msg_id + '''",''' + '''"''' + room_name + '''",''' + '''"''' + email_id + '''",'''+ '''"''' + rcvd_time + '''",'''
       for i , (ques, ans) in enumerate(inputs_copy.items()): 
           update_query = update_query +  ques + '''="''' + ans + '''" '''
           ins_qry_cn = ins_qry_cn + ques
           ins_qry_val = ins_qry_val + '''"''' + ans + '''"'''
           if i != len(inputs_copy)-1:
              update_query = update_query + ", "
              ins_qry_cn = ins_qry_cn + ", " 
              ins_qry_val = ins_qry_val + ", "              
       update_query = update_query + "WHERE " +  "email_id" + '''="''' + email_id + '''" '''
       insert_query = insert_query + ins_qry_cn + ")" + "VALUES (" +  ins_qry_val + ")"
       print("value of user_exists: ",user_exists)
       if user_exists:
          #UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6
          print("update_query: ",update_query)
          sql_create(update_query)
       else:
          #insert
          print("insert_query: ",insert_query)
          sql_create(insert_query)          
       return "yay! your response is submitted "          
    else:
       return "whew! The Poll/Survey ended"    
    
    

#sample:
# {
  # "id": "Y2lzY29zcGFyazovL3VzL0FUVEFDSE1FTlRfQUNUSU9OLzg0ZTI3NTAwLTkwOTItMTFlYS04N2NkLWM3NmU1YTY4ZWMzMg",
  # "type": "submit",
  # "messageId": "Y2lzY29zcGFyazovL3VzL01FU1NBR0UvZGIzM2NjNDEtOTA4MC0xMWVhLWEwZWYtZGI1M2RhNWE1NWI1",
  # "inputs": {
    # "poll_id": "fP-nYUXyjIc",
    # "submit_value": "poll_enduser_submit",
    # "A4": "anjapaarrrrrr asdf",
    # "A1": "2",
    # "A2": "1",
    # "A3": "3"
  # },
  # "personId": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MGQ1YTRiOS02ZWVmLTQ0MjYtYTkxZC1lODAyOWFjYzBhY2U",
  # "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vYjhkMWU4ZDAtNjNjZC0xMWU4LWE5OGQtYWZiYjZlMjM0NDIx",
  # "created": "2020-05-07T18:42:35.728Z"
# }    
    