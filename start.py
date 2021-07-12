import cre
import sys
import os
import datetime
import schedule
sys.path.append(os.getcwd() + '/Keenup.lib')
import time

now = datetime.datetime.now()

class ScheduleManager(object):
    _schedtime: int
    def __init__(self):
        p = cre.XML('ui')
        ScheduleManager.schedtime = int(p.parsingFile("cron", True))

        ScheduleManager.atime = p.parsingFile("atime", True)
        ScheduleManager.wait = p.parsingFile("wait", True)
        ScheduleManager.sql = p.parsingFile("sql", True)

        ScheduleManager.dbn =p.parsingFile("database",True)
        ScheduleManager.us = p.parsingFile("user", True)
        ScheduleManager.pas = p.parsingFile("password", True)
        ScheduleManager.hos = p.parsingFile("host", True)


    def insert_data(self, data):
        """ insert multiple vendors into the vendors table  """
        sql = "INSERT INTO datacatch(keyname , value) VALUES(%s, %s)"
        datesql = "INSERT INTO public.date(date) VALUES(%s);"
        self.conn = None
        try:
            p = cre2.XML('ui')
            dbn = p.parsingFile("database", True)
            us = p.parsingFile("user", True)
            pas = p.parsingFile("password", True)
            hos = p.parsingFile("host", True)

            date_object = "\'"+str(datetime.date.today())+"\'"
            print(date_object)

            try:
                self.conn = psycopg2.connect(dbname=dbn, user=us, password=pas, host=hos)

                # create a new cursor
                cur = self.conn.cursor()
                cur.execute(datesql, (date_object,))
                for i in data:
                      cur.execute(sql, (i, data[i]))

                # commit the changes to the database
                self.conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    @staticmethod
    def job():
        # print(ScheduleManager.compl())
        # x = 'cmd /k '+ ScheduleManager.compl()
        # print(x)
        os.system("pg_dump -U postgres -h localhost keenup > 2021_07_12_keenup.pgsql.backup")
        os.system("date")

    @staticmethod
    def compl():
        return ('pg_dump -U '+ScheduleManager.us+' -h '+ScheduleManager.hos+" "+ScheduleManager.dbn+'> '+now.strftime("%Y_%m_%d")+'_'+ScheduleManager.dbn+'.pgsql.backup')


    @classmethod
    def run(self):
        schedule.every().day.at(ScheduleManager.atime).do(self.job)
        # schedule.every(ScheduleManager.schedtime).seconds.do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(ScheduleManager.schedtime)



