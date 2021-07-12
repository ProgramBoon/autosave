import xml.etree.ElementTree as xml


class XML:
    fileName: str

    def __init__(self, fileName):
        self.fileName = fileName + ".xml"
        self.openFile()

    def openFile(self):
        try:
            file = open(self.fileName, "r")
        except FileNotFoundError:
            self.createFile()

    # def createFile(self):
    #     rootXML = xml.Element("settings")
    #
    #     text = xml.Element("text")
    #     text.text = "Text"
    #     rootXML.append(text)
    #     list = xml.Element("list")
    #     rootXML.append(list)
    #
    #     item: xml.SubElement
    #
    #     item = xml.SubElement(list, "user")
    #     item.text = "postgres"
    #
    #     item = xml.SubElement(list, "password")
    #     item.text = "xthyjskm2000"
    #
    #     item = xml.SubElement(list, "host")
    #     item.text = "localhost"
    #
    #     item = xml.SubElement(list, "port")
    #     item.text = "4"
    #
    #     item = xml.SubElement(list, "database")
    #     item.text = "keenup"
    #
    #     list = xml.Element("list")
    #     rootXML.append(list)
    #
    #     item: xml.SubElement
    #
    #     item = xml.SubElement(list, "cron")
    #     item.text = "30"
    #
    #     file = open(self.fileName, "w")
    #     file.write(xml.tostring(rootXML, encoding="utf-8", method="xml").decode(encoding="utf-8"))
    #     file.close()

    def parsingFile(self, elements, text=True):
        tree = xml.ElementTree(file=self.fileName)
        rootXML = tree.getroot()
        for element in rootXML.iter(elements):
            if (text):
                return element.text
            return element

