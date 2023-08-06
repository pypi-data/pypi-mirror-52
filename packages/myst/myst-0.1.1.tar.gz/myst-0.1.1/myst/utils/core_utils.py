"""This module contains utility functions."""
import datetime
import errno
import os

import pkg_resources
import pytz
from six.moves import urllib

import myst
from myst.constants import USER_AGENT_PREFORMAT


def get_package_version():
    """Gets the version of the Myst Python client library.

    Returns:
        version (str): Myst Python client library version
    """
    version = pkg_resources.get_distribution(myst.__package__).version
    return version


def get_user_agent():
    """Gets the `User-Agent` header string to send to the Myst API with requests.

    Returns:
        user_agent (str): user agent string
    """
    # Infer Myst API version and Myst Python client library version for current active versions.
    user_agent = USER_AGENT_PREFORMAT.format(api_version=myst.api_version, package_version=get_package_version())
    return user_agent


def get_pkg_resource_path(resource_name="", resource_package="myst.data"):
    """Gets a package resource path.

    Args:
        resource_name (str, optional): relative path to resource from `myst.data`; if not specified, will simply
            return the absolute path the the given resource package
        resource_package (str, optional): path to package where resource is stored

    Returns:
        resource_path (str): absolute path to resource
    """
    resource_path = os.path.abspath(pkg_resources.resource_filename(resource_package, resource_name))
    return resource_path


def build_resource_url(resource_name, resource_uuid=None):
    """Builds the Myst API URL for a resource.

    Args:
        resource_name (str): resource name to build URL for
        resource_uuid (str, optional): resource instance uuid; if None, this function will just return the resource
            class url

    Returns:
        resource_url (str): resource url
    """
    api_base = urllib.parse.urljoin("{api_host}/".format(api_host=myst.api_host), myst.api_version)
    resource_url = urllib.parse.urljoin("{api_base}/".format(api_base=api_base), resource_name)
    if resource_uuid is not None:
        resource_url = urllib.parse.urljoin("{resource_url}/".format(resource_url=resource_url), resource_uuid)
    return resource_url


def encode_url(base_url, params):
    """Encodes the base url using the passed get parameters.

    Args:
        base_url (str): base url
        params (list of tuple): parameters to be used in the encoded url; note that even though `urllib.parse.urlencode`
            can take `params` in dictionary form, a list of tuple preserves order, whereas a dictionary does not

    Returns:
        encoded_url (str): encoded url
    """
    # Format any special parameter types that need to be formatted.
    formatted_params = []
    for param, value in params:
        if isinstance(value, datetime.datetime):
            value = format_timestamp(value)
        formatted_params.append((param, value))

    encoded_url = "{base_url}?{params}".format(base_url=base_url, params=urllib.parse.urlencode(formatted_params))
    return encoded_url


def format_timestamp(timestamp):
    """Formats the passed timestamp according to the RFC 3339 standard.

    Args:
        timestamp (datetime.datetime): timestamp to be formatted

    Returns:
        formatted_timestamp (str): formatted timestamp
    """
    if timestamp.tzinfo is None or timestamp.tzinfo is pytz.UTC:
        formatted_timestamp = "{}Z".format(timestamp.replace(tzinfo=None).isoformat())
    else:
        formatted_timestamp = timestamp.isoformat()
    return formatted_timestamp


def make_directory(path):
    """Makes nested directories if needed safely.

    Args:
        path (str): path to directory to create
    """
    try:
        os.makedirs(path)
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise


def format_repr(class_name, class_properties=None):
    """Formats the string representation of a class.

    Args:
        class_name (str): name of the class
        class_properties (dict): properties of the class

    Returns:
        formatted_repr (str): formatted string representation
    """
    if not class_properties:
        formatted_repr = "<{class_name}>".format(class_name=class_name)
    else:
        formatted_repr = "<{class_name}: {class_properties}>".format(
            class_name=class_name,
            class_properties=", ".join(
                map(
                    lambda class_property_tuple: "{key}={value}".format(
                        key=class_property_tuple[0], value=class_property_tuple[1]
                    ),
                    class_properties.items(),
                )
            ),
        )
    return formatted_repr
