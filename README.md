# webexteams-pollbot
pollbot with all expected features

Stories for development:

1. when poll owner submits the form all the data should be inserted as row in the poll.db this includes the preview/end_user_form

2. The db should contain the following in poll.db:
room, poll_owner, poll_id,  poll_participants, poll_name, share_public, poll_anonymous, poll_duration, creation_time, end_user_form, table_pollid

3. The dumped end_user_form should be used to display the preview form

4. Once the poll owner submits publish:
  --  a new table dedicated for this poll should be created with poll_id as name,
  -- the table should contain all questions and answers , participants id,
  --   the dumped end_user_form should be used to broadcast the poll from participants list. (broadcast should know if its space or individual)
  -- as the message is sent an entry should be added in the db with message id (this will be used for deleting the message)
  --   Start and end of the publish message should be conveyed to the user in plain text with poll name.

5. If user aborts the db entry should be removed and the preview message should be deleted.  As negative case, if user click publish again an
error message should be thrown.

6. As participants click submit , their inputs should be added in the newly created pollid.db table 
   -- poll end user form should be deleted only if it is from personal room space.

7. create function that gets the poll status when poll_id is passed.

8. This allows the poll owner and participants (if enabled) to get the status on the fly

9. create a function that handles end of poll.
  -- based on the answers prepare the data
  -- custom answers should not be considered for polling results
  -- include user specific results if anonymous is set to false
  -- publish the data to user and to participants if public is set to true

10. end of poll function should be triggered when:
  -- poll duration expires
  -- if all participants have voted
  -- poll owner ends the poll 

phase-2
1. publish data in graphical way either pdf or jpeg
2. delete all messages sent by poll_bot *where ever applicable 
3. redesign the adapative cards with more fancy wordings and pictures
  
