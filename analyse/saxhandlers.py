from xml.sax.handler import ContentHandler
from datetime import datetime
from xml.sax import make_parser
import util.datetimeutils


import sys

class LabelHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'label') :
            self.build.number = attrs["value"];

class ProjNameHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'projectname') :
            self.build.name = attrs["value"];

class TimeStampHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'cctimestamp') :
            self.build.start_time = datetime.strptime(attrs["value"], "%Y%m%d%H%M%S") ;

class ResultHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'logfile') :
            self.build.is_passed = attrs["value"].find('Lbuild') > -1

class LastPassHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'lastsuccessfulbuild') :
            self.build.last_pass = datetime.strptime(attrs["value"], "%Y%m%d%H%M%S")

class LastBuildHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'lastbuild') :
            self.build.last_build = datetime.strptime(attrs["value"], "%Y%m%d%H%M%S")

class BuildTimeHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "build") :
            build_time = util.datetimeutils.evaluate_time_to_seconds(attrs["time"])
            self.build.build_time = build_time

class CommitHandler(ContentHandler):
    def __init__(self, build):
        self.build = build
        self.should_capture = False
        self.is_user = False
        self.is_revision = False
        self.user = ""
        self.revision = ""

    def startElement(self, name, attrs):
        self.buffer = ""
        if name == 'modification':
            self.should_capture = True            
        if name == 'user':
            self.is_user = True
        if name == 'revision':
            self.is_revision = True

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        if self.should_capture:
            if name == 'user':
                self.user = self.buffer
            if name == 'revision':
                self.revision = self.buffer

        if name == 'modification':
            self.build.add_commitor(self.user, self.revision)
            self.should_capture = False
            self.is_user = False
            self.is_revision = False
            self.user = ""
            self.revision = ""            

class MultipleHandlers(ContentHandler):
    def __init__(self, build):
        self.handlers = [LabelHandler(build), ProjNameHandler(build), TimeStampHandler(build), ResultHandler(build),
                         LastPassHandler(build), LastBuildHandler(build), BuildTimeHandler(build), CommitHandler(build)]

    def startElement(self, name, attrs):
        for handler in self.handlers :
            handler.startElement(name, attrs)

    def characters(self, data):
        for handler in self.handlers :
            handler.characters(data)

    def endElement(self, name):
        for handler in self.handlers :
            handler.endElement(name)

