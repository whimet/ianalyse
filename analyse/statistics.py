from datetime import datetime, timedelta
import os
import re
import csv

from django.db import settings
from xml.sax.handler import ContentHandler
from xml.sax import parse, parseString

from util.datetimeutils import *
from analyse.openFlashChart import Chart
import analyse.ordered_dic
from analyse.config import Config, Configs
from analyse.saxhandlers import *
from analyse.tar import Tar

FAILED_BUILD_COLOR_CODE =  '#FF368D'
PASSED_BUILD_COLOR_CODE = '#1C9E05'
BLUE_COLOR_CODE = "#0000ff"

class DateXAxis:
    '''use this class to workaround the bug in open flash chart, if the min date and the max date are equal, browser will hang.'''
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def min_date(self):
        return self.min
    
    def max_date(self):
        if self.min == self.max:
            return self.max + 200
        return self.max

class NDaysStatistics :
    def __init__(self, builds):
        self.builds = builds
        self.project_id = builds.project_id()

    def build_time_over_time(self):
        chart = Chart()

        element = Chart()
        element.type = "line"
        element.dot_style = { "type": "dot" }
        element.width = 2
        element.colour = BLUE_COLOR_CODE
        element.fill = FAILED_BUILD_COLOR_CODE
        element.fill_alpha = 0.7

        values, min_date, max_date, max_time = self.builds.build_times()

        element.values = values
        chart.elements = [element]
        all_percentage = []

        dateXAxis = DateXAxis(min_date, max_date)
        chart.y_axis   = { "min": 0, "max": max_time + 10, "steps": max_time / 10}
        chart.x_axis   = { "min": dateXAxis.min_date(), "max": dateXAxis.max_date(), "steps": 86400,
                           "labels": { "text": "#date:Y-m-d at H:i#", "steps": 86400, "visible-steps": 2, "rotate": 90 }}
        chart.title    = { "text": "Build time over time."}
        return chart.create()

    def overall_pass_rate(self):
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
        element1.colours = [PASSED_BUILD_COLOR_CODE, FAILED_BUILD_COLOR_CODE ]

        chart.elements = [element1]
        chart.title = {"text": str(self.builds.total_count()) + ' Runs', "style": "{font-size: 15px; font-family: Times New Roman; font-weight: bold; color: #4183C4; text-align: center;}" }
        chart.bg_colour = "#FFFFFF" 
        return chart.create()

    def per_build_info(self):
        chart = Chart()

        values, labels, max_time = self.builds.per_build_time();
        element = Chart()
        element.type = "bar_glass"
        element.values = values
        

        chart.elements = [element]
        chart.y_axis = { "min": 0, "max": max_time + 10, "steps": max_time / 10}
        chart.x_axis = {"labels" : {"labels" : labels, "visible-steps": 2, "rotate": 90}}
        return chart.create()

    def pass_rate_by_day(self):
        chart = Chart()

        element = Chart()
        element.type = "line"
        element.dot_style = { "type": "dot" }
        element.width = 2
        element.colour = "#C4B86A"
        element.fill = "#1C9E05"
        element.fill_alpha = 0.7

        n_days_summary = self.builds.get_n_days_summary()

        element.values = n_days_summary.pass_rate_values()
        chart.elements = [element]
        all_percentage = []

        for i in range(110):
            all_percentage.append(str(i) + "%");

        dateXAxis = DateXAxis(n_days_summary.min_timestamp(),  n_days_summary.max_timestamp())
        chart.y_axis   = { "min": 0, "max": 110, "steps": 10,  "labels" : {"labels" : all_percentage, "steps" : 20}}
        chart.x_axis   = { "min": dateXAxis.min_date(), "max":dateXAxis.max_date(), "steps": 86400,
                           "labels": { "text": "#date:Y-m-d at H:i#", "steps": 86400, "visible-steps": 2, "rotate": 90 }}
        chart.title    = { "text": "Pass rate over time."}
        return chart.create()

    def _create_line(self, values, colour, text, width=2):
        element1 = Chart()

        element1.type ='line'
        element1.values = values
        element1.dot_style={ "type": "dot", "dot-size": 5, "colour": colour }
        element1.width = width
        element1.colour = colour
        element1.text = text
        return element1
        
    def run_times_and_pass_count_by_day(self):
        chart = Chart()
        summary = self.builds.get_n_days_summary()
        total_runs_values = summary.total_runs_values();
        
        chart.elements = [self._create_line(summary.total_runs_values(),   BLUE_COLOR_CODE, 'Total runs', 5),
                          self._create_line(summary.passed_runs_values(),  PASSED_BUILD_COLOR_CODE, 'Passed runs'),
                          self._create_line(summary.failed_runs_values(),  FAILED_BUILD_COLOR_CODE, 'Failed runs')]
        chart.title = { "text": "Run times and pass count by day" }
        chart.y_axis = { "min": 0, "max": 20, "steps": 5 }
        
        dateXAxis = DateXAxis(total_runs_values[0].get('x'), total_runs_values[len(summary) - 1].get('x'))
        
        chart.x_axis   = { "min": dateXAxis.min_date(), "max": dateXAxis.max_date(), "steps": 86400,
                           "labels": { "text": "#date:Y-m-d at H:i#", "steps": 86400, "visible-steps": 2, "rotate": 90 }}

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
            { "colour": FAILED_BUILD_COLOR_CODE, "text": "Failed builds", "font-size": 13 },
            { "colour": PASSED_BUILD_COLOR_CODE, "text": "Passed builds", "font-size": 13 }]
        element.tip = "#val# runs of #total# in project #x_label#"
        
        chart.title = { "text": "Passed/Failed builds between projects", "style": "{font-size: 20px; color: #F24062; text-align: center;}" }
        chart.x_axis = { "labels": { "labels": names, "rotate": 45} }
        chart.y_axis = { "min": 0, "max": max + 2, "steps": 5 }
        chart.tooltip =  { "mouse": 2 } 
        chart.elements = [element]
        
        return chart.create()
            
        
    def __getattr__(self, name):
        if not name.startswith("generate_"):
            raise AttributeError(name)
        field = name[len("generate_"):]
        result = getattr(self, field)()

        total_json_file = os.path.join(Configs().results_dir(), 'group_' + self.project_group.group_id + '_comparation.txt');
        os.write_to_file(total_json_file, result)
        return lambda : {}
