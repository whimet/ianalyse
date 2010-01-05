from xml.sax.handler import ContentHandler

class LastPassedPlugin(ContentHandler):
    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'lastsuccessfulbuild') :
            self.last_passed = attrs["value"];        
            
    def csv_cell(self):
        return self.last_passed

Plugins.register('Last passed', LastPassedPlugin())