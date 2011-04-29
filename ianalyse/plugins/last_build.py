from xml.sax.handler import ContentHandler

class LastBuildPlugin(ContentHandler):
    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'lastbuild') :
            self.last_build = attrs["value"];        
            
    def csv_cell(self):
        return self.last_build

Plugins.register('Last build', LastBuildPlugin())