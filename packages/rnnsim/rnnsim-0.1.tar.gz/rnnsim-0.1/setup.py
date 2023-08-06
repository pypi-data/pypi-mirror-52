# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rnnsim']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16.1,<2.0.0']

entry_points = \
{'console_scripts': ['rnnsim = rnnsim.cli:main']}

setup_kwargs = {
    'name': 'rnnsim',
    'version': '0.1',
    'description': 'Random Neural Network Simulator implemented in Python.',
    'long_description': '# Overview\n\nRandom Neural Network Simulator implemented in Python.\n\n[![PyPI Version](https://img.shields.io/pypi/v/rnnsim.svg)](https://pypi.org/project/rnnsim)\n[![PyPI License](https://img.shields.io/pypi/l/rnnsim.svg)](https://pypi.org/project/rnnsim)\n\n# Setup\n\n## Requirements\n\n* Python 3.6+\n* NumPy\n* Sklearn \n\n## Installation\n\nInstall this library directly into an activated virtual environment:\n\n```bash\n$ pip install rnnsim\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```bash\n$ poetry add rnnsim\n```\n\n# Usage\n\nAfter installation, the package can either be used as:\n\n```python\n\nfrom rnnsim.model import SequentialRNN\n\nsequential_model = SequentialRNN([2, 2, 1])\nsequential_model.compile()\nsequential_model.fit(train_data=(X_train, y_train), epochs=50, metrics="acc")\nprint(sequential_model.score((X_test, y_test)))\n```\n\nor \n\n```python\nfrom rnnsim.RNN import RNN\n\n# define model connections\nconn_plus = {\n    1: [3, 4], 2: [3, 4],\n    3: [5], 4: [5], 5: []}\nconn_minus = {\n    1: [3, 4], 2: [3, 4],\n    3: [5], 4: [5], 5: []}\nmodel = RNN(n_total=5, input_neurons=2, output_neurons=1, conn_plus=conn_plus, conn_minus=conn_minus)\nmodel.fit(epochs=N_Iterations, train_data=(X, Y))\n```\n\n\nReferences\n\n1. E. Gelenbe, Random neural networks with negative and positive signals and product\nform solution," Neural Computation, vol. 1, no. 4, pp. 502-511, 1989.\n2. E. Gelenbe, Stability of the random neural network model," Neural Computation, vol.\n2, no. 2, pp. 239-247, 1990.',
    'author': 'Mandar Gogate',
    'author_email': 'contact@mandargogate.com',
    'url': 'https://pypi.org/project/rnnsim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
