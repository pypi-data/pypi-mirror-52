import troposphere.efs as efs

from .common import *
from .shared import (Parameter, do_no_override, get_endvalue, get_expvalue,
    get_subvalue, auto_get_props, get_condition)
from .route53 import R53RecordSetEFS
from .securitygroup import SecurityGroup, SecurityGroupIngress


class EFSFileSystem(efs.FileSystem):
    def setup(self):
        self.Condition = self.title
        self.Encrypted = False
        self.PerformanceMode = 'generalPurpose'


class EFSMountTarget(efs.MountTarget):
    def setup(self, index, sgname, efsresname):
        name = self.title
        self.Condition = name
        self.FileSystemId = Ref(efsresname)
        self.SecurityGroups = [
            Ref(sgname)
        ]
        self.SubnetId = Select(str(index), Split(',', get_expvalue('SubnetsPrivate')))

# #################################
# ### START STACK INFRA CLASSES ###
# #################################

class EFS_FileStorage(object):
    def __init__(self, key):
        for n, v in getattr(cfg, key).iteritems():
            resname =  key + n  # Ex. EFSFileSystemWordPress
            recordname = 'RecordSetEFS' + n  # Ex. RecordSetEFSWordPress
            sgservername = 'SecurityGroupEFSServer' + n  # Ex. SecurityGroupEFSServerWordPress
            sgclientname = 'SecurityGroupEFS' + n  # Ex. SecurityGroupEFSWordPress
            sginame = 'SecurityGroupIngressEFS' + n  # Ex. SecurityGroupIngressEFSWordPress
            for i in range(cfg.AZones['MAX']):
                mountname = 'EFSMountTarget%s%s' % (n, i)  # Ex. EFSMountTargetWordPress3
                # conditions
                do_no_override(True)
                c_FileZone = {mountname: And(
                    Condition(resname),
                    Equals(FindInMap('AvabilityZones', Ref('AWS::Region'), 'Zone%s' % i), 'True')
                )}
                cfg.Conditions.append(c_FileZone)
                do_no_override(False)

                # resources
                r_Mount = EFSMountTarget(mountname)
                r_Mount.setup(index=i, sgname=sgservername, efsresname=resname)

                cfg.Resources.append(r_Mount)
            # conditions
            do_no_override(True)
            c_File = {resname: Not(
                Equals(get_endvalue(resname + 'Enabled'), 'None')
            )}
            cfg.Conditions.append(c_File)
            do_no_override(False)

            # resources
            r_File = EFSFileSystem(resname)
            r_File.setup()

            r_Record = R53RecordSetEFS(recordname)
            r_Record.setup(n)

            r_SGServer = SecurityGroup(sgservername)
            r_SGServer.setup()
            r_SGServer.Condition = resname
            r_SGServer.GroupDescription = 'Rule to access EFS FileSystem ' + n

            r_SGClient = SecurityGroup(sgclientname)
            r_SGClient.setup()
            r_SGClient.Condition = resname
            r_SGClient.GroupDescription = 'Enable access to EFS FileSystem ' + n

            SGIExtra = {
                'Name': sginame,
                'Condition': resname,
                'FromPort': 2049,
                'GroupId': 'Sub(\'${%s.GroupId}\')' % sgservername,
                'SourceSecurityGroupId': 'Ref(\'%s\')' % sgclientname,
                'ToPort': 2049
            }

            r_SGI = SecurityGroupIngress(sginame)
            auto_get_props(r_SGI, SGIExtra, rootdict=SGIExtra, mapname='', del_prefix=sginame)

            cfg.Resources.extend([
                r_File,
                r_Record,
                r_SGServer,
                r_SGClient,
                r_SGI,
            ])

            # outputs

            o_SG = Output(sgclientname)
            o_SG.Condition = resname
            o_SG.Value = GetAtt(sgclientname, 'GroupId')
            o_SG.Export = Export(sgclientname)

            cfg.Outputs.append(o_SG)
