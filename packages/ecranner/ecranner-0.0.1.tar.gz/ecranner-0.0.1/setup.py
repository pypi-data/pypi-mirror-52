# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ecranner']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0',
 'docker>=4.0,<5.0',
 'pyyaml>=5.1,<6.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['ecranner = ecranner.cli:main']}

setup_kwargs = {
    'name': 'ecranner',
    'version': '0.0.1',
    'description': 'Scan the vulnerability of Docker images stored in ECR',
    'long_description': '# ECRanner\n\n![](https://github.com/homoluctus/ecranner/workflows/Test/badge.svg)\n![GitHub release (latest by date)](https://img.shields.io/github/v/release/homoluctus/ecranner)\n![GitHub](https://img.shields.io/github/license/homoluctus/ecranner)\n\nThis is that scan the vulnerability of Docker images stored in ECR.<br>\n\n# Table of contents\n- [Feature](#feature)\n- [Get Started](#get-started)\n  - [Install Prerequirements](#install-prerequirements)\n  - [Install ECRanner](#install-ecranner)\n  - [Write ecranner.yml](#write-ecranner.yml)\n  - [Execute](#execute)\n- [Configuration Parameter](#configuration-parameter)\n  - [aws](#aws)\n  - [aws.\\<id\\>](#awsid)\n  - [aws.\\<id\\>.account_id](#awsidaccount_id)\n  - [aws.\\<id\\>.region](#awsidregion)\n  - [aws.\\<id\\>.aws_access_key_id](#awsidaws_access_key_id)\n  - [aws.\\<id\\>.aws_secret_access_key](#awsidaws_secret_access_key)\n  - [aws.\\<id\\>.images](#awsidimages)\n  - [trivy](#trivy)\n  - [trivy.path](#trivypath)\n  - [trivy.options](#trivyoptions)\n- [Command options](#command-options)\n\n# Feature\n- Pull Docker Image From ECR\n- Support multi account\n- Vulnerability Scan\n  - [Trivy](https://github.com/aquasecurity/trivy) detects software (OS package and application library) vulnerabilities in Docker Image\n- Slack Integration\n  - Push vulnerability information to Slack. Slack UI is as following:\n\n    <img src="https://raw.githubusercontent.com/homoluctus/ecranner/master/slack_ui.png" alt="Slack-UI" width="70%">\n\n# Get Started\n## Install Prerequirements\n\n- [Trivy](https://github.com/aquasecurity/trivy)\n- Git (Used with Trivy)\n\n## Install ECRanner\n\n```\npip install ecranner\n```\n\n## Write ecranner.yml\n\nA `ecranner.yml` looks like this:\n\n```\naws:\n  stg:\n    account_id: xxxxxxxxx\n    region: us-east-1\n    aws_access_key_id: xxxxxxxxx\n    aws_secret_access_key: xxxxxxxxx\n    images:\n      - image:latest\n      - image:1.0-dev\n  prod:\n    account_id: xxxxxxxxx\n    region: us-east-1\n    aws_access_key_id: xxxxxxxxx\n    aws_secret_access_key: xxxxxxxxx\n    images:\n      - image:1.4\n      - image:5.3\n\ntrivy:\n  path: ~/user/.local/bin/trivy\n  options: --severity CRITICAL -q\n```\n\n## Execute\n\n```\necranner\n```\n\nYou execute the above and then output the scan result to the console as follows:\n\n```\n[ { \'Target\': \'image_name:latest\'\n              \'(alpine 3.10.1)\',\n    \'Vulnerabilities\': [ { \'Description\': \'aa_read_header in \'\n                                          \'libavformat/aadec.c in FFmpeg \'\n                                          \'before 3.2.14 and 4.x before 4.1.4 \'\n                                          \'does not check for sscanf failure \'\n                                          \'and consequently allows use of \'\n                                          \'uninitialized variables.\',\n                           \'FixedVersion\': \'4.1.4-r0\',\n                           \'InstalledVersion\': \'4.1.3-r1\',\n                           \'PkgName\': \'ffmpeg\',\n                           \'References\': [ \'https://git.ffmpeg.org/gitweb/ffmpeg.git/shortlog/n4.1.4\',\n                                           \'https://github.com/FFmpeg/FFmpeg/commit/ed188f6dcdf0935c939ed813cf8745d50742014b\',\n                                           \'https://github.com/FFmpeg/FFmpeg/compare/a97ea53...ba11e40\',\n                                           \'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-12730\',\n                                           \'http://www.securityfocus.com/bid/109317\',\n                                           \'https://git.ffmpeg.org/gitweb/ffmpeg.git/commit/9b4004c054964a49c7ba44583f4cee22486dd8f2\'],\n                           \'Severity\': \'HIGH\',\n                           \'Title\': \'\',\n                           \'VulnerabilityID\': \'CVE-2019-12730\'}\n```\n\n# Configuration Parameter\nAll parameters is required.<br>\nSo, ECRanner will fail if at least one parameter is not set.\n\n## `aws`\nFirst, declare that this configuration is for AWS.\n\n## `aws.<id>`\n`<id>` must be unique.<br>\nYou are free to decide which word is `<id>`.\n\n## `aws.<id>.account_id`\nYour AWS account ID.\n\n## `aws.<id>.region`\nSpecify the region where docker images to be pulled is stored.\n\n## `aws.<id>.aws_access_key_id`\nYour IAM user\'s AWS access key ID.<br>\nAbsolutely, you should not use AWS Root account for ECRanner.\n\n## `aws.<id>.aws_secret_access_key`\nYour IAM user\'s AWS secret access key.\n\n## `aws.<id>.images`\nSpecify docker images that you want to pull.\n\n## `trivy`\nSet configuration for Trivy command.\n\n## `trivy.path`\nSpecify the path of trivy command.<br>\nYou does not need to specify the path if trivy is installed in $PATH.\n\n## `trivy.options`\nSet trivy command options as a one line string.<br>\nTo send the scan result to Slack, the `-f json` option is already set.<br>\nYou can specify all options except this option.<br>\nPlease see [Trivy documentation](https://github.com/aquasecurity/trivy#examples) in details.\n\n# Command options\n\n|option|required|default|description|\n|:--:|:--:|:--:|:--|\n|-f, --file|false|`./ecranner.yml`|Filepath to configuration in YAML.<br>Specify this option if you change configuration filename.|\n|--env-file|false|`./.env`|Specify .env file path.<br>Automatically load .env file if this file is found in current directory.|\n|--slack|false|N/A|Send the scan result to Slack.<br>If you use this option, set incoming webhooks url as system environment variable like this:<br>`export SLACK_WEBHOOK=https://xxxxxxxxxx`|\n|--rm|false|N/A|Remove images after scan with Trivy.|\n|-q, --quiet|false|N/A|Suppress logging message.|\n|--no-cache|false|N/A|***Implement in the future, so you can not use this option***<br>Disable to store cache.<br>This command does not use cache, but Trivy command use cache.|\n|-h, --help|false|N/A|Show command option usage.|',
    'author': 'homoluctus',
    'author_email': 'w.slife18sy@gmail.com',
    'url': 'https://github.com/homoluctus/ecranner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
