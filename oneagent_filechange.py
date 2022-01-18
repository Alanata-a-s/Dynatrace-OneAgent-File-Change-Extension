from ruxit.api.base_plugin import BasePlugin
from ruxit.api.selectors import HostSelector
import logging
import glob
import os.path
import time
import datetime

logger = logging.getLogger(__name__)

class FileChangePlugin(BasePlugin):
    def initialize(self, **kwargs):
        config = kwargs['config']
        logger.info("Config: %s", config)

    def query(self, **kwargs): 
        # File Change 
        host_id =  self.query_snapshot.host_id
        dirModificationMinutes = int(self.config["dir_chg_modification_minutes"])
        dir_event_title = self.config["dir_chg_event_title"]
        dir_event_description = self.config["dir_chg_event_description"]
        dir_event_severity = self.config["dir_chg_event_severity"]

        for dirPattern in self.config["dir_chg_patterns"].split(";"):
            fileChanges = 0 
            # Checking pattern
            logger.debug(f"Change check for pattern {dirPattern}")
            for fileName in glob.glob(dirPattern):
                fileLastModifiedEpoch = os.path.getmtime(fileName)
                logger.debug(f"Change check - validating file {fileName},last modified {fileLastModifiedEpoch}")
                if (time.time() - fileLastModifiedEpoch > dirModificationMinutes*60):
                    logger.debug(f"File {fileName} of not changed within {dirModificationMinutes} seconds")
                    eventTitle = dir_event_title.format(fileName=fileName, fileLastModifiedEpoch=fileLastModifiedEpoch, dirModificationMinutes=dirModificationMinutes, dirPattern=dirPattern)
                    eventDescription = dir_event_description.format(fileName=fileName, fileLastModifiedEpoch=fileLastModifiedEpoch, dirModificationMinutes=dirModificationMinutes, dirPattern=dirPattern)
                    eventProperties = {
                        "File pattern": dirPattern,
                        "File name": fileName,
                        "Last modified": datetime.datetime.utcfromtimestamp(fileLastModifiedEpoch).isoformat()
                    }
                    if dir_event_severity=="Availability":
                        self.results_builder.report_availability_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                    elif dir_event_severity=="Error":
                        self.results_builder.report_error_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                    elif dir_event_severity=="Slowdown":
                        self.results_builder.report_performance_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                    elif dir_event_severity=="Resource":
                        self.results_builder.report_resource_contention_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                    elif dir_event_severity=="Custom":
                        self.results_builder.report_custom_info_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                    else:
                        logger.error(f"Unknown severity {dir_event_severity}")
                else:
                    fileChanges = fileChanges + 1
        self.results_builder.absolute(key="file_changes_detected", value=fileChanges)

        filePatternCountLimit = self.config["dir_count_limit"]
        dir_count_event_title = self.config["dir_count_event_title"]
        dir_count_event_description = self.config["dir_count_event_description"]
        dir_count_event_severity = self.config["dir_count_event_severity"]


        for dirPattern in self.config["dir_count_patterns"].split(";"):
            # Checking pattern
            logger.debug(f"Size check for pattern {dirPattern}")
            filePatternSize = len(glob.glob(dirPattern))
            if filePatternSize > filePatternCountLimit:
                logger.debug(f"Number of files matching {dirPattern} - {filePatternSize} above limit of {filePatternCountLimit}")                
                eventTitle = dir_count_event_title.format(dirPattern=dirPattern, filePatternSize=filePatternSize, filePatternSizeLimit=filePatternCountLimit)
                eventDescription = dir_count_event_description.format(dirPattern=dirPattern, filePatternSize=filePatternSize, filePatternSizeLimit=filePatternCountLimit)
                eventProperties = {
                    "File pattern": dirPattern,
                    "Number of files": str(filePatternSize),
                    "Limit": str(filePatternCountLimit)
                }
                if dir_count_event_severity=="Availability":
                    self.results_builder.report_availability_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                elif dir_count_event_severity=="Error":
                    self.results_builder.report_error_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                elif dir_count_event_severity=="Slowdown":
                    self.results_builder.report_performance_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                elif dir_count_event_severity=="Resource":
                    self.results_builder.report_resource_contention_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                elif dir_count_event_severity=="Custom":
                    self.results_builder.report_custom_info_event(description=eventDescription, title=eventTitle, properties=eventProperties, entity_selector=HostSelector())
                else:
                    logger.error(f"Unknown severity {dir_count_event_severity}")


