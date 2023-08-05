# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['try_match']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'try-match',
    'version': '0.2.0',
    'description': 'Pattern matching',
    'long_description': '# try_match\nPattern matching\n\nIt supports Python 2.7 and 3+\n\n# Installation\nUsing pip to install\n```bash\npip install try-match\n```\n\n# Usage\n```python\nfrom try_match import Case, match, DefaultCase\n\n### match value\ntry:\n    match(1)\nexcept Case(2):\n    raise\nexcept Case(1):\n    print(1)\n   \n# => 1\n\n\n### match class\ntry:\n    match(1)\nexcept Case(str):\n    raise\nexcept Case(int):\n    print(\'int\')\n    \n# => \'int\'\n\n\n### match range\ntry:\n    match(10)\nexcept Case(range(1, 5)):\n    raise\nexcept Case(range(9, 20)):\n    print(range(9, 20))\n    \n# => range(9, 20)\n\n\n### match lambda\ntry:\n    match(2)\nexcept Case(lambda x > 5):\n    raise\nexcept Case(lambda x < 5):\n     print("x < 5")\n     \n# => "x < 5"\n\n\n### default case\ntry:\n    match(1)\nexcept Case(2):\n    raise\nexcept Case(3):\n    raise\nexcept DefaultCase:\n    print("default")\n    \n# => "default"\n```\n\n✨🍰✨ enjoy it\n',
    'author': 'Zhengyu Xu',
    'author_email': 'zen-xu@outlook.com',
    'url': 'https://github.com/zen-xu/try_match',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7,<4',
}


setup(**setup_kwargs)
