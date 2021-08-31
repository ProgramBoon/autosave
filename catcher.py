# import datetime
# import schedule
# import outinters
# import parser2
# import subprocess
import os



class Catcher(object):

    @classmethod
    def cat(self):
        # открываем файл и чатаем его, проверяем только то, что не знаем (тег dnow)
        f = open("log.txt", 'r+')
        new_data = ''
        for line in f:
            if line.endswith('dnow'+'\n') == 1:
                if os.path.exists(line.split(' ')[0]):
                    statinfo = os.stat(line.split(' ')[0])
                    if statinfo.st_size !=0:
                        # файл есть, размер не нулевой
                        new_data+=(line.replace('dnow', 'good'+'\n'))
                    else:
                        # файл есть, размер нулевой
                        new_data+=line.replace('dnow'+'\n', 'zerosize'+'\n')
                else:
                    #  файла нет или он находится в другой папке, если путь до файла не указан в логе, будет искать в корне
                    new_data+=line.replace('dnow'+'\n','dontexist'+'\n')
            else:
                new_data += line

        f.close()
        f = open("log.txt", 'w+')
        f.write(new_data)
        f.close()


