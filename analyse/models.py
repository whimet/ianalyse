from django.db import connection, models,settings
import string
from datetime import datetime, timedelta
import os
from util.datetimeutils import *
from analyse.openFlashChart import Chart
import re
import analyse.ordered_dic
from analyse.config import Config, Configs

from xml.sax.handler import ContentHandler
from xml.sax import parse, parseString
import sys
from analyse.saxhandlers import *
from lxml import etree
import StringIO
import csv
from analyse.tar import Tar


class Build(models.Model):
    project_id = models.TextField()
    number = models.TextField()
    name = models.TextField()
    scm_type = models.TextField()
    scm_revision = models.TextField()
    start_time = models.DateTimeField('build start')
    build_time = models.IntegerField('How long does this build take', default=0)
    is_passed = models.BooleanField('Does the build pass', default=False)
    last_pass = models.DateTimeField('When is the last successful date happend?')
    last_build = models.DateTimeField('When is the last build happend?')

    def __unicode__(self):
        return self.name + " << " + str(self.is_passed) + " << " + str(self.start_time) + "\n"

    def day_of_start(self):
        return begining_of_the_day(self.start_time)

    @staticmethod
    def from_xml(input):
        build = Build()
        parseString(input, MultipleHandlers(build))
        return build

    @staticmethod
    def from_file(input):
        build = Build()
        parse(input, MultipleHandlers(build))
        return build

    @staticmethod
    def select_values(file, csv_settings):
        tree = etree.parse(file)
        root = tree.getroot()
        result = []
        for setting in csv_settings :
            try:
                select_xpath = etree.XPath(setting[1])
                result.append(select_xpath(root)[0])
            except Exception, e:
                result.append(None)
        return result

    @staticmethod
    def started_build_at(project_id):
        cursor = connection.cursor()
        cursor.execute("select min(start_time) from analyse_build where project_id = %s", [project_id])
        return  cursor.fetchone()[0]

    @staticmethod
    def last_built_at(project_id):
        cursor = connection.cursor()
        cursor.execute("select max(start_time) from analyse_build where project_id = %s", [project_id])
        return  cursor.fetchone()[0]

    @staticmethod
    def total(project_id):
        cursor = connection.cursor()
        cursor.execute("select count(1) from analyse_build where project_id = %s", [project_id])
        total = cursor.fetchone()
        return total[0]

    @staticmethod
    def view_all(project_id, results):
        results["started_build_at"] = Build.started_build_at(project_id)
        results["last_built_at"] = Build.last_built_at(project_id)
        return

    def need_attention(self):
        if self.is_last_pass_old():
            return True
        
        if self.is_last_build_old():
            return True
        
        return False
    
    def is_last_pass_old(self):
        now = datetime.now()
        return self.find_last_pass() != None and now - self.find_last_pass() > timedelta(hours=24)
        
    def is_last_build_old(self):
        now = datetime.now()
        return self.start_time != None and now - self.start_time > timedelta(hours=24)

    def last_build_t(self):
        return time_delta_as_str(datetime.now() - self.start_time)

    def last_pass_t(self):
        return time_delta_as_str(datetime.now() - self.find_last_pass())

    def find_last_pass(self):
        if self.is_passed :
            return self.start_time
        else:
            return self.last_pass


class TopNStatistics :
    def __init__(self, project_id=None, builds = list()):
        self.project_id = project_id
        self.builds = builds

    def pass_rate(self):
        builds = Builds()
        builds.builds = self.builds

        total  = builds.total_count()
        passed = builds.pass_count()
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
        chart.title = {"text": str(len(builds)) + ' Runs', "style": "{font-size: 15px; font-family: Times New Roman; font-weight: bold; color: #4183C4; text-align: center;}" }
        chart.bg_colour = "#FFFFFF" 
        return chart.create()

    def per_build_time(self):
        builds = Builds()
        builds.builds = self.builds

        chart = Chart()

        values, labels, max_time = builds.per_build_time();
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

        builds = Builds()
        builds.builds = self.builds
        values, min_date, max_date = builds.pass_rate_by_day()

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

        builds = Builds()
        builds.builds = self.builds
        
        values, min_date, max_date, max_time = builds.build_times()

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

class Builds:
    def __init__(self):
        self.builds = []

    def __len__(self):
        return len(self.builds)

    def __iter__(self):
       return self.builds.__iter__()

    def __getitem__(self, index):
        return self.builds.__getitem__(index)

    def total_count(self):
        return len(self.builds)
        
    def last(self):
        size = len(self.builds)
        if size == 0 :
            return None
        else :
            return self.builds[size - 1]

    def append(self, build):
        self.builds.append(build)
        
    def group_by_each_day(self):
        grouped_builds = analyse.ordered_dic.ordered_dict()

        for build in self.builds :
            day_of_start = build.day_of_start()
            if (day_of_start not in grouped_builds):
                newbuilds = Builds()
                newbuilds.builds.append(build)
                grouped_builds[day_of_start] = newbuilds
            else :
                grouped_builds[day_of_start].builds.append(build)

        return grouped_builds

    def pass_rate_by_day(self) :
        arry = []
        builds = Builds()
        builds.builds = self.builds
        grped_builds = builds.group_by_each_day();
        min_date = None;
        max_date = None;

        for day_of_start in grped_builds.order() :
            timestamp = int(to_unix_timestamp(day_of_start));
            pass_rate = grped_builds[day_of_start].pass_rate()
            arry.append({"x" : timestamp, "y" : pass_rate * 100})
            if min_date == None or timestamp < min_date:
                min_date = timestamp;

            if max_date == None or timestamp >  max_date:
                max_date = timestamp;

        return arry,min_date, max_date

    def build_times(self):
        arry = []
        min_date = None;
        max_date = None;
        max_time = None
        for build in self.builds :
            timestamp = int(to_unix_timestamp(build.start_time));
            arry.append({"x" : timestamp, "y" : build.build_time})
            if min_date == None or timestamp < min_date:
                min_date = timestamp;

            if max_date == None or timestamp >  max_date:
                max_date = timestamp;

            if max_time == None or build.build_time > max_time:
                max_time = build.build_time

        return arry,min_date, max_date, max_time    

    def per_build_time(self):
        arry = []
        labels = []
        max_time = None
        for build in self.builds :
            timestamp = int(to_unix_timestamp(build.start_time));
            color = None;
            if build.is_passed:
                color = '#1C9E05'
            else:
                color = '#FF368D'                           

            arry.append({"top" : build.build_time, "colour": color})
            labels.append(str(build.start_time))
            if max_time == None or build.build_time > max_time:
                max_time = build.build_time
        return arry, labels, max_time

    def pass_count(self) :
        count = 0
        for build in self.builds :
            if build.is_passed :
                count = count + 1
        return count

    def pass_rate(self) :
        if len(self.builds) == 0:
            return 0

        return float('%.2f' % (self.pass_count() / (len(self.builds) - 0.0)))
    
    def avg_build_time(self):
        array = []
        for build in self.builds :
            array.append(build.build_time)
        if len(array) == 0:
            return '0'

        average = float(sum(array)) / len(array)
        return "%.2f" % average
    
    def avg_runs(self):
        min = self.builds[0]
        max = self.builds[len(self.builds) - 1]
        delta = max.start_time - min.start_time
        len_builds = len(self.builds)
        if delta.days <= 1 :
            return '%.2f' % len_builds
        return '%.2f' % (len_builds / (delta.days - 0.0))
    
    def __unicode__(self):
        return "<Builds " + str(self.builds) + ">\n"


    @staticmethod
    def create_builds(config, pattern):
        if pattern == None :
            pattern = "log.*.xml"

        Build.objects.filter(project_id = config.id).delete()
        builds_obj = Builds()  
        builds = list();

        all_necessary_files = os.filter_by_days(config.logdir(), pattern, config.days())

        for eachfile in all_necessary_files:
            if None != re.match(pattern, eachfile) :
                try :
                    build = Build.from_file(config.logfile(eachfile))
                    build.project_id = config.id
                    build.save()
                    builds.append(build)
                except Exception, e :
                    print e
                    pass

        builds_obj.builds = builds
        return builds_obj;

    @staticmethod  
    def select_values_from(config, pattern):
        if pattern == None :
            pattern = "log.*.xml"

        values = []
        all_necessary_files = os.filter_by_days(config.logdir(),"log([0-9]*).*.xml", config.days())
        
        for eachfile in all_necessary_files:
            if None != re.match(pattern, eachfile) :
                try :
                    value = Build.select_values(config.logfile(eachfile), config.csv_settings())
                    values.append(value)
                except Exception, e :
                    pass
        return values
        
    @staticmethod
    def create_csv(project_id):
        config = Configs().find(project_id)
        arrays = Builds.select_values_from(config, None)
        folder = config.result_dir()
        writer = csv.writer(open(os.path.join(folder, project_id + '.csv'), 'w'), delimiter=',')
        writer.writerow(config.csv_keys())
        writer.writerows(arrays)
    
    @staticmethod
    def gen_all_reports(project_id):
        stat = TopNStatistics(project_id = project_id, builds = Build.objects.filter(project_id = project_id).order_by('start_time'))
        stat.generate_pass_rate()
        stat.generate_successful_rate()
        stat.generate_build_times()
        stat.generate_per_build_time()
        Builds.create_csv(project_id)
        return

class ProjectGroup:
    def __init__(self):
        self.projects = {}
    
    def append(self, config, builds):
        if isinstance(config, Config):
            self.projects[config.id] = builds
        else:
            self.projects[config] = builds
        
    def find(self, id):
        builds = self.projects.get(id)
        if builds == None:
            return Builds()
        else:
            return builds
    
    def latest_build_of(self, id):
        builds = self.find(id)
        return builds.last()

    @staticmethod        
    def create():
        pg = ProjectGroup()
        configs = Configs()

        for config in configs:
            try:
                pg.append(config[1], Builds.create_builds(config[1], None))
                Builds.gen_all_reports(config[1].id)
            except Exception, e:
                pass
        try:
            tar = Tar(configs).create()
        except Exception, e:
            print e
            pass
                    
        return pg
    
    
    
    

    
    
    
    
    
    
    
    

