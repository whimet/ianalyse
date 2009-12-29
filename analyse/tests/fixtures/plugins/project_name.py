from xml.sax.handler import ContentHandler

class ProjectNamePlugin(ContentHandler):

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'projectname'):
            self.project_name = attrs["value"];

    def csv_cell(self):
        return self.project_name

Plugins.register('project name', ProjectNamePlugin())