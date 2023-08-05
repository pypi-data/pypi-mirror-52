# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetJobCollectionResult:
    """
    A collection of values returned by getJobCollection.
    """
    def __init__(__self__, location=None, name=None, quotas=None, resource_group_name=None, sku=None, state=None, tags=None, id=None):
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        """
        The Azure location where the resource exists.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if quotas and not isinstance(quotas, list):
            raise TypeError("Expected argument 'quotas' to be a list")
        __self__.quotas = quotas
        """
        The Job collection quotas as documented in the `quota` block below.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        __self__.sku = sku
        """
        The Job Collection's pricing level's SKU.
        """
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        __self__.state = state
        """
        The Job Collection's state.
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
class AwaitableGetJobCollectionResult(GetJobCollectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetJobCollectionResult(
            location=self.location,
            name=self.name,
            quotas=self.quotas,
            resource_group_name=self.resource_group_name,
            sku=self.sku,
            state=self.state,
            tags=self.tags,
            id=self.id)

def get_job_collection(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing Scheduler Job Collection.
    
    > **NOTE:** Support for Scheduler Job Collections has been deprecated by Microsoft in favour of Logic Apps ([more information can be found at this link](https://docs.microsoft.com/en-us/azure/scheduler/migrate-from-scheduler-to-logic-apps)) - as such we plan to remove support for this data source as a part of version 2.0 of the AzureRM Provider.
    
    :param str name: Specifies the name of the Scheduler Job Collection.
    :param str resource_group_name: Specifies the name of the resource group in which the Scheduler Job Collection resides.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/d/scheduler_job_collection.html.markdown.
    """
    __args__ = dict()

    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:scheduler/getJobCollection:getJobCollection', __args__, opts=opts).value

    return AwaitableGetJobCollectionResult(
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        quotas=__ret__.get('quotas'),
        resource_group_name=__ret__.get('resourceGroupName'),
        sku=__ret__.get('sku'),
        state=__ret__.get('state'),
        tags=__ret__.get('tags'),
        id=__ret__.get('id'))
