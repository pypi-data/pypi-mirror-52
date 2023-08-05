# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetAppServicePlanResult:
    """
    A collection of values returned by getAppServicePlan.
    """
    def __init__(__self__, is_xenon=None, kind=None, location=None, maximum_elastic_worker_count=None, maximum_number_of_workers=None, name=None, properties=None, resource_group_name=None, sku=None, tags=None, id=None):
        if is_xenon and not isinstance(is_xenon, bool):
            raise TypeError("Expected argument 'is_xenon' to be a bool")
        __self__.is_xenon = is_xenon
        """
        A flag that indicates if it's a xenon plan (support for Windows Container)
        """
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        __self__.kind = kind
        """
        The Operating System type of the App Service Plan
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        """
        The Azure location where the App Service Plan exists
        """
        if maximum_elastic_worker_count and not isinstance(maximum_elastic_worker_count, float):
            raise TypeError("Expected argument 'maximum_elastic_worker_count' to be a float")
        __self__.maximum_elastic_worker_count = maximum_elastic_worker_count
        """
        The maximum number of total workers allowed for this ElasticScaleEnabled App Service Plan.
        """
        if maximum_number_of_workers and not isinstance(maximum_number_of_workers, float):
            raise TypeError("Expected argument 'maximum_number_of_workers' to be a float")
        __self__.maximum_number_of_workers = maximum_number_of_workers
        """
        Maximum number of instances that can be assigned to this App Service plan.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if properties and not isinstance(properties, list):
            raise TypeError("Expected argument 'properties' to be a list")
        __self__.properties = properties
        """
        A `properties` block as documented below.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        __self__.sku = sku
        """
        A `sku` block as documented below.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the resource.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetAppServicePlanResult(GetAppServicePlanResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAppServicePlanResult(
            is_xenon=self.is_xenon,
            kind=self.kind,
            location=self.location,
            maximum_elastic_worker_count=self.maximum_elastic_worker_count,
            maximum_number_of_workers=self.maximum_number_of_workers,
            name=self.name,
            properties=self.properties,
            resource_group_name=self.resource_group_name,
            sku=self.sku,
            tags=self.tags,
            id=self.id)

def get_app_service_plan(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing App Service Plan (formerly known as a `Server Farm`).
    
    :param str name: The name of the App Service Plan.
    :param str resource_group_name: The Name of the Resource Group where the App Service Plan exists.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/d/app_service_plan.html.markdown.
    """
    __args__ = dict()

    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:appservice/getAppServicePlan:getAppServicePlan', __args__, opts=opts).value

    return AwaitableGetAppServicePlanResult(
        is_xenon=__ret__.get('isXenon'),
        kind=__ret__.get('kind'),
        location=__ret__.get('location'),
        maximum_elastic_worker_count=__ret__.get('maximumElasticWorkerCount'),
        maximum_number_of_workers=__ret__.get('maximumNumberOfWorkers'),
        name=__ret__.get('name'),
        properties=__ret__.get('properties'),
        resource_group_name=__ret__.get('resourceGroupName'),
        sku=__ret__.get('sku'),
        tags=__ret__.get('tags'),
        id=__ret__.get('id'))
