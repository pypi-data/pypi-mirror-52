# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nimi']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0',
 'click>=7.0,<8.0',
 'jinja2>=2.10,<3.0',
 'requests>=2.22,<3.0',
 'terminaltables>=3.1,<4.0']

entry_points = \
{'console_scripts': ['nimi = nimi:cli.cli']}

setup_kwargs = {
    'name': 'nimi',
    'version': '0.2.0',
    'description': 'Painless Dynamic DNS with AWS',
    'long_description': "# Nimi - Painless Dynamic DNS with AWS\n\nNimi is yet another self-hosted dynamic DNS solution, built using Python, AWS Route53, Lambda\nand API Gateway.\n\nWhile there are numerous implementations of similar systems available, this project was motivated\nby some of the shortcomings of projects I reviewed:\n\n- The setup process is often manual, which is tedious and error prone.\n- The clients interact directly with the cloud providers API, requiring appropriate credentials\n  to be configured on each host.\n\nNimi aims to be easy to setup, manage and destroy - the tool provisions and tears down all the\nrequired AWS infrastructure. The dynamic DNS client does not interact with any AWS API's directly\nand can be deployed on any host with a bit more peace of mind.\n\n[![asciicast](https://asciinema.org/a/KO9RCVwMeQ05c8eCiC615UWpa.svg)](https://asciinema.org/a/KO9RCVwMeQ05c8eCiC615UWpa)\n\n## Installation\n\n```\npip install nimi\n```\n\n## Usage\n\nThe package will install the `nimi` command line tool, which is used to setup the AWS infrastructure\nwith CloudFront, add and remove domains from Route53 and configure dynamic DNS hostnames. This\nrequires valid AWS credentials to be configured.\nThe subcommand `nimi client` is for use on the hosts added to the system and don't require any AWS\ncredentials. Instead, it's configured with values generated during the setup.\n\n### Credentials\n\nThe `nimi` tool does not accept credentials explicitly and expects them to be configured either in\nthe environment or configuration file as described in the\n[AWS CLI documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).\n\n### Provision infrastructure\n\nIn order to use Nimi, corresponding AWS infrastructure must be provisioned first. This is done\nautomatically using CloudFormation by invoking the following command.\n\n```\nnimi setup\n```\n\n### Add a domain\n\nIf your domain is already configured in Route53, skip this step. Otherwise run the following command\nto create a new hosted zone. Once complete, the output will include a list of name servers, which\nyou will have to configure with your domain registrar.\n\n```\nnimi import <domain>\n```\n\n### Add a host\n\nBefore running `nimi client`, the desired hostname has to be configured. Invoking the following\ncommand will add the hostname to the configuration and generate a shared secret, that the client\napplication will use to sign requests sent to the system. The hostname can either be the root domain\nor a subdomain of any domain configured in Route53.\n\n```\nnimi add <hostname>\n```\n\n### Configure client\n\nThe `nimi client` subcommands do not need or use any AWS credentials. Instead, the\ndeployments API URL, desired hostname and shared secret have to be passed as options to the command\nor set as environment variables. Each configured hostname must be paired with a unique shared\nsecret, while the API URL is common between them all. Invoke the following command to view said\ninformation.\n\n```\nnimi info\n```\n\nMake note of the configured values for the hostname you added. The mapping of values to environment\nvariables and command line options are marked below.\n\n| Value         | Environment   | Option   |\n| ------------- | ------------- | -------- |\n| API URL       | NIMI_URL      | URL      |\n| Hostname      | NIMI_HOSTNAME | HOSTNAME |\n| Shared Secret | NIMI_SECRET   | SECRET   |\n\nSet the required environment variables and run the following command on the host you want to enable\ndynamic DNS for.\n\n```\nnimi client ping\n```\n\nAlternatively pass the values as command line options.\n\n```\nnimi client ping URL HOSTNAME SECRET\n```\n\nThe `ping` command sends a single request to the provisioned backend. The payload includes the\ndesired hostname and its HMAC-SHA256 hash created using the shared secret. The backend will validate\nthe request by comparing the hash and update the corresponding DNS `A` record if the source IP\naddress has changed.\n\n### Running client periodically\n\nThe `ping` command should be run periodically on the host to ensure the DNS records stay up to date.\nThe client currently has no means to setup periodic execution automatically.\nUsers should schedule the command to be executed at a desired interval using tools available on\nthe hosts platform, i.e. [Cron](https://help.ubuntu.com/community/CronHowto) on Linux or\n[launchd](https://www.launchd.info) on Mac OS.\n\n### Cleanup\n\nIf you wish to stop using the system, the `nimi` command line tool includes commands to delete\nanything you configured with it.\n\nRemove a configured hostname, any subsequent pings will have no effect.\n\n```\nnimi remove <hostname>\n```\n\nRemove a domain from Route53 and all associated hostnames.\n\n```\nnimi eject <domain>\n```\n\nCompletely remove provisioned AWS infrastructure. Does not remove any domains from Route53.\n\n```\nnimi destroy\n```\n\n## Cost\n\nFor personal use, the cost of running the system should be neglieble, but not completely free.\nAWS Lambda includes a [geneours free tier](https://aws.amazon.com/lambda/pricing/) with up to\na million requests per month for free and your usage should stay well within those limits.\n\nAPI Gateways free tier is only valid for the first 12 months of the account, but for a small\ndeployment [the pricing](https://aws.amazon.com/api-gateway/pricing/) is reasonable and usually\ncomes to about \\$0.02 per month for a deployment with a couple of hosts pinging every 5 to 10\nminutes.\n\nThe most costly part of the deployment is [Route53](https://aws.amazon.com/route53/pricing/),\nwhich charges \\$0.50 per hosted zone (domain), as well as for DNS queries served, though for a\npersonal deployment the latter should be small enough to not be reflected in the bill.\n\nThere is no reason the system couldn't support other DNS providers that are cheaper or free, if\nyou'd like to extend support feel free to contribute.\n",
    'author': 'Martin Raag',
    'author_email': 'hi@mraag.xyz',
    'url': 'https://github.com/martinraag/nimi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
