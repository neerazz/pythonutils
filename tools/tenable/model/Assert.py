from typing import List

from util import datetime_util as du


class CIDR:
    cidr: str
    ipaddress: str
    range: int

    def __init__(self, cidr):
        self.cidr = cidr
        split = cidr.split("/")
        if len(split) == 2:
            self.ipaddress = split[0]
            self.range = int(split[1])
        else:
            print(f"Invalid CIDR: {cidr}. Setting values to default.")


class TenableSource:
    name: str
    first_seen: str
    last_seen: str

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)


class TenableTag:
    tag_uuid: str
    tag_key: str
    tag_value: str
    added_by: str
    added_at: str

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)


class TenableInterface:
    name: str
    aliased: int
    fqdn: list
    mac_address: list
    ipv4: list
    ipv6: list

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)


class TenableSecurityProtection:
    id: str
    cpe: str
    version: str
    vendor_name: str
    product_name: str
    form_factor: str
    disposition: str
    updated_at: int

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)


class TenableAssert:
    id: str
    has_agent: int
    created_at: str
    updated_at: str
    first_seen: str
    last_seen = ""
    last_scan_target: str
    last_authenticated_scan_date: str
    last_licensed_scan_date: str
    last_scan_id: str
    last_schedule_id: str
    sources: List[TenableSource]
    tags: List[TenableTag]
    interfaces: List[TenableInterface]
    network_id: List
    ipv4: List
    ipv6: list
    fqdn: List
    mac_address: List
    netbios_name: List
    operating_system: List
    system_type: List
    tenable_uuid: List
    hostname: List
    agent_name: List
    bios_uuid: List
    aws_ec2_instance_id: list
    aws_ec2_instance_ami_id: list
    aws_owner_id: list
    aws_availability_zone: list
    aws_region: list
    aws_vpc_id: list
    aws_ec2_instance_group_name: list
    aws_ec2_instance_state_name: list
    aws_ec2_instance_type: list
    aws_subnet_id: list
    aws_ec2_product_code: list
    aws_ec2_name: list
    azure_vm_id: list
    azure_resource_id: list
    azure_subscription_id: list
    azure_resource_group: list
    azure_location: list
    azure_type: list
    gcp_project_id: list
    gcp_zone: list
    gcp_instance_id: list
    ssh_fingerprint: list
    mcafee_epo_guid: list
    mcafee_epo_agent_guid: list
    qualys_asset_id: list
    qualys_host_id: list
    servicenow_sysid: list
    installed_software: List[str]
    bigfix_asset_id: list
    security_protection_level: int
    security_protections: List[TenableSecurityProtection]
    exposure_confidence_value: str

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)
        self.last_seen = du.get_date(self.last_seen, du.CCYY_MM_DD_HH_MM_SS)
        # self.process_specials()

    def process_specials(self):
        if self.sources is not None:
            self.process_sources(self.sources)

        if self.tags is not None:
            self.process_tags(self.tags)

        if self.interfaces is not None:
            self.process_interfaces(self.interfaces)

        if self.security_protections is not None:
            self.process_security_protections(self.security_protections)

    def process_sources(self, sources):
        self.sources = []
        for source in sources:
            self.sources.append(TenableSource(source))

    def process_tags(self, tags):
        self.tags = []
        for tag in tags:
            self.tags.append(TenableTag(tag))

    def process_interfaces(self, interfaces):
        self.interfaces = []
        for interface in interfaces:
            self.interfaces.append(TenableInterface(interface))

    def process_security_protections(self, security_protections):
        self.security_protections = []
        for protection in security_protections:
            self.security_protections.append(TenableSecurityProtection(protection))

    def __repr__(self):
        return f"Assert name : {self.hostname}, with IP : {self.ipv4}"


class TenableAsserts:
    total: int
    assets = []

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)
        assets = []
        for each_assert in self.assets:
            assets.append(TenableAssert(each_assert))
        self.assets = assets

    def __repr__(self):
        asserts = "\n".join([str(a) for a in self.assets])
        return f"Asserts : {asserts}\nLength:{len(self.assets)}\nTotal:{self.total}"
