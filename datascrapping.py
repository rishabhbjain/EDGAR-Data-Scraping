#libraries imported
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
import os
import logging
import sys
import zipfile,io
import shutil
import json
import time
import datetime
import boto3

## check existance of url
def get_url(cik,accession):
    try:
        if (re.match('[0-9]+',cik) and re.match('[0-9]+',accession)):
            cik_strip = cik.lstrip('0')
            acc = re.sub(r'[-]', r'', accession)
            url = 'http://www.sec.gov/Archives/edgar/data/'
            link = url+ cik_strip +'/'+ acc +'/'+accession+'/-index.html'
            logging.info('Calling the initial URL')
            return link
    except Exception as e:
        logging.info(str(e))
        sys.exit()

def printtable(table):
    printtable = []
    printtrs = table.find_all('tr')
    for tr in printtrs:
        data=[]
        pdata=[]
        printtds=tr.find_all('td')
        for elem in printtds:
            x=elem.text;
            x=re.sub(r"['()]","",str(x))
            x=re.sub(r"[$]"," ",str(x))
            if(len(x)>1):
                x=re.sub(r"[—]","",str(x))
                pdata.append(x)
        data=([elem.encode('utf-8') for elem in pdata])
        printtable.append([elem.decode('utf-8').strip() for elem in data])
    return printtable

def upload_to_s3(Inputlocation,Access_key,Secret_key):
    try:
        buck_name='edgardatascrapping'
        S3_client = boto3.client('s3',Inputlocation,aws_access_key_id= Access_key, aws_secret_access_key= Secret_key)
        print(Inputlocation)
        if Inputlocation == 'us-east-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'us-west-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'us-east-2':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'us-west-2':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'ap-northeast-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'ap-northeast-2':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'ap-northeast-3':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'ap-south-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'ap-southeast-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'ap-southeast-2':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'ca-central-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'cn-north-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'cn-northwest-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'eu-central-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'eu-west-1':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'eu-west-2':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'eu-west-3':
            S3_client.create_bucket(Bucket=buck_name)
        elif Inputlocation == 'sa-east-1':
            S3_client.create_bucket(Bucket=buck_name)
        else:
            #S3_client.create_bucket(Bucket=buck_name,CreateBucketConfiguration={'LocationConstraint': Inputlocation})
            logging.info("Please enter valid location")
            sys.exit()
        S3_client.upload_file("Data_Scrapping.zip", buck_name,"Data_Scrapping.zip")

    except Exception as e:
        print("Error uploading files to Amazon s3" + str(e))
        logging.info(str(e))
        sys.exit()

##log file initialization
root = logging.getLogger()
root.setLevel(logging.DEBUG)

##making directory
try:
    if not os.path.exists('Data_Scrapping'):
        os.makedirs('Data_Scrapping', mode=0o777)
        logging.info("Data_Scrapping folder created")
    else:
        shutil.rmtree(os.path.join(os.path.dirname(__file__),'Data_Scrapping'),ignore_errors=False)
        os.makedirs('Data_Scrapping', mode=0o777)
    logging.info('Data_Scrapping folder cleanup completed')
    if not os.path.exists('Data_Scrapping/extracted_csv'):
        os.makedirs('Data_Scrapping/extracted_csv', mode=0o777)
        logging.info("Data_Scrapping/extracted_csv folder created")
    else:
        shutil.rmtree(os.path.join(os.path.dirname(__file__),'Data_Scrapping/extracted_csv'),ignore_errors=False)
        os.makedirs('Data_Scrapping/extracted_csv', mode=0o777)
        logging.info("Data_Scrapping/extracted_csv folder created")
except Exception as e:
    logging.error(str(e))
    exit()

##output the  log to a file
log = logging.FileHandler('Data_Scrapping/problem1_log.log')
log.setLevel(logging.DEBUG)
#creation of formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log.setFormatter(formatter)
root.addHandler(log)

##print the logs in console
console = logging.StreamHandler(sys.stdout )
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
root.addHandler(console)

## input from user
argLen=len(sys.argv)
Access_key=''
Secret_key=''
Inputlocation=''
cik=''
accession=''

for i in range(1,argLen):
    val=sys.argv[i]
    if val.startswith('cik='):
        pos=val.index("=")
        cik=val[pos+1:len(val)]
        continue
    elif val.startswith('accession='):
        pos=val.index("=")
        accession=val[pos+1:len(val)]
        continue
    elif val.startswith('accessKey='):
        pos=val.index("=")
        Access_key=val[pos+1:len(val)]
        continue
    elif val.startswith('secretKey='):
        pos=val.index("=")
        Secret_key=val[pos+1:len(val)]
        continue
    elif val.startswith('location='):
        pos=val.index("=")
        Inputlocation=val[pos+1:len(val)]
        continue

##checking the entered details
try:
    link = get_url(cik,accession)
    request = requests.get(link)
except Exception as e:
    logging.error(str(e))
    logging.info("Check the entered details")
    quit()

##Generation of URL using acc_no
try:
    html_doc = request.text

    #Getting 10q tag
    soup = BeautifulSoup(html_doc,'lxml')
    a_tags = soup.find_all('a')
    table_tags = soup.find_all('table',class_='tableFile')
    chk = 0
    for table_tag in table_tags:
        for tr in table_tag.find_all('tr'):
                td = tr.find_all('td')
                for row in td:
                    if (str(row.string) == '10-Q'):
                        tr_crt = tr
                        chk = 1
                    if chk == 1:
                        a_tag = tr_crt.find('a')
                        linkq = a_tag.get('href')
                        link10q = ('https://www.sec.gov'+linkq)

    request1 = requests.get(link10q)
    html_doc1 = request1.text
    soup1 = BeautifulSoup(html_doc1,'lxml')
    logging.info("10q link founded %s",link10q)

    #Getting table data using table tag
    table_tags = soup1.find_all('table')
    my_df1=[]
    for table in table_tags:
        for tr in table.find_all('tr'):
            flag = 0
            for td in tr.find_all('td'):
                if('$' in td.get_text() or '%' in td.get_text()):
                    my_df1.append(printtable(table))
                    flag = 1
                    break
            if(flag == 1):
                break
    logging.info("Data Scrapped from tables")
except Exception as e:
    logging.error(str(e))
    quit()

## Transfering data to csv
i = 0
for j in my_df1:

    file = cik+accession+'-'+str(i)+'.csv'
    with open(os.path.join('Data_Scrapping/extracted_csv', file),'w') as outfile:
        df_csv = pd.DataFrame(j)
        df_csv.to_csv(outfile,index = False, header = 0,sep =',',encoding = 'utf-8')
    i = i + 1
    df_csv.iloc[0:0]
logging.info("Data transfered to csv files")

##zipfile creation
zf = zipfile.ZipFile("Data_Scrapping.zip", "w",zipfile.ZIP_DEFLATED)
for dirname, subdirs, files in os.walk("Data_Scrapping"):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()

logging.info('Compiled csv and log file zipped')

##uploading files to aws s3
upload_to_s3(Inputlocation,Access_key,Secret_key)
logging.info("Files uploaded successfully")
