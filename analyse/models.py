from datetime import datetime, timedelta
import os
import re
import csv

from django.db import settings
from xml.sax.handler import ContentHandler
from xml.sax import parse, parseString
from lxml import etree

from util.datetimeutils import *
import analyse.ordered_dic
from analyse.config import Config, Configs
from analyse.saxhandlers import *
from analyse.tar import Tar
from analyse.statistics import *

class Build():
    project_id = ""
    name = ""
    start_time = None;
    build_time = 0
    is_passed = False
    last_pass = None
    last_build = None

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

    def __unicode__(self):
        return self.name + " << " + str(self.is_passed) + " << " + str(self.start_time) + "\n"


class Builds:
    def __init__(self):
        self.builds = []

    def total_count(self):
        return len(self.builds)
        
    def project_id(self):
        return self.builds[0].project_id

    def last(self):
        size = len(self.builds)
        if size == 0 :
            return None
        else :
            return self.builds[size - 1]

    def started_at(self):
        return self.builds[0].start_time

    def ended_at(self):
        return self.builds[len(self.builds) - 1].start_time

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
    
    @staticmethod
    def create_builds(config, pattern):
        if pattern == None :
            pattern = "log.*.xml"

        builds_obj = Builds()  
        builds = list();

        all_necessary_files = os.filter_by_days(config.logdir(), pattern, config.days())

        for eachfile in all_necessary_files:
            if None != re.match(pattern, eachfile) :
                try :
                    build = Build.from_file(config.logfile(eachfile))
                    build.project_id = config.id
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
        
    
    def gen_all_reports(self):
        stat = NDaysStatistics(self)
        stat.generate_pass_rate()
        stat.generate_successful_rate()
        stat.generate_build_times()
        stat.generate_per_build_time()
        self.create_csv()
        return

    def create_csv(self):
        project_id = self.project_id()
        config = Configs().find(project_id)
        arrays = Builds.select_values_from(config, None)
        folder = config.result_dir()
        writer = csv.writer(open(os.path.join(folder, project_id + '.csv'), 'w'), delimiter=',')
        writer.writerow(config.csv_keys())
        writer.writerows(arrays)

    def __unicode__(self):
        return "<Builds " + str(self.builds) + ">\n"

    def __len__(self):
        return len(self.builds)

    def __iter__(self):
       return self.builds.__iter__()

    def __getitem__(self, index):
        return self.builds.__getitem__(index)


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


    def projects_comparation(self):
        names = []
        values = []
        max = 0
        
        for project in self:
            project_id = project[0]
            builds = project[1]
            names.append(project_id)
            
            pass_count = builds.pass_count()
            total_count = builds.total_count()
            if total_count > max:
                max = total_count
                
            value = [pass_count,  total_count - pass_count]
            
            values.append(value)
        return values, names, max
        
        
    @staticmethod        
    def create():
        pg = ProjectGroup()
        configs = Configs()

        for config in configs:
            try:
                builds = Builds.create_builds(config[1], None)
                pg.append(config[1], builds)
                builds.gen_all_reports()
            except Exception, e:
                pass
        try:
            tar = Tar(configs).create()
        except Exception, e:
            pass
        stat = GlobalStatistics(pg)
        stat.generate_projects_comparation()                    
        return pg

    def __iter__(self):
        items = self.projects.items()
        items.sort()
        return items.__iter__()