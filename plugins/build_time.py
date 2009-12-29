from xml.sax.handler import ContentHandler

class BuildTimePlugin(ContentHandler):
    def startElement(self, name, attrs):
        if (name == "build") :
            self.build_time = attrs["time"]
            
    def csv_cell(self):
        return self.build_time

Plugins.register('build time', BuildTimePlugin())