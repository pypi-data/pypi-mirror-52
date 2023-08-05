# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class NetworkConnectionMonitor(pulumi.CustomResource):
    auto_start: pulumi.Output[bool]
    """
    Specifies whether the connection monitor will start automatically once created. Defaults to `true`. Changing this forces a new resource to be created.
    """
    destination: pulumi.Output[dict]
    """
    A `destination` block as defined below.
    
      * `address` (`str`)
      * `port` (`float`)
      * `virtual_machine_id` (`str`)
    """
    interval_in_seconds: pulumi.Output[float]
    """
    Monitoring interval in seconds. Defaults to `60`.
    """
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    The name of the Network Connection Monitor. Changing this forces a new resource to be created.
    """
    network_watcher_name: pulumi.Output[str]
    """
    The name of the Network Watcher. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the Connection Monitor. Changing this forces a new resource to be created.
    """
    source: pulumi.Output[dict]
    """
    A `source` block as defined below.
    
      * `port` (`float`)
      * `virtual_machine_id` (`str`)
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, auto_start=None, destination=None, interval_in_seconds=None, location=None, name=None, network_watcher_name=None, resource_group_name=None, source=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Configures a Network Connection Monitor to monitor communication between a Virtual Machine and an endpoint using a Network Watcher.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_start: Specifies whether the connection monitor will start automatically once created. Defaults to `true`. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] destination: A `destination` block as defined below.
        :param pulumi.Input[float] interval_in_seconds: Monitoring interval in seconds. Defaults to `60`.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Network Connection Monitor. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_watcher_name: The name of the Network Watcher. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Connection Monitor. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] source: A `source` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        
        The **destination** object supports the following:
        
          * `address` (`pulumi.Input[str]`)
          * `port` (`pulumi.Input[float]`)
          * `virtual_machine_id` (`pulumi.Input[str]`)
        
        The **source** object supports the following:
        
          * `port` (`pulumi.Input[float]`)
          * `virtual_machine_id` (`pulumi.Input[str]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/network_connection_monitor.html.markdown.
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

            __props__['auto_start'] = auto_start
            if destination is None:
                raise TypeError("Missing required property 'destination'")
            __props__['destination'] = destination
            __props__['interval_in_seconds'] = interval_in_seconds
            __props__['location'] = location
            __props__['name'] = name
            if network_watcher_name is None:
                raise TypeError("Missing required property 'network_watcher_name'")
            __props__['network_watcher_name'] = network_watcher_name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if source is None:
                raise TypeError("Missing required property 'source'")
            __props__['source'] = source
            __props__['tags'] = tags
        super(NetworkConnectionMonitor, __self__).__init__(
            'azure:network/networkConnectionMonitor:NetworkConnectionMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, auto_start=None, destination=None, interval_in_seconds=None, location=None, name=None, network_watcher_name=None, resource_group_name=None, source=None, tags=None):
        """
        Get an existing NetworkConnectionMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_start: Specifies whether the connection monitor will start automatically once created. Defaults to `true`. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] destination: A `destination` block as defined below.
        :param pulumi.Input[float] interval_in_seconds: Monitoring interval in seconds. Defaults to `60`.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Network Connection Monitor. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_watcher_name: The name of the Network Watcher. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Connection Monitor. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] source: A `source` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        
        The **destination** object supports the following:
        
          * `address` (`pulumi.Input[str]`)
          * `port` (`pulumi.Input[float]`)
          * `virtual_machine_id` (`pulumi.Input[str]`)
        
        The **source** object supports the following:
        
          * `port` (`pulumi.Input[float]`)
          * `virtual_machine_id` (`pulumi.Input[str]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/network_connection_monitor.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["auto_start"] = auto_start
        __props__["destination"] = destination
        __props__["interval_in_seconds"] = interval_in_seconds
        __props__["location"] = location
        __props__["name"] = name
        __props__["network_watcher_name"] = network_watcher_name
        __props__["resource_group_name"] = resource_group_name
        __props__["source"] = source
        __props__["tags"] = tags
        return NetworkConnectionMonitor(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

