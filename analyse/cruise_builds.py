import json as JSON
import urllib
import analyse.models
from datetime import datetime
import logging
import analyse.models
import analyse.models
import os

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
        self.stageName = ss[1]
        if len(ss) == 3:
            self.jobName = ss[2]
        else:
            self.jobName = None
        self.buildsCnt = 30

    def stageHistoryJson(self):
        url = '%s/stageHistory.json?pipelineName=%s&stageName=%s&perPage=%d' % (self.baseurl, self.pipelineName, self.stageName, self.buildsCnt)
        json = UrlUtils.get(url)
        return JSON.loads(self.fix_json(json))

    def fix_json(self, json):
        return json.replace(r"\'", "").replace("&amp;", "&")

    def createBuilds(self):
        if not self.jobName == None:
            return self.createBuildsForJob()
        else:
            return self.createBuildsForStage()

    def createBuildsForJob(self):
        stageHistory = self.stageHistoryJson()

        result = analyse.models.Builds()
        stageList = stageHistory['history']
        stageList.reverse()
        for stage in stageList:

            for job in stage['builds']:
                buildCause = stage['buildCause']

                if job['name'] == self.jobName and ( job['result'] == 'Passed' or job['result'] == 'Failed' ):
                    build = analyse.models.Build()
                    build.project_id = '%s__%s__%s' % (self.pipelineName, self.stageName, self.jobName)
                    build.name = job['name']
                    dateTimeStr = job['build_building_date']
                    build.start_time = datetime.strptime(dateTimeStr[0:-6], "%Y-%m-%dT%H:%M:%S") #remove timezone
                    build.build_time = int(job['current_build_duration'])
                    build.is_passed = job['result'] == 'Passed'

                    index = buildCause.find('by ')
                    if index > -1:
                        commitor = buildCause[index + 3:]
                        build.add_commitor(commitor, None)

                    result.append(build)
        return result

    def createBuildsForStage(self):
        return analyse.models.Builds()
