from xml.sax.handler import ContentHandler

class BuildStartedPlugin(ContentHandler):
    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'cctimestamp') :
            self.started = attrs["value"];
            
    def csv_cell(self):
        return self.started

Plugins.register('Build started', BuildStartedPlugin())