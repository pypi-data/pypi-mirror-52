import datetime
import urllib

import pyodbc
import pandas as pd

from sqlalchemy import create_engine

def read_sql_to_df(query='', username="", password="", database='',server="",driver='{ODBC Driver 17 for SQL Server}'):
    # Setup connection parameters

    db = database
    u = username
    p = password
    driver= driver
    s=server

    connection_string = 'DRIVER=' + driver + \
                    ';SERVER=' + s + \
                    ';PORT=1433' + \
                    ';DATABASE=' + db + \
                    ';UID=' + u + \
                    ';PWD=' + p 
    params = urllib.parse.quote_plus(connection_string)
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)

    # Read from database
    temp_df = pd.read_sql(query, engine)

    return temp_df
sql_df=read_sql_to_df


def write_df_to_sql(df,table='', username="", password="", database='', server='',
	 if_exists = 'append',chunksize=10000,driver='{ODBC Driver 17 for SQL Server}',
	 update_date=True):
    # Add datestamp to df
    if update_date:
    	df.insert(0, 'update_date', datetime.date.today()) 
    # Setup connection parameters
    
    db = database
    u = username
    p = password
    driver= '{ODBC Driver 17 for SQL Server}'
    s=server

    connection_string = 'DRIVER=' + driver + \
                        ';SERVER=' + s + \
                        ';PORT=1433' + \
                        ';DATABASE=' + db + \
                        ';UID=' + u + \
                        ';PWD=' + p 

    params = urllib.parse.quote_plus(connection_string)

    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)

    # Write (update) df to database.table
    df.to_sql(table, con = engine, if_exists = if_exists, index = False, chunksize=chunksize)
df_sql=write_df_to_sql

def query_sql_without_return(query='', username="", password="", database='',server='',driver= '{ODBC Driver 17 for SQL Server}'):
    # Setup connection parameters
    s = server
    db = database
    u = username
    p = password
    driver= driver

    connection_string = 'DRIVER=' + driver + \
                    ';SERVER=' + s + \
                    ';PORT=1433' + \
                    ';DATABASE=' + db + \
                    ';UID=' + u + \
                    ';PWD=' + p 
    params = urllib.parse.quote_plus(connection_string)
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)

    # Execute query
    connection = engine.connect()
    connection.execute(query)
    connection.close()
query=query_sql_without_return
def connect(username,password,db,server,driver="{ODBC Driver 17 for SQL Server}"):
	constr="DRIVER={};SERVER={};DATABASE={};UID={};PWD={}".format(driver,server,db,username,password)
	cnxn=pyodbc.connect(constr)
	c=cnxn.cursor()
	return cnxn,c
def insert(cursor,table,object,replace=None,commit=True):
	if replace:
		c.execute("delete from {} where {} = ?".format(table,replace),object[replace])
	sql="insert into {} ({})VALUES({})".format(table,
		",".join(list(object.keys())),
		",".join(["?"]*len(object)))
	print(sql)
	c.execute(sql,*list(object.values()))
	if commit:
		cnxn.commit()
	return c
	
if __name__=="__main__":
	creds=["vlad@simportersqlserver","M1crosoftSQL","dg_team","simportersqlserver.database.windows.net"]
	table="carrefour_item_attrs_temp"

	if True and "read":
		sql="select TOP(10) * from {}".format(table)

		print(sql_df(sql,*creds))

	if True and "write":
		
		df=pd.DataFrame([{"Artykul":"101-404-451",}])
		print(df_sql(df,table,*creds))

	if True and "query":
		query("delete from {}".format(table),*creds)

	if True and "insert":
		cnxn,c=connect(*creds)
		insert(c,table,{"Artykul":"101-404-451","Brand":"Huawei"},commit=True)
		insert(c,table,{"Artykul":"101-404-451","Brand":"Apple"},commit=True,replace="Artykul")