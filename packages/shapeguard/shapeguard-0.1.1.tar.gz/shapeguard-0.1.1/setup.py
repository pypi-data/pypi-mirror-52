# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['shapeguard']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0',
 'tensorflow-probability>=0.7.0,<0.8.0',
 'tensorflow>=1.14,<2.0']

setup_kwargs = {
    'name': 'shapeguard',
    'version': '0.1.1',
    'description': 'ShapeGuard is a tool to help with handling shapes in Tensorflow.',
    'long_description': '# Shape Guard\n\nShapeGuard is a tool to help with handling shapes in Tensorflow.\n\n\n\n## Basic Usage\n```python\nimport tensorflow as tf\nfrom shapeguard import ShapeGuard\n\nsg = ShapeGuard()\n\nimg = tf.ones([64, 32, 32, 3])\nflat_img = tf.ones([64, 1024])\nlabels = tf.ones([64])\n\n# check shape consistency\nsg.guard(img, "B, H, W, C")\nsg.guard(labels, "B, 1")  # raises error because of rank mismatch\nsg.guard(flat_img, "B, H*W*C")  # raises error because 1024 != 32*32*3\n\n# guard also returns the tensor, so it can be inlined\nmean_img = sg.guard(tf.reduce_mean(img, axis=0), "H, W, C")\n\n# more readable reshapes\nflat_img = sg.reshape(img, \'B, H*W*C\')\n\n# evaluate templates\nassert sg[\'H, W*C+1\'] == [32, 97]\n\n# attribute access to inferred dimensions\nassert sg.B == 64\n```\n\n\n## Shape Template Syntax\nThe shape template mini-DSL supports many different ways of specifying shapes:\n\n  * numbers: `"64, 32, 32, 3"`\n  * named dimensions: `"B, width, height2, channels"`\n  * wildcards: `"B, *, *, *"`\n  * ellipsis: `"B, ..., 3"`\n  * addition, subtraction, multiplication, division: `"B*N, W/2, H*(C+1)"`\n  * dynamic dimensions: `"?, H, W, C"`  *(only matches `[None, H, W, C]`)*\n\n---\n**DISCLAIMER**\n\nThis is not an officially supported Google product.\n\n---\n',
    'author': 'Klaus Greff',
    'author_email': 'klaus.greff@startmail.com',
    'url': 'https://github.com/Qwlouse/shapeguard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
