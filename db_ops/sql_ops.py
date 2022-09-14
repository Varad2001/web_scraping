import mysql.connector as conn
import logging
logging.basicConfig(filename="video_scraper.log", level=logging.INFO, format="%(name)s:%(levelname)s:%(asctime)s:%(message)s" )
import os
from dotenv import load_dotenv

# credential for aws rds
endpoint = "videoscraper.cjo7hysuktlq.us-east-1.rds.amazonaws.com"
port = '3306'
region = 'us-east-1'


def create_db(db_name):
    logging.info("\nCreate database request for %s..." %db_name)
    load_dotenv()
    try:
        user = os.environ.get('USER_SQL')
        passwd = os.environ.get('PASS_SQL')
        mydb = conn.connect(host=endpoint, user=user, passwd= passwd, port=port, ssl_ca='SSLCERTIFICATE')
    except Exception as e:
        logging.exception(e)
    cursor = mydb.cursor()
    try :
        cursor.execute("create database %s" % db_name)
        cursor.execute("use %s" % db_name)
        logging.info("Database created successfully.")
    except Exception as e:
        # if the database already exists, use it and delete all of its entries
        if e.args[0] == 1007:
            cursor.execute("use %s" % db_name)
            cursor.execute("drop table videodata")
            logging.info("Database already exists, using it..")
        else :
            logging.exception(e)
            raise e

    query = "create table videodata(" \
            "%s TINYTEXT," \
            "%s TINYTEXT," \
            "%s VARCHAR(20)," \
            "%s VARCHAR(20)," \
            "%s VARCHAR(20)," \
            "%s int)" %('video_url', 'title', 'likes', 'date', 'views', 'comments_num')
    try :
        cursor.execute(query)
        logging.info("Table 'videodata' created.")
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        mydb.close()


def insert_data(db_name,data):
    logging.info("Inserting data to %s..." % db_name)
    load_dotenv()
    try:
        user = os.environ.get('USER_SQL')
        passwd = os.environ.get('PASS_SQL')
        mydb = conn.connect(host=endpoint, user=user, passwd= passwd, port=port, ssl_ca='SSLCERTIFICATE')
        cursor = mydb.cursor()
        cursor.execute("use %s" % db_name)
    except Exception as e:
        logging.exception(e)
        raise e

    query = ("insert into videodata values (%s,%s,%s,%s,%s,%s)")
    try :
        cursor.execute(query, data)
        mydb.commit()
        logging.info("Data inserted successfully.")
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        mydb.close()


def fetch_data(db_name, table_name):
    logging.info("Fetching data from database {}, table {}...".format(db_name,table_name))
    load_dotenv()
    try:
        user = os.environ.get('USER_SQL')
        passwd = os.environ.get('PASS_SQL')
        mydb = conn.connect(host=endpoint, user=user, passwd=passwd, port=port, ssl_ca='SSLCERTIFICATE')
    except Exception as e:
        logging.exception(e)
    cursor = mydb.cursor()
    results = []
    try :
        cursor.execute("use %s" %db_name)
        cursor.execute("select * from %s" %table_name)
        results = cursor.fetchall()
        logging.info("Fetching data successful.")
    except Exception as e:
        logging.exception(e)

    return results


mydb = conn.connect(host=endpoint, user=user, passwd= passwd, port=port, ssl_ca='SSLCERTIFICATE')
cursor = mydb.cursor()
#cursor.execute("show databases")
cursor.execute("use CERN_Lectures")
cursor.execute("select * from videodata")
print(cursor.fetchall())