# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pymedphys',
 'pymedphys._base',
 'pymedphys._dicom',
 'pymedphys._dicom.constants',
 'pymedphys._dicom.ct',
 'pymedphys._dicom.delivery',
 'pymedphys._dicom.rtplan',
 'pymedphys._dicom.shim',
 'pymedphys._dicom.utilities',
 'pymedphys._electronfactors',
 'pymedphys._gamma',
 'pymedphys._gamma.api',
 'pymedphys._gamma.implementation',
 'pymedphys._gamma.utilities',
 'pymedphys._mocks',
 'pymedphys._mosaiq',
 'pymedphys._mudensity',
 'pymedphys._mudensity.delivery',
 'pymedphys._mudensity.plt',
 'pymedphys._trf',
 'pymedphys._utilities',
 'pymedphys._utilities.algorithms',
 'pymedphys._utilities.constants',
 'pymedphys._utilities.filehash',
 'pymedphys._utilities.transforms',
 'pymedphys.cli',
 'pymedphys.docker',
 'pymedphys.labs',
 'pymedphys.labs.fileformats',
 'pymedphys.labs.fileformats.mapcheck',
 'pymedphys.labs.fileformats.mephysto',
 'pymedphys.labs.fileformats.profiler',
 'pymedphys.labs.film',
 'pymedphys.labs.managelogfiles',
 'pymedphys.labs.paulking',
 'pymedphys.labs.pedromartinez',
 'pymedphys.labs.pinnacle',
 'pymedphys.labs.tpscompare',
 'pymedphys.labs.winstonlutz']

package_data = \
{'': ['*'],
 'pymedphys.docker': ['nginx/*',
                      'orthanc/*',
                      'orthanc/orthanc-and-miniconda/*',
                      'orthanc/scripts/*']}

extras_require = \
{'all': ['attrs',
         'keyring',
         'packaging',
         'tqdm',
         'python_dateutil',
         'PyYAML',
         'numpy>=1.12,<2.0',
         'matplotlib',
         'scipy',
         'pandas',
         'Pillow',
         'imageio',
         'scikit-image',
         'pymssql',
         'shapely',
         'pydicom']}

entry_points = \
{'console_scripts': ['pymedphys = pymedphys.cli.main:pymedphys_cli']}

setup_kwargs = {
    'name': 'pymedphys',
    'version': '0.12.0.dev0',
    'description': '',
    'long_description': '=========\nPyMedPhys\n=========\n\n|build| |pypi| |conda| |python| |license|\n\n.. |build| image:: https://dev.azure.com/pymedphys/pymedphys/_apis/build/status/pymedphys.pymedphys?branchName=master\n    :target: https://dev.azure.com/pymedphys/pymedphys/_build/latest?definitionId=4&branchName=master\n\n.. |pypi| image:: https://img.shields.io/pypi/v/pymedphys.svg\n    :target: https://pypi.org/project/pymedphys/\n\n.. |conda| image:: https://img.shields.io/conda/vn/conda-forge/pymedphys.svg\n    :target: https://anaconda.org/conda-forge/pymedphys/\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/pymedphys.svg\n    :target: https://pypi.org/project/pymedphys/\n\n.. |license| image:: https://img.shields.io/pypi/l/pymedphys.svg\n    :target: https://choosealicense.com/licenses/agpl-3.0/\n\n\n.. START_OF_ABOUT_IMPORT\n\nBringing together Medical Physicists to create quality transparent software at\na price affordable by all our peers, no matter what country they are from (free).\n\nPyMedPhys, a community powered by git and continuous integration. A place to\nshare, review, improve, and transparently learn off of each other’s code. \nIt is a library of tools that we all have access to and, because of its\n`license`_, will all have access to whatever it becomes in the future.\nIt is inspired by the collaborative work of our physics peers in\nastronomy and their `Astropy Project`_.\n\n.. _`Astropy Project`: http://www.astropy.org/\n\n.. _`license`: https://choosealicense.com/licenses/agpl-3.0/\n\n\nThis package is available on `PyPI`_, `GitHub`_ and `conda-forge`_. You\ncan access the Documentation `here <https://pymedphys.com>`__.\n\n\n.. _`PyPI`: https://pypi.org/project/pymedphys/\n.. _`GitHub`: https://github.com/pymedphys/pymedphys\n.. _`conda-forge`: https://anaconda.org/conda-forge/pymedphys\n\n\nPyMedPhys is currently within the ``beta`` stage of its lifecycle. It will\nstay in this stage until the version number leaves ``0.x.x`` and enters\n``1.x.x``. While PyMedPhys is in ``beta`` stage, **no API is guaranteed to be\nstable from one release to the next.** In fact, it is very likely that the\nentire API will change multiple times before a ``1.0.0`` release. In practice,\nthis means that upgrading ``pymedphys`` to a new version will possibly break\nany code that was using the old version of pymedphys. We try to be abreast of\nthis by providing details of any breaking changes from one release to the next\nwithin the `Release Notes\n<http://pymedphys.com/getting-started/changelog.html>`__.\n\n\nOur Team\n--------\n\nPyMedPhys is what it is today due to its maintainers and developers. The\ncurrently active developers and maintainers of PyMedPhys are given below\nalong with their affiliation:\n\n* `Simon Biggs`_\n    * `Riverina Cancer Care Centre`_, Australia\n\n.. _`Simon Biggs`: https://github.com/SimonBiggs\n\n\n* `Matthew Jennings`_\n    * `Royal Adelaide Hospital`_, Australia\n\n.. _`Matthew Jennings`: https://github.com/Matthew-Jennings\n\n\n* `Phillip Chlap`_\n    * `University of New South Wales`_, Australia\n    * `South Western Sydney Local Health District`_, Australia\n\n.. _`Phillip Chlap`: https://github.com/pchlap\n\n\n* `Paul King`_\n    * `Anderson Regional Cancer Center`_, United States\n\n.. _`Paul King`: https://github.com/kingrpaul\n\n\n* `Matthew Sobolewski`_\n    * `Riverina Cancer Care Centre`_, Australia\n    * `Northern Beaches Cancer Care`_, Australia\n\n.. _`Matthew Sobolewski`: https://github.com/msobolewski\n\n\n* `Jacob McAloney`_\n    * `Riverina Cancer Care Centre`_, Australia\n\n.. _`Jacob McAloney`: https://github.com/JacobMcAloney\n\n\n* `Pedro Martinez`_\n    * `University of Calgary`_, Canada\n    * `Tom Baker Cancer Centre`_, Canada\n\n.. _`Pedro Martinez`: https://github.com/peterg1t\n\n\n|rccc| |rah| |jarmc| |nbcc| |uoc|\n\n\n.. |rccc| image:: https://github.com/pymedphys/pymedphys/raw/master/docs/logos/rccc_200x200.png\n    :target: `Riverina Cancer Care Centre`_\n\n.. |rah| image:: https://github.com/pymedphys/pymedphys/raw/master/docs/logos/gosa_200x200.png\n    :target: `Royal Adelaide Hospital`_\n\n.. |jarmc| image:: https://github.com/pymedphys/pymedphys/raw/master/docs/logos/jarmc_200x200.png\n    :target: `Anderson Regional Cancer Center`_\n\n.. |nbcc| image:: https://github.com/pymedphys/pymedphys/raw/master/docs/logos/nbcc_200x200.png\n    :target: `Northern Beaches Cancer Care`_\n\n.. |uoc| image:: https://github.com/pymedphys/pymedphys/raw/master/docs/logos/uoc_200x200.png\n    :target: `University of Calgary`_\n\n.. _`Riverina Cancer Care Centre`: http://www.riverinacancercare.com.au/\n\n.. _`Royal Adelaide Hospital`: http://www.rah.sa.gov.au/\n\n.. _`University of New South Wales`: https://www.unsw.edu.au/\n\n.. _`South Western Sydney Local Health District`: https://www.swslhd.health.nsw.gov.au/\n\n.. _`Anderson Regional Cancer Center`: http://www.andersonregional.org/CancerCenter.aspx\n\n.. _`Northern Beaches Cancer Care`: http://www.northernbeachescancercare.com.au/\n\n.. _`University of Calgary`: http://www.ucalgary.ca/\n\n.. _`Tom Baker Cancer Centre`: https://www.ahs.ca/tbcc\n\n\nWe want you on this list. We want you, whether you are a  clinical\nMedical Physicist, PhD or Masters student, researcher, or even just\nsomeone with an interest in Python to join our team. We want you if you\nhave a desire to create and validate a toolbox we can all use to improve\nhow we care for our patients.\n\nThe aim of PyMedPhys is that it will be developed by an open community\nof contributors. We use a shared copyright model that enables all\ncontributors to maintain the copyright on their contributions. All code\nis licensed under the AGPLv3+ with additional terms from the Apache-2.0\nlicense.\n\n\n.. END_OF_ABOUT_IMPORT\n\n\nBeta stage development\n----------------------\n\nThese libraries are currently under beta level development.\nBe prudent with the code in this library.\n\nThroughout the lifetime of this library the following disclaimer will\nalways hold:\n\n    In no event and under no legal theory, whether in tort (including\n    negligence), contract, or otherwise, unless required by applicable\n    law (such as deliberate and grossly negligent acts) or agreed to in\n    writing, shall any Contributor be liable to You for damages,\n    including any direct, indirect, special, incidental, or\n    consequential damages of any character arising as a result of this\n    License or out of the use or inability to use the Work (including\n    but not limited to damages for loss of goodwill, work stoppage,\n    computer failure or malfunction, or any and all other commercial\n    damages or losses), even if such Contributor has been advised of the\n    possibility of such damages.\n\nWhere the definition of License is taken to be the\nAGPLv3+ with additional terms from the Apache 2.0. The definitions of\nContributor, You, and Work are as defined within the Apache 2.0 license.\n\n\n.. END_OF_FRONTPAGE_IMPORT\n\n\nInstallation\n------------\n\nFor instructions on how to install see the documentation at\nhttps://pymedphys.com/getting-started/installation.html.\n\n\nContributing\n------------\n\nSee the contributor documentation at\nhttps://pymedphys.com/developer/contributing.html\nif you wish to create and validate open source Medical Physics tools\ntogether.\n',
    'author': 'Simon Biggs',
    'author_email': 'me@simonbiggs.net',
    'url': 'https://pymedphys.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
