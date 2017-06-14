try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Spaceship',
    'author': 'Tadas S.',
    'url': 'https://github.com/tadas-s',
    'download_url': 'https://github.com/tadas-s',
    # 'author_email': '...',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['spaceship'],
    'scripts': [],
    'name': 'spaceship'
}

setup(**config)