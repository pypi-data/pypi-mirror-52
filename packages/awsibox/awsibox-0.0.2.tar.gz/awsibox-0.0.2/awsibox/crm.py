import troposphere.certificatemanager as crm

from .common import *
from .shared import (Parameter, do_no_override, get_endvalue, get_expvalue,
    get_subvalue, auto_get_props, get_condition)


class CRMCertificate(crm.Certificate):
    def setup(self, key):
        auto_get_props(self, key, recurse=True)


# #################################
# ### START STACK INFRA CLASSES ###
# #################################

class CRM_Certificate(object):
    def __init__(self, key):
        for n, v in getattr(cfg, key).iteritems():
            if 'Enabled' in v and not v['Enabled']:
                continue
            # resources
            resname = key + n
            r_Certificate = CRMCertificate(resname)
            r_Certificate.setup(key=v)
            r_Certificate.Tags = Tags(Name=n)

            cfg.Resources.extend([
                r_Certificate,
            ])

            # outputs
            o_Certificate = Output(resname)
            o_Certificate.Value = Ref(resname)

            if hasattr(r_Certificate, 'Condition'):
                o_Certificate.Condition = r_Certificate.Condition

            cfg.Outputs.extend([
                o_Certificate,
            ])


class CRM_CertificateEC2(object):
    def __init__(self, key):
        if cfg.ListenerLoadBalancerHttpsPort != 'None':
            CRM_Certificate(key)


class CRM_CertificateECS(object):
    def __init__(self, key):
        if cfg.ListenerLoadBalancerHttpsPort != 443:
            CRM_Certificate(key)


class CRM_CertificateRES(object):
    def __init__(self, key):
        CRM_Certificate(key)
