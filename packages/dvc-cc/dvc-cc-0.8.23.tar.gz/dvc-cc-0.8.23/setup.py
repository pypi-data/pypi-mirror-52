# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dvc_cc',
 'dvc_cc.cancel',
 'dvc_cc.dvc',
 'dvc_cc.git',
 'dvc_cc.hyperopt',
 'dvc_cc.init',
 'dvc_cc.live_output',
 'dvc_cc.output_to_tmp',
 'dvc_cc.output_to_tmp_fast',
 'dvc_cc.run',
 'dvc_cc.run_all_defined',
 'dvc_cc.setting',
 'dvc_cc.status']

package_data = \
{'': ['*']}

install_requires = \
['cc-faice>=8.0,<9.0',
 'dvc>=0,<1',
 'keyring>=19.0,<20.0',
 'matplotlib>=3.1,<4.0',
 'nbconvert>=5.5,<6.0',
 'numpy>=1.16,<2.0',
 'pandas>=0,<1',
 'paramiko>=2.4,<3.0',
 'pyrsistent>=0.15.2,<0.16.0',
 'python-gitlab>=1.8,<2.0',
 'pyyaml>=5.1,<6.0',
 'seaborn>=0,<1']

entry_points = \
{'console_scripts': ['dvc-cc = dvc_cc.main:main']}

setup_kwargs = {
    'name': 'dvc-cc',
    'version': '0.8.23',
    'description': 'This connector is used to combine the work of CC (www.curious-containers.cc) and DVC (Open-source Version Control System for Machine Learning Projects).',
    'long_description': '![The DVC-CC-Logo](../dvc_cc_logo.png)\n\n\n- TODO: SOME DESCRIPTION\n- TODO: GIF of how to use DVC-CC basic commands\n\n## Installation of DVC-CC\n\nDVC-CC is written in python so you can easily install DVC-CC by using pip. We recommend that you install DVC-CC in an [anaconda](https://www.anaconda.com/distribution/) environment.\nYou can create, and activate an environment with the following lines:\n\n```bash\nconda create --name dvc_cc python pip\nconda activate dvc_cc\n```\n\n### Installation with pip\nThe following script will install the client on your computer:\n\n```bash\npip install --upgrade dvc-cc\n```\n\n### Installation from source\n\nIf you want to install the latest version from source you can install it with [poetry](https://poetry.eustace.io/).\n\n```bash\ngit clone https://github.com/deep-projects/dvc-cc.git\ncd dvc-cc/dvc-cc\npoetry build\npip install dvc_cc-?????.whl # replace ????? with the current version that you build in the previous step.\n```\n\n## Get started\nInstall DVC-CC and take a look at [this tutorial](dvc-cc/tutorial/Get_Started.md).\n\n### Tutorials\n- [Working with jupyter notebooks](tutorial/_working_with_jupyter_notebook.md)\n- [working with sshfs](tutorial/_working_with_sshfs.md)\n- <del>[An old tutorial](tutorial/SimpleStart.md)</del>\n\n## Structure of this repository\n\n\n## Acknowledgements\nThe DVC-CC software is developed at CBMI (HTW Berlin - University of Applied Sciences). The work is supported by the\nGerman Federal Ministry of Education and Research (project deep.TEACHING, grant number 01IS17056 and project\ndeep.HEALTH, grant number 13FH770IX6).\n',
    'author': 'Jonas Annuscheit',
    'author_email': 'annusch@htw-berlin.de',
    'url': 'https://github.com/mastaer/dvc-cc.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
