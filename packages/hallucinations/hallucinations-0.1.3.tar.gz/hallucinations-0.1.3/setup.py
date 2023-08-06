# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hallucinations']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1,<4.0', 'numba>=0.45.1,<0.46.0']

setup_kwargs = {
    'name': 'hallucinations',
    'version': '0.1.3',
    'description': '',
    'long_description': '# hallucinations\n\nBasic usage:\n\n```bash\n>>> import hallucinations\n...\n```\n\nThats it. \n\nNow go to your browser and open the output link of that import.',
    'author': 'Rodolfo Ferro',
    'author_email': 'rodolfoferroperez@gmail.com',
    'url': 'https://github.com/RodolfoFerro/hallucinations',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
