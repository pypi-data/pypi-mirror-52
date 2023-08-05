import troposphere.logs as lgs

from .common import *
from .shared import (Parameter, do_no_override, get_endvalue, get_expvalue,
    get_subvalue, auto_get_props, get_condition)


class LogsLogGroup(lgs.LogGroup):
    def __init__(self, title, **kwargs):
        super(LogsLogGroup, self).__init__(title, **kwargs)
        self.LogGroupName = get_endvalue('LogGroupName')
        self.RetentionInDays = get_endvalue('LogRetentionInDays')


# #################################
# ### START STACK INFRA CLASSES ###
# #################################

class LGS_LogGroup(object):
    def __init__(self, key):
        R_Group = LogsLogGroup('LogsLogGroup')

        cfg.Resources.extend([
            R_Group,
        ])
