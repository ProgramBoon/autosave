import cre
import sys
import os
import time
import datetime
import schedule
import outinters
import parser2

import requests
import simplejson as json

from os.path import getctime
import subprocess
import catcher
# os.environ['PATH'] = '/usr/lib/postgresql/12/bin/pg_dump'

# sys.path.append(os.getcwd() + '/auto.lib')




now = datetime.datetime.now()

class ScheduleManager(object):
    _schedtime: int
    # парсим хмл
    pats = parser2.Parsert.paret()
    # print(pats[5][0])


    def __init__(self):
        z=0


    @classmethod
    def alott(self):
        n: int = 0
        # разбор информации о работах
        while (n <= len(ScheduleManager.pats)-1):
            try:
                # информация о бд
                if type(ScheduleManager.pats[n]) != list:
                    ScheduleManager.user = ScheduleManager.pats[n]
                    n += 1
                    ScheduleManager.password = ScheduleManager.pats[n]
                    n += 1
                    ScheduleManager.host = ScheduleManager.pats[n]
                    n += 1
                    ScheduleManager.dbname = ScheduleManager.pats[n]
                    n += 1
                    ScheduleManager.port = ScheduleManager.pats[n]
                    n += 1
                    ScheduleManager.server = ScheduleManager.pats[n]
                    n += 1
                else:
                    # информация о задаче, указывается в <task>
                    ScheduleManager.sql = ScheduleManager.pats[n][0]
                    # print(ScheduleManager.pats[n][1]) cron
                    ScheduleManager.atime = ScheduleManager.pats[n][2]
                    ScheduleManager.day = ScheduleManager.pats[n][3]
                    # создание работы
                    self.run()

                    n+=1

            except:
                print('err')

        while True:
            schedule.run_pending()
            ## заменить на переменную
            ## time.sleep(1)
        ## for item in ScheduleManager.pats:
        ##     print(item)
        ## ScheduleManager.dbname = ScheduleManager.pats[item]
            ## ScheduleManager.password



    @staticmethod
    def job(sql,password,user,host,dbname,port,server):

        try:

            ScheduleManager.dbfull = []
            x = now.strftime('%Y_%m_%d')
            # словарь замен, заменяем переменные их значениями, подменяем символы с которыми возникают проблемы у хмл или виндовс
            d = {'{password}': password, "{user}": user, "{host}":host,"{dbname}":dbname,"{x}": x, "{port}":port, "{A}":"&&", "{q}":","}
            sql = ScheduleManager.replace_all(sql, d)

            # запускаем команду скл
            p = os.popen(sql)
            # print('done')
            p.close()
            ## with outinters.OutputInterceptor() as output:
            ##     eval(sql.replace("{password}",password))
            ## os.system(ScheduleManager.listToString(output))

            # заносим информацию в лог, нужно для отлавливания
            t = ScheduleManager.listToString(sql).split(" ")
            lenw = len(t)
            # определяем операционную систему ("TO DISK = N'") - виндовс, иначе - линукс, в зависимости от ОС имя файла находится в разных местах строки
            if sql.find("TO DISK = N'") != -1:

                q = [(sql.split("TO DISK = N'")[1].split("' ")[0]), ' ', "dnow", '\n']
                temppath = (sql.split("TO DISK = N'")[1].split("' ")[0])
            else:

                q = [t[lenw - 1].replace('"', ''), ' ', "dnow", '\n']
                temppath = (t[lenw - 1].replace('"', ''))

            q = ''.join(q)
            ScheduleManager.log = open('log.txt', 'a+')
            ScheduleManager.log.write(q)
            ScheduleManager.log.close()

            # заносим информацию в бд
            str = ''.join(temppath)
            file = str
            # print(str)
            # путь
            way = os.path.abspath(file)

            # время
            datet = datetime.datetime.fromtimestamp(getctime(file)).strftime('%Y-%m-%d %H:%M:%S')
            # размер
            size = os.path.getsize(os.path.abspath(file))
            sizemb=size/1024/1024
            # to server
            url = 'http://:4999/post/'
            myobj = {"host": "'"+host+"'", "name": "'"+way+"'", "date": "'"+datet+"'", "size": sizemb, "server" : "'"+server+"'"}
            try:
                requests.post(url, data=json.dumps(myobj),headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
            except Exception as e:
                # отправляем сообщение об ошибке
                errurl = 'http://:4999/posterr/'
                stre = str(e)
                obj = {"server": "'"+server+"'", "content": "'"+stre+"'"}
                requests.post(errurl, data=obj, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
            # проверяем наличие и размер дампа
            ScheduleManager.jobcatch()

        except Exception as e:
            print(e)


    @staticmethod
    def jobcatch():
        x = catcher.Catcher()
        x.cat()

    @staticmethod
    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @staticmethod
    def listToString(s):
        # initialize an empty string
        str1 = ""
        # traverse in the string
        for ele in s:
            str1 += ele
            # return string
        return str1

    #
    # @staticmethod
    # def compl():
    #     return (exec(ScheduleManager.sql))



    @classmethod
    def run(self):
        # разбор по дням, если день не равен англ названию, работа будет выполнятся ежедневно
        if ScheduleManager.day == "monday":
            schedule.every().monday.at(ScheduleManager.atime).do(self.job,ScheduleManager.sql,ScheduleManager.password,ScheduleManager.user,ScheduleManager.host,ScheduleManager.dbname,ScheduleManager.port,ScheduleManager.server)
        elif ScheduleManager.day == "tuesday":
            schedule.every().tuesday.at(ScheduleManager.atime).do(self.job,ScheduleManager.sql,ScheduleManager.password,ScheduleManager.user,ScheduleManager.host,ScheduleManager.dbname,ScheduleManager.port,ScheduleManager.server)
        elif ScheduleManager.day == "wednesday":
            schedule.every().wednesday.at(ScheduleManager.atime).do(self.job,ScheduleManager.sql,ScheduleManager.password,ScheduleManager.user,ScheduleManager.host,ScheduleManager.dbname,ScheduleManager.port,ScheduleManager.server)
        elif ScheduleManager.day == "thursday":
            schedule.every().thursday.at(ScheduleManager.atime).do(self.job,ScheduleManager.sql,ScheduleManager.password,ScheduleManager.user,ScheduleManager.host,ScheduleManager.dbname,ScheduleManager.port,ScheduleManager.server)
        elif ScheduleManager.day == "friday":
            schedule.every().friday.at(ScheduleManager.atime).do(self.job,ScheduleManager.sql,ScheduleManager.password,ScheduleManager.user,ScheduleManager.host,ScheduleManager.dbname,ScheduleManager.port,ScheduleManager.server)
        elif ScheduleManager.day == "saturday":
            schedule.every().saturday.at(ScheduleManager.atime).do(self.job,ScheduleManager.sql,ScheduleManager.password,ScheduleManager.user,ScheduleManager.host,ScheduleManager.dbname,ScheduleManager.port,ScheduleManager.server)
        elif ScheduleManager.day == "sunday":
            schedule.every().sunday.at(ScheduleManager.atime).do(self.job,ScheduleManager.sql,ScheduleManager.password,ScheduleManager.user,ScheduleManager.host,ScheduleManager.dbname,ScheduleManager.port,ScheduleManager.server)
        else:
            schedule.every().day.at(ScheduleManager.atime).do(self.job,ScheduleManager.sql, ScheduleManager.password, ScheduleManager.user,ScheduleManager.host, ScheduleManager.dbname,ScheduleManager.port,ScheduleManager.server)
        # код для отладки, запускает работу сразу же
        # self.job(ScheduleManager.sql, ScheduleManager.password, ScheduleManager.user,ScheduleManager.host, ScheduleManager.dbname,ScheduleManager.port,ScheduleManager.server)

