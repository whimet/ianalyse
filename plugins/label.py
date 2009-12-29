from xml.sax.handler import ContentHandler

class LabelPlugin(ContentHandler):
    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'label') :
            self.label = attrs["value"];        
            
    def csv_cell(self):
        return self.label

Plugins.register('Label', LabelPlugin())