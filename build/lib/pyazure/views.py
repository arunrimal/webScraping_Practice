#from django.shortcuts import render
import pyodbc, yaml, os
#from azure.storage.blob import BlobClient
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
print(BASE_DIR)
# module_dir = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, 'config/config.yaml')
print(file_path)
#-----------------------------------------------------------
#file_path2 = os.path.join(BASE_DIR, '/pyazure')
#try:
#    os.mkdir(file_path2)
#except OSError:
#    print ("Creation of the directory %s failed" % file_path2)
#else:
#    print ("Successfully created the directory %s " % file_path2)
#-------------------------------------------------------------

with open(file_path) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    
#def push_to_azure_blob_storage(output, name, folder_name):
#    """Pushes data to Azure blob Storage.

#    Pushes the data specified by user as argument 'output' into Azure blob storage with file name as
#    'name' into the sub-directory 'folder_name' as specfied by the user in arguments 'name' and 
#    'folder_name' respectively.

#    Args:
#      output:
#        An pandas dataframe to csv converted raw encoded variable.
#      name:
#        An string specifying the name of the file which will be stored in Azure blob storage.
#      folder_name:
#        An string specifying the name of the sub directory in which the file will be stored in 
#        Azure blob storage.
        

#    Returns:
#      None
#    """
#    accountname = config['azure_storage_account_name']
#    containerName = config['azure_container_name'] + str(folder_name)
#    connection_string = config['azure_storage_account_connection_string']

#    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=containerName, blob_name=name)
#    blob.upload_blob(output)
    



def get_job_source_data(table_name):
    """Retrives CompanyUUID and JobBoardURL column from job source tables.

    Retrives the CompanyUUID and JobBoardURL column data from table specified by the user in argument
    'table_name' and stores the two column in separate variables and returns them.

    Args:
      table_name:
        An string specifying the name of the table which whose data will be retrived.

    Returns:
      Returns two array consisting of JobBoardURL and CompanyUUID data of the specified table.
    """ 
    CompanyUUID_list = []
    JobBoardURL_list = []
    server= config['oasis_data_server']
    database= config['transaction_database']
    username = config['azure_oasis_username']
    password = config['azure_oasis_password']
    conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password

    cnxn = pyodbc.connect(conn_str)
    cursor=cnxn.cursor()

    cursor.execute(r"select top 1 CompanyUUID, JobBoardURL from {}".format(table_name))
    for row in cursor.fetchall():
        CompanyUUID_list.append(str(row.CompanyUUID))
        JobBoardURL_list.append(str(row.JobBoardURL))

    cnxn.commit()                 
    cursor.close()
    #print(CompanyUUID_list)
    #print(len(CompanyUUID_list))
    print(len(JobBoardURL_list))
    
    #return JobBoardURL_list, CompanyUUID_list
  

get_job_source_data('[Import].[GreenhouseSourceTable]')
