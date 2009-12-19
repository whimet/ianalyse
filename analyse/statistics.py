from datetime import datetime, timedelta
import os
import re
import csv

from django.db import settings
from xml.sax.handler import ContentHandler
from xml.sax import parse, parseString
from lxml import etree

from util.datetimeutils import *
from analyse.openFlashChart import Chart
import analyse.ordered_dic
from analyse.config import Config, Configs
from analyse.saxhandlers import *
from analyse.tar import Tar

class NDaysStatistics :
    def __init__(self, builds):
        self.builds = builds
        self.project_id = builds.project_id()

    def pass_rate(self):
        total  = self.builds.total_count()
        passed = self.builds.pass_count()
        failed = total - passed        
        
        chart = Chart()
        element1 = Chart()
        element1.values =  [passed, failed]
        element1.type = "pie"
        element1.alpha = 0.6
        element1.animate = False
        element1.angle = 35
        element1.tip = '#val# of #total#<br>#percent# of 100%';
        element1.colours = ['#1C9E05','#FF368D']

        chart.elements = [element1]
        chart.title = {"text": str(self.builds.total_count()) + ' Runs', "style": "{font-size: 15px; font-family: Times New Roman; font-weight: bold; color: #4183C4; text-align: center;}" }
        chart.bg_colour = "#FFFFFF" 
        return chart.create()

    def per_build_time(self):
        chart = Chart()

        values, labels, max_time = self.builds.per_build_time();
        element = Chart()
        element.type = "bar_glass"
        element.values = values
        

        chart.elements = [element]
        chart.y_axis = { "min": 0, "max": max_time + 10, "steps": max_time / 10}
        chart.x_axis = {"labels" : {"labels" : labels, "visible-steps": 2, "rotate": 90}}
        return chart.create()

    def successful_rate(self):
        chart = Chart()

        element = Chart()
        element.type = "line"
        element.dot_style = { "type": "dot" }
        element.width = 2
        element.colour = "#C4B86A"
        element.fill = "#1C9E05"
        element.fill_alpha = 0.7

        values, min_date, max_date = self.builds.pass_rate_by_day()

        element.values = values
        chart.elements = [element]
        all_percentage = []

        for i in range(110):
            all_percentage.append(str(i) + "%");

        chart.y_axis   = { "min": 0, "max": 110, "steps": 10,  "labels" : {"labels" : all_percentage, "steps" : 20}}
        chart.x_axis   = { "min": min_date, "max": max_date, "steps": 86400,
                           "labels": { "text": "#date:Y-m-d at H:i#", "steps": 86400, "visible-steps": 2, "rotate": 90 }}
        chart.title    = { "text": "Pass rate over time."}
        return chart.create()

    def build_times(self):
        chart = Chart()

        element = Chart()
        element.type = "line"
        element.dot_style = { "type": "dot" }
        element.width = 2
        element.colour = "#0000ff"
        element.fill = "#1C9E05"
        element.fill_alpha = 0.7

        values, min_date, max_date, max_time = self.builds.build_times()

        element.values = values
        chart.elements = [element]
        all_percentage = []

        chart.y_axis   = { "min": 0, "max": max_time + 10, "steps": max_time / 10}
        chart.x_axis   = { "min": min_date, "max": max_date, "steps": 86400,
                           "labels": { "text": "#date:Y-m-d at H:i#", "steps": 86400, "visible-steps": 2, "rotate": 90 }}
        chart.title    = { "text": "Build time over time."}
        return chart.create()

    def __getattr__(self, name):
        if not name.startswith("generate_"):
            raise AttributeError(name)
        field = name[len("generate_"):]
        result = getattr(self, field)()
        
        total_json_file = os.path.join(Configs().find(self.project_id).result_dir(), field + '.txt');

        os.write_to_file(total_json_file, result)
        return lambda : {}
        
        
class GlobalStatistics:
    def __init__(self, project_group):
       self.project_group = project_group

    def projects_comparation(self):
        chart = Chart()
        element = Chart()
        element.type = "bar_stack"
        element.colours = [ '#1C9E05','#FF368D']
        values, names, max =    self.project_group.projects_comparation()
        element.values =  values

        element.keys =  [
            { "colour": '#FF368D', "text": "Failed builds", "font-size": 13 },
            { "colour": '#1C9E05', "text": "Passed builds", "font-size": 13 }]
        element.tip = "#val# runs of #total# in project #x_label#"
        
        chart.title = { "text": "Passed/Failed builds between projects", "style": "{font-size: 20px; color: #F24062; text-align: center;}" }
        chart.x_axis = { "labels": { "labels": names} }
        chart.y_axis = { "min": 0, "max": max + 2, "steps": 2 }
        chart.tooltip =  { "mouse": 2 } 
        chart.elements = [element]

        #for builds in self.project_group:

        return chart.create()
            
        
    def __getattr__(self, name):
        if not name.startswith("generate_"):
            raise AttributeError(name)
        field = name[len("generate_"):]
        result = getattr(self, field)()

        total_json_file = os.path.join(Configs().results_dir(), field + '.txt');
        os.write_to_file(total_json_file, result)
        return lambda : {}
