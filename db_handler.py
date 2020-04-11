import sqlite3
import secrets
import time
from cards_html import *

db_name = 'poll_bot.db'

#functions for SQL queries
def sql_query(query,var):
   conn = sqlite3.connect(db_name)
   conn.row_factory =sqlite3.Row
   cur = conn.cursor() 
   cur.execute(query,var)
   rows = cur.fetchall()
   conn.close()
   return rows

def sql_query2(query):
   conn = sqlite3.connect(db_name)
   conn.row_factory =sqlite3.Row
   cur = conn.cursor() 
   cur.execute(query)
   rows = cur.fetchall()
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
             end_user_form TEXT )'''
             
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
    qry = '''
        INSERT INTO pollmaster (poll_id, poll_participants, room,
                                poll_owner, poll_name, share_public, 
                                poll_anonymous, poll_duration, creation_time,
                                table_pollid,end_user_form) VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?) '''
                        
    sql_edit(qry,(poll_id, poll_participants, room,poll_owner,
                  poll_name, share_public,poll_anonymous, poll_duration, 
                  creation_time,table_pollid,str(preview_form)))
    print("entry added in database")
    return preview_form
    
def poll_abort_db(poll_id):
    qry = '''DELETE FROM pollmaster WHERE poll_id=?'''
    sql_edit(qry,(poll_id,))
    print("poll id: ", poll_id, " removed from db")