# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class EventHubNamespace(pulumi.CustomResource):
    auto_inflate_enabled: pulumi.Output[bool]
    """
    Is Auto Inflate enabled for the EventHub Namespace?
    """
    capacity: pulumi.Output[float]
    """
    Specifies the Capacity / Throughput Units for a `Standard` SKU namespace. Valid values range from 1 - 20.
    """
    default_primary_connection_string: pulumi.Output[str]
    """
    The primary connection string for the authorization
    rule `RootManageSharedAccessKey`.
    """
    default_primary_key: pulumi.Output[str]
    """
    The primary access key for the authorization rule `RootManageSharedAccessKey`.
    """
    default_secondary_connection_string: pulumi.Output[str]
    """
    The secondary connection string for the
    authorization rule `RootManageSharedAccessKey`.
    """
    default_secondary_key: pulumi.Output[str]
    """
    The secondary access key for the authorization rule `RootManageSharedAccessKey`.
    """
    kafka_enabled: pulumi.Output[bool]
    """
    Is Kafka enabled for the EventHub Namespace? Defaults to `false`.
    """
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
    """
    maximum_throughput_units: pulumi.Output[float]
    """
    Specifies the maximum number of throughput units when Auto Inflate is Enabled. Valid values range from 1 - 20.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the EventHub Namespace resource. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the namespace. Changing this forces a new resource to be created.
    """
    sku: pulumi.Output[str]
    """
    Defines which tier to use. Valid options are `Basic` and `Standard`.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, auto_inflate_enabled=None, capacity=None, kafka_enabled=None, location=None, maximum_throughput_units=None, name=None, resource_group_name=None, sku=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manage an EventHub Namespace.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_inflate_enabled: Is Auto Inflate enabled for the EventHub Namespace?
        :param pulumi.Input[float] capacity: Specifies the Capacity / Throughput Units for a `Standard` SKU namespace. Valid values range from 1 - 20.
        :param pulumi.Input[bool] kafka_enabled: Is Kafka enabled for the EventHub Namespace? Defaults to `false`.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[float] maximum_throughput_units: Specifies the maximum number of throughput units when Auto Inflate is Enabled. Valid values range from 1 - 20.
        :param pulumi.Input[str] name: Specifies the name of the EventHub Namespace resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku: Defines which tier to use. Valid options are `Basic` and `Standard`.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/eventhub_namespace.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['auto_inflate_enabled'] = auto_inflate_enabled
            __props__['capacity'] = capacity
            __props__['kafka_enabled'] = kafka_enabled
            __props__['location'] = location
            __props__['maximum_throughput_units'] = maximum_throughput_units
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if sku is None:
                raise TypeError("Missing required property 'sku'")
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['default_primary_connection_string'] = None
            __props__['default_primary_key'] = None
            __props__['default_secondary_connection_string'] = None
            __props__['default_secondary_key'] = None
        super(EventHubNamespace, __self__).__init__(
            'azure:eventhub/eventHubNamespace:EventHubNamespace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, auto_inflate_enabled=None, capacity=None, default_primary_connection_string=None, default_primary_key=None, default_secondary_connection_string=None, default_secondary_key=None, kafka_enabled=None, location=None, maximum_throughput_units=None, name=None, resource_group_name=None, sku=None, tags=None):
        """
        Get an existing EventHubNamespace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_inflate_enabled: Is Auto Inflate enabled for the EventHub Namespace?
        :param pulumi.Input[float] capacity: Specifies the Capacity / Throughput Units for a `Standard` SKU namespace. Valid values range from 1 - 20.
        :param pulumi.Input[str] default_primary_connection_string: The primary connection string for the authorization
               rule `RootManageSharedAccessKey`.
        :param pulumi.Input[str] default_primary_key: The primary access key for the authorization rule `RootManageSharedAccessKey`.
        :param pulumi.Input[str] default_secondary_connection_string: The secondary connection string for the
               authorization rule `RootManageSharedAccessKey`.
        :param pulumi.Input[str] default_secondary_key: The secondary access key for the authorization rule `RootManageSharedAccessKey`.
        :param pulumi.Input[bool] kafka_enabled: Is Kafka enabled for the EventHub Namespace? Defaults to `false`.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[float] maximum_throughput_units: Specifies the maximum number of throughput units when Auto Inflate is Enabled. Valid values range from 1 - 20.
        :param pulumi.Input[str] name: Specifies the name of the EventHub Namespace resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku: Defines which tier to use. Valid options are `Basic` and `Standard`.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/eventhub_namespace.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["auto_inflate_enabled"] = auto_inflate_enabled
        __props__["capacity"] = capacity
        __props__["default_primary_connection_string"] = default_primary_connection_string
        __props__["default_primary_key"] = default_primary_key
        __props__["default_secondary_connection_string"] = default_secondary_connection_string
        __props__["default_secondary_key"] = default_secondary_key
        __props__["kafka_enabled"] = kafka_enabled
        __props__["location"] = location
        __props__["maximum_throughput_units"] = maximum_throughput_units
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["sku"] = sku
        __props__["tags"] = tags
        return EventHubNamespace(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

