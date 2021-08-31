import xml.etree.ElementTree as ET


tree = ET.parse('ui.xml')
root = tree.getroot()


class Parsert(object):


    @staticmethod
    def paret():
        _Row = []
        for connect in root.findall('connect'):
            # при добавлении новых переменных, следует добавить их отлов сюда
            # инф о бд
            user = connect.find('user').text
            password = connect.find('password').text
            host = connect.find('host').text
            database = connect.find('database').text
            port = connect.find('port').text
            server = connect.find('server').text
            _Row.append(user)
            _Row.append(password)
            _Row.append(host)
            _Row.append(database)
            _Row.append(port)
            _Row.append(server)
            # инф о задании
            Row2 = []
            for task in connect.findall('task'):
                sql = task.find('sql').text
                cron = task.find('cron').text
                atime=task.find('atime').text
                day=task.find('day').text
                wait=task.find('wait').text
                Row2.append(sql)
                Row2.append(cron)
                Row2.append(atime)
                Row2.append(day)
                Row2.append(wait)
                _Row.append(Row2)
                Row2 = []
        return(_Row)
