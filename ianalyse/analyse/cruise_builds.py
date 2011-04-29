import json as JSON
import urllib
import analyse.models
from datetime import datetime
import logging
import analyse.models
import analyse.models
import os
import analyse.models
from util.datetimeutils import *

class UrlUtils:
    @staticmethod
    def get(url):
        f = urllib.urlopen(url)
        content = f.read();
        f.close();
        return content

class CruiseBuilds:
    def __init__(self, config):
        self.baseurl = config.baseurl()
        ss = config.id.split('__')
        self.pipelineName = ss[0]
        if len(ss) > 1:
            self.stageName = ss[1]
        else:
            self.stageName = None
        if len(ss) > 2:
            self.jobName = ss[2]
        else:
            self.jobName = None
        self.buildsCnt = 20

    def stageHistory(self):
        url = '%s/stageHistory.json?pipelineName=%s&stageName=%s&perPage=%d' \
                    % (self.baseurl, self.pipelineName, self.stageName, self.buildsCnt)
        logging.getLogger('ianalyse_logger').info('requesting ' + url)
        json = UrlUtils.get(url)
        jsonObj = JSON.loads(self.fix_json(json))
        stageList = jsonObj['history']
        stageList.reverse()
        return stageList

    def pipelineHistory(self):
        url = '%s/pipelineHistory.json?pipelineName=%s&perPage=%s' \
                        % (self.baseurl, self.pipelineName, self.buildsCnt)
        logging.getLogger('ianalyse_logger').info('requesting ' + url)
        json = UrlUtils.get(url)
        jsonObj = JSON.loads(self.fix_json(json))
        historyList = []
        for group in jsonObj['groups']:
            historyList.extend(group['history'])
        historyList.reverse()
        return historyList

    @staticmethod
    def stageStatusJson(baseurl, pipelineName, pipelineCounter, stageName, stageCounter):
        url = '%s/stageStatus.json?pipelineName=%s&label=%s&stageName=%s&counter=%s' \
                % (baseurl, pipelineName, pipelineCounter, stageName, stageCounter)
        logging.getLogger('ianalyse_logger').info('requesting ' + url)
        json = UrlUtils.get(url)
        return JSON.loads(CruiseBuilds.fix_json(json))

    @staticmethod
    def fix_json(json):
        return json.replace(r"\'", "").replace("&amp;", "&")

    @staticmethod
    def getCruiseTime(dateTimeStr):
        return datetime.strptime(dateTimeStr[0:-6], "%Y-%m-%dT%H:%M:%S") #remove timezone

    @staticmethod
    def getCommit(json, buildCauseKey = 'buildCause'):
        revision = json['materialRevisions'][0]['revision']
        buildCause = json[buildCauseKey]
        index = buildCause.find('by ')
        if index > -1:
            commitor = buildCause[index + 3:]
            return analyse.models.Commit(commitor, revision)

    def createBuilds(self):
        if not self.jobName == None:
            return self.createBuildsForJob()
        elif not self.stageName == None:
            return self.createBuildsForStage()
        else:
            return self.createBuildsForPipeline()

    def createBuildsForJob(self):
        result = analyse.models.Builds()
        for stage in self.stageHistory():
            for job in stage['builds']:
                if job['name'] == self.jobName and ( job['result'] == 'Passed' or job['result'] == 'Failed' ):
                    build = analyse.models.Build()
                    build.project_id = '%s__%s__%s' % (self.pipelineName, self.stageName, self.jobName)
                    build.name = job['name']
                    build.start_time = self.getCruiseTime(job['build_building_date'])
                    build.build_time = int(job['current_build_duration'])
                    build.is_passed = job['result'] == 'Passed'
                    build.commits.add(CruiseBuilds.getCommit(stage))
                    result.append(build)
        return result

    def createBuildsForStage(self):
        result = analyse.models.Builds()
        for stageJson in self.stageHistory():
            build = analyse.models.Build()
            stage = Stage(stageJson)
            if not stage.isBuilding():
                build.project_id = '%s__%s' % (self.pipelineName, self.stageName)
                build.name = stage.name()
                build.start_time = stage.startTime()
                build.build_time = stage.buildTime()
                build.is_passed = stage.isPassed()
                build.commits.add(stage.commit())
                
                if not build.start_time == None:
                    result.append(build)
        return result

    def createBuildsForPipeline(self):
        result = analyse.models.Builds()
        list = self.pipelineHistory()
        for pipelineJson in list:
            build = analyse.models.Build()
            pipeline = Pipeline(self.pipelineName, pipelineJson, self.baseurl)
            build.project_id = self.pipelineName
            build.name = self.pipelineName
            build.start_time = pipeline.startTime()
            build.build_time = pipeline.buildTime()
            build.is_passed = pipeline.isPassed()
            build.commits.add(pipeline.commit())

            if not build.start_time == None:
                result.append(build)
        return result

class Stage:
    def __init__(self, stageJsonObj):
        self.json = stageJsonObj

    def name(self):
        return self.json['stageName']

    def startTime(self):
        minTime = None
        for job in self.json['builds']:
            timeStr = job['build_building_date']
            if len(timeStr) > 0 and not timeStr == 'N/A' :
                time = CruiseBuilds.getCruiseTime(timeStr)
                if minTime == None or minTime > time:
                    minTime = time
        return minTime

    def endTime(self):
        maxTime = None
        for job in self.json['builds']:
            timeStr = job['build_completed_date']
            if len(timeStr) > 0 and not timeStr == 'N/A':
                time = CruiseBuilds.getCruiseTime(timeStr)
                if maxTime == None or maxTime < time:
                    maxTime = time
        return maxTime

    def buildTime(self):
        endTime = self.endTime()
        startTime = self.startTime()
        if not endTime == None and not startTime == None:
            return to_unix_timestamp(endTime) - to_unix_timestamp(self.startTime())
        return 0

    def isBuilding(self):
        return self.json['current_status'] == 'building'

    def isPassed(self):
        for job in self.json['builds']:
            if job['result'] == 'Failed':
                return False
        return True

    def commit(self):
        return CruiseBuilds.getCommit(self.json)

class Pipeline:
    def __init__(self, name, json, baseurl):
        self.name = name
        self.json = json
        self.baseurl = baseurl
        self.cache = {}

    def stage(self, stageName, stageCounter):
        stage_id = stageName + '-' + stageCounter
        if not self.cache.has_key(stage_id):
            json = CruiseBuilds.stageStatusJson(self.baseurl, self.name, self.json['counterOrLabel'], stageName, stageCounter)
            self.cache[id] = Stage(json['stage'])
        return self.cache[id]

    def startTime(self):
        minTime = None
        for stage in self.json['stages']:
            stage = self.stage(stage['stageName'], stage['stageCounter'])
            stageStartTime = stage.startTime()
            if minTime == None or minTime > stageStartTime:
                minTime = stageStartTime
        return minTime

    def buildTime(self):
        time = 0
        for stage in self.json['stages']:
            stage = self.stage(stage['stageName'], stage['stageCounter'])
            time = time + stage.buildTime()
        return time

    def isPassed(self):
        for stage in self.json['stages']:
            stage = self.stage(stage['stageName'], stage['stageCounter'])
            if not stage.isPassed():
                return False
        return True

    def commit(self):
        return CruiseBuilds.getCommit(self.json, 'buildCauseBy')


