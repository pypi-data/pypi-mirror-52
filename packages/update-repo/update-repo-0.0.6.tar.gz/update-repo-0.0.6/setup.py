r'''
Clone/pull a git repo
'''
# pylint: disable=invalid-name
from pathlib import Path
import re

from setuptools import setup, find_packages  # type: ignore

name = "update-repo"
# description = ' '.join(name.split('-'))
description = 'clone/pull a repo'
dir_name, = find_packages()

version, = re.findall(r"\n__version__\W*=\W*'([^']+)'", open('%s/__init__.py' % dir_name).read())

README_rst = '%s/README.md' % Path(__file__).parent
long_description = open(README_rst, encoding='utf-8').read() if Path(README_rst).exists() else ''
if Path('requirements.txt').exists():
    install_requires = [elm.split()[0] for elm in Path('requirements.txt').read_text(encoding='utf-8').split('\n')]
else:
    install_requires = []

setup(
    name=name,
    packages=find_packages(),
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['git', 'colab'],
    author="mikeee",
    url='http://github.com/ffreemt/%s' % name,
    download_url='https://github.com/ffreemt/%s/archive/v_%s.tar.gz' % (name, version),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT License',
)
