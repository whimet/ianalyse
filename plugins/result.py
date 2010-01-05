from xml.sax.handler import ContentHandler

class ResultPlugin(ContentHandler):
    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'logfile') :
            file = attrs["value"]
            if file.find('L') > -1:
                self.log_result = "Passed"
            else:
                self.log_result = "Failed"
    
    def csv_cell(self):
        return self.log_result

Plugins.register('Result', ResultPlugin())