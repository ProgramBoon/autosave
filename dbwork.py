import pgsql
# importpip install psycopg2-binary cre2
import datetime


class Database:
    _conn = 0

    def insert_data(self, data):
        """ insert multiple vendors into the vendors table  """
        sql = "INSERT INTO public.info(hostname, filepath, date, filesize) VALUES(%s, %s, %s, %s)"
        datesql = "INSERT INTO public.date(date) VALUES(%s);"
        self.conn = None
        try:
        #     dbn = p.parsingFile("database", True)
        #     us = p.parsingFile("user", True)
        #     pas = p.parsingFile("password", True)
        #     hos = p.parsingFile("host", True)

            date_object = "\'"+str(datetime.date.today())+"\'"
            print(date_object)

            try:
                db = pgsql.Connection(database="autsave", user="postgres", password="xthyjskm2000")
                print(db("INSERT INTO public.info(hostname, filepath, date, filesize) VALUES(%s, %s, %s, %s)", data[0], data[1],data[2],data[3]))
                print("INSERT INTO public.info(hostname, filepath, date, filesize) VALUES(%s, %s, %s, %s)", (data[0],
                         data[1], data[2], data[3]))

            except Exception as e: print('l09k',e)
        except Exception as e: print('ii',e)

        print("INSERT INTO public.info(hostname, filepath, date, filesize) VALUES(%s, %s, %s, %s)", str(data[0]),data[1], data[2], data[3])