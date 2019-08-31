# EDGAR Data Scraping

**EDGAR**, the **Electronic Data Gathering, Analysis, and Retrieval** system, performs automated collection, validation, indexing, acceptance, and forwarding of submissions by companies and others who are required by law to file forms with the **U.S. Securities and Exchange Commission** (the "SEC"). The database is freely available to the public via the Internet (Web or FTP).

# Details
https://datahub.io/dataset/edgar lists how to access data from Edgar.Tables are extracted from 10Q filings using Python.<br>
Given a company with CIK (company ID) XXX (omitting leading zeroes) and document accession
number YYY (acc-no on search results), programmatically the url is generated to get data
(http://www.sec.gov/Archives/edgar/data/51143/000005114313000007/0000051143-13-000007-
index.html for IBM for example). The file is parsed to locate the link to the 10Q file
(https://www.sec.gov/Archives/edgar/data/51143/000005114313000007/ibm13q3_10q.htm for the
above example). The file is parsed to extract “all” tables in filing and are saved as csv files.
The Docker image is built for whole pipeline with giving user the access to upload csv file and log file into AWS S3

# Docker Commands

**_Command to pull docker image :_**<br><br>
docker pull rishabhjain27/datascrapping:1.0<br><br><br>

**_Command to run docker image :_**<br><br>
docker run rishabhjain27/datascrapping:1.0 python3 datascrapping.py cik=51143 accession=0000051143-13-000007 accessKey=**<aws_accessKey>** secretKey=**<aws_secretKey>** location=us-east-1
<br><br><br>

# Reference

https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm

