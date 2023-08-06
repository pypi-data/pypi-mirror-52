import os

from nimi.stack import Stack
from nimi.route53 import find_hosted_zone_id, get_alias_record
from nimi.function import Function, env_from_config


def setup(name):
    """Create new CloudFormation stack."""

    stack = Stack(name)
    stack.create()


def add_hostname(stack, hostname, secret=None):
    """Add hostname to dynamic DNS"""

    hosted_zone_id = find_hosted_zone_id(hostname)
    secret = secret if secret else os.urandom(16).hex()

    # Update existing function environment with new values
    function = Function(stack.get_output("LambdaFunctionName"))
    config = function.get_config()
    config[hostname] = {"hosted_zone_id": hosted_zone_id, "shared_secret": secret}
    env = env_from_config(config)

    # Create a list of unique hosted zone id's
    hosted_zones = [host["hosted_zone_id"] for host in config.values()]
    hosted_zones.append(hosted_zone_id)
    hosted_zones = list(set(hosted_zones))

    stack.update(hosted_zones=hosted_zones, env=env)


def remove_hostname(stack, hostname):
    """Remove hostname and configured records from dynamic DNS"""

    function = Function(stack.get_output("LambdaFunctionName"))
    config = function.get_config()

    if not hostname in config:
        return

    # TODO: Remove Route53 records
    del config[hostname]
    env = env_from_config(config)

    hosted_zones = [host["hosted_zone_id"] for host in config.values()]
    hosted_zones = list(set(hosted_zones))

    stack.update(hosted_zones=hosted_zones, env=env)


def get_info(stack):
    """Get dynamic DNS configuration info."""

    api_url = stack.get_output("ApiUrl")
    function = Function(stack.get_output("LambdaFunctionName"))
    config = function.get_config()

    return {"url": api_url, "hosts": config}


def destroy(stack):
    """Remove CloudFormation stack and configured DNS records"""

    # TODO: Remove Route53 records
    stack.destroy()
