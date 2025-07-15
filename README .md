# SECURITY MONITORING MODULE

Security Monitoring module:
Here’s the code for the module that implements the connection and runs the queries to store users login in database.
The modules used here are pymysql.
With methods:
•	.connect() 
•	.close() 
•	.cursor.execute() 
•	 .connect.commit()   


CLI for user:
Functions of CLI:
•	In this program regex module was used to get strong and unique password.
•	These passwords are getting crosschecked and validated by the module User_DB_handler that is shown above.
•	After fulfilling the requirements by the conditional checks the valid credentials are stored for later login authentication.
