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


class HudsonBuilds:

 	@staticmethod
    def create_hudson_builds(config, pattern):
        builds_obj = Builds()
        builds = list();

        all_necessary_files = HudsonBuilds.filter_by_days(config.logdir(), config.days())
        for eachfile in all_necessary_files:
            if None != re.match(pattern, eachfile) :
                try :
                    build = Build.from_file(config.logfile(eachfile))
					build.
                    build.project_id = config.id
                    builds.append(build)
                except Exception, e :
                    logging.getLogger('ianalyse_logger').error(e)
                    pass

        builds_obj.builds = builds
        return builds_obj;

 	@staticmethod
    def filter_by_days(dir, days):
		files = list();
		