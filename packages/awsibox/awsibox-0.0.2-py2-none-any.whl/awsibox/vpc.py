import troposphere.ec2 as ec2

from .common import *
from .shared import (Parameter, do_no_override, get_endvalue, get_expvalue,
    get_subvalue, auto_get_props, get_condition)


class EC2VPCPeeringConnection(ec2.VPCPeeringConnection):
    def setup(self):
        self.Condition = 'VPCPeeringConnection'
        self.PeerVpcId = get_expvalue('VpcId-stg', '')
        self.VpcId = get_expvalue('VpcId-dev', '')
        self.Tags = Tags(Name='Dev-Peer-Staging')


class EC2RouteNatGateway(ec2.Route):
    def setup(self):
        self.DestinationCidrBlock = '0.0.0.0/0'
        self.NatGatewayId = Ref('NatGateway')
        self.RouteTableId = Ref('RouteTablePrivate')


class EC2RouteInternetGateway(ec2.Route):
    def setup(self):
        self.DestinationCidrBlock = '0.0.0.0/0'
        self.GatewayId = Ref('InternetGateway')
        self.RouteTableId = Ref('RouteTablePublic')


class EC2RoutePeeringConnection(ec2.Route):
    def setup(self):
        self.Condition = 'VPCPeeringConnection'
        self.VpcPeeringConnectionId = Ref('VPCPeeringConnectionDevStaging')


class EC2RoutePeeringConnectionDev(EC2RoutePeeringConnection):
    def setup(self):
        super(EC2RoutePeeringConnectionDev, self).setup()
        self.DestinationCidrBlock = get_expvalue('VPCCidr-stg', '')
        self.RouteTableId = get_expvalue('RouteTablePrivate-dev', '')


class EC2RoutePeeringConnectionStg(EC2RoutePeeringConnection):
    def setup(self):
        super(EC2RoutePeeringConnectionStg, self).setup()
        self.DestinationCidrBlock = get_expvalue('VPCCidr-dev', '')
        self.RouteTableId = get_expvalue('RouteTablePrivate-stg', '')


class EC2VPCEndpoint(ec2.VPCEndpoint):
    def setup(self):
        self.RouteTableIds = [ get_expvalue('RouteTablePrivate') ]
        self.VpcId = get_expvalue('VpcId')


class EC2VPCEndpointS3(EC2VPCEndpoint):
    def setup(self):
        super(EC2VPCEndpointS3, self).setup()
        self.ServiceName = Sub('com.amazonaws.${AWS::Region}.s3')

class EC2VPC(ec2.VPC):
    def setup(self):
        self.CidrBlock = Ref('VPCCidrBlock')
        self.EnableDnsSupport = True
        self.EnableDnsHostnames = True


class EC2Subnet(ec2.Subnet):
    def setup(self, zone):
        self.AvailabilityZone = Sub('${AWS::Region}%s' % zone.lower()) 
        self.VpcId = Ref('VPC')


class EC2SubnetPrivate(EC2Subnet):
    def setup(self, zone):
        super(EC2SubnetPrivate, self).setup(zone)
        self.CidrBlock = Ref('SubnetCidrBlockPrivate%s' % zone)
        self.MapPublicIpOnLaunch = False
        self.Tags = Tags(Name=Sub('${VPCName}-Private%s' % zone))


class EC2SubnetPublic(EC2Subnet):
    def setup(self, zone):
        super(EC2SubnetPublic, self).setup(zone)
        self.CidrBlock = Ref('SubnetCidrBlockPublic%s' % zone)
        self.MapPublicIpOnLaunch = True
        self.Tags = Tags(Name=Sub('${VPCName}-Public%s' % zone))


class EC2RouteTable(ec2.RouteTable):
    def setup(self):
        self.VpcId = Ref('VPC')




class EC2SubnetRouteTableAssociationPrivate(ec2.SubnetRouteTableAssociation):
    def setup(self, zone):
        self.RouteTableId = Ref('RouteTablePrivate')
        self.SubnetId = Ref('SubnetPrivate%s' % zone)


class EC2SubnetRouteTableAssociationPublic(ec2.SubnetRouteTableAssociation):
    def setup(self, zone):
        self.RouteTableId = Ref('RouteTablePublic')
        self.SubnetId = Ref('SubnetPublic%s' % zone)
##

class VPC_Endpoint(object):
    def __init__(self, key):
        # Conditions
        do_no_override(True)
        C_S3 = {'EC2VPCEndpointS3': Not(
            Equals(get_endvalue('VPCEndpoint'), 'None')
        )}

        cfg.Conditions.extend([
            C_S3,
        ])
        do_no_override(False)

        # Resources
        R_S3 = EC2VPCEndpointS3('EC2VPCEndpointS3')
        R_S3.setup()
        R_S3.Condition = 'EC2VPCEndpointS3'

        cfg.Resources.extend([
            R_S3,
        ])


class VPC_VPC(object):
    def __init__(self, key):
        vpc_net = '10.80'
        o_subnetprivate = []
        o_subnetpublic = []

        # Parameters
        P_CidrBlock = Parameter('VPCCidrBlock')
        P_CidrBlock.Description = 'CIDR Block for VPC'
        P_CidrBlock.Default = '%s.0.0/16' % vpc_net

        P_Name = Parameter('VPCName')
        P_Name.Description = 'VPC Tag Name'

        cfg.Parameters.extend([
            P_CidrBlock,
            P_Name,
        ])

        # Resources
        R_VPC = ec2.VPC('VPC')
        auto_get_props(R_VPC, mapname='')

        R_RouteTablePrivate = EC2RouteTable('RouteTablePrivate')
        R_RouteTablePrivate.setup()
        R_RouteTablePrivate.Tags = Tags(Name=Sub('${VPCName}-Private'))

        R_RouteTablePublic = EC2RouteTable('RouteTablePublic')
        R_RouteTablePublic.setup()
        R_RouteTablePublic.Tags = Tags(Name=Sub('${VPCName}-Public'))

        R_InternetGateway = ec2.InternetGateway('InternetGateway')
        R_InternetGateway.Tags = Tags(Name=Ref('VPCName'))

        R_VPCGatewayAttachment = ec2.VPCGatewayAttachment('VPCGatewayAttachment')
        R_VPCGatewayAttachment.InternetGatewayId = Ref('InternetGateway')
        R_VPCGatewayAttachment.VpcId = Ref('VPC')

        R_EIPNat = ec2.EIP('EIPNat')
        R_EIPNat.Domain = 'vpc'

        R_NatGateway = ec2.NatGateway('NatGateway')
        R_NatGateway.AllocationId = GetAtt('EIPNat', 'AllocationId')
        R_NatGateway.SubnetId = Ref('SubnetPublicA')

        R_RouteNatGateway = EC2RouteNatGateway('RouteNatGateway')
        R_RouteNatGateway.setup()

        R_RouteInternetGateway = EC2RouteInternetGateway('RouteInternetGateway')
        R_RouteInternetGateway.setup()

        cfg.Resources.extend([
            R_VPC,
            R_RouteTablePrivate,
            R_RouteTablePublic,
            R_InternetGateway,
            R_VPCGatewayAttachment,
            R_EIPNat,
            R_NatGateway,
            R_RouteNatGateway,
            R_RouteInternetGateway,
        ])

        for i in range(cfg.AZones['MAX']):
            zone_name = cfg.AZoneNames[i]
            zone_cond = 'Zone%s' % zone_name

            # parameters
            p_SubnetCidrBlockPrivate = Parameter('SubnetCidrBlockPrivate%s' % zone_name )
            p_SubnetCidrBlockPrivate.Description = 'Ip Class Range for Private Subnet in Zone %s' % zone_name
            p_SubnetCidrBlockPrivate.Default = '%s.%s.0/20' %(vpc_net, i * 16)

            p_SubnetCidrBlockPublic = Parameter('SubnetCidrBlockPublic%s' % zone_name )
            p_SubnetCidrBlockPublic.Description = 'Ip Class Range for Public Subnet in zone %s' % zone_name
            p_SubnetCidrBlockPublic.Default = '%s.%s.0/24' %(vpc_net, i + 1)

            cfg.Parameters.extend([
                p_SubnetCidrBlockPrivate,
                p_SubnetCidrBlockPublic,
            ])

            # conditions
            do_no_override(True)
            c_Zone = {zone_cond: Equals(
                FindInMap('AvabilityZones', Ref('AWS::Region'), 'Zone%s' % i), 'True'
            )}
            cfg.Conditions.append(c_Zone)
            do_no_override(False)

            # resources

            r_SubnetPrivate = EC2SubnetPrivate('SubnetPrivate%s' % zone_name)
            r_SubnetPrivate.setup(zone_name)
            r_SubnetPrivate.Condition = zone_cond

            r_SubnetPublic = EC2SubnetPublic('SubnetPublic%s' % zone_name)
            r_SubnetPublic.setup(zone_name)
            r_SubnetPublic.Condition = zone_cond

            r_SubnetRouteTableAssociationPrivate = EC2SubnetRouteTableAssociationPrivate('SubnetRouteTableAssociationPrivate%s' % zone_name)
            r_SubnetRouteTableAssociationPrivate.setup(zone_name)
            r_SubnetRouteTableAssociationPrivate.Condition = zone_cond

            r_SubnetRouteTableAssociationPublic = EC2SubnetRouteTableAssociationPublic('SubnetRouteTableAssociationPublic%s' % zone_name)
            r_SubnetRouteTableAssociationPublic.setup(zone_name)
            r_SubnetRouteTableAssociationPublic.Condition = zone_cond

            cfg.Resources.extend([
                r_SubnetPrivate,
                r_SubnetPublic,
                r_SubnetRouteTableAssociationPrivate,
                r_SubnetRouteTableAssociationPublic,
            ])

            # outputs
            o_subnetprivate.append(If(
                zone_cond,
                Ref('SubnetPrivate%s' % zone_name),
                Ref('AWS::NoValue')
            ))

            o_subnetpublic.append(If(
                zone_cond,
                Ref('SubnetPublic%s' % zone_name),
                Ref('AWS::NoValue')
            ))


        # Outputs
        O_VpcId = Output('VpcId')
        O_VpcId.Value = Ref('VPC')
        O_VpcId.Export = Export('VpcId')

        O_VPCCidr = Output('VPCCidr')
        O_VPCCidr.Value = GetAtt('VPC', 'CidrBlock')
        O_VPCCidr.Export = Export('VPCCidr')

        O_RouteTablePrivate = Output('RouteTablePrivate')
        O_RouteTablePrivate.Value = Ref('RouteTablePrivate')
        O_RouteTablePrivate.Export = Export('RouteTablePrivate')

        O_EIPNat = Output('EIPNat')
        O_EIPNat.Value = Ref('O_EIPNat')

        O_SubnetsPrivate = Output('SubnetsPrivate')
        O_SubnetsPrivate.Value = Join(',', o_subnetprivate)
        O_SubnetsPrivate.Export = Export('SubnetsPrivate')

        O_SubnetsPublic = Output('SubnetsPublic')
        O_SubnetsPublic.Value = Join(',', o_subnetpublic)
        O_SubnetsPublic.Export = Export('SubnetsPublic')

        cfg.Outputs.extend([
            O_VpcId,
            O_VPCCidr,
            O_RouteTablePrivate,
            O_EIPNat,
            O_SubnetsPrivate,
            O_SubnetsPublic,
        ])
