import os
import ibm_db
from dotenv import load_dotenv

load_dotenv()

dsn_hostname = os.getenv("DBHOST")
dsn_uid = os.getenv("DBUID")
dsn_pwd = os.getenv("DBPWD")

dsn_driver = os.getenv("DBDRIVER")
dsn_database = os.getenv("DBDATABASE")
dsn_port = os.getenv("DBPORT")
dsn_protocol = os.getenv("DBPROTOCOL")

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

print(dsn)
