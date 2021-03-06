#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class ExtraAssets(build_py):

    def run(self):
        if not self.dry_run:
            import os.path
            from pygments.formatters import HtmlFormatter
            formatter = HtmlFormatter(linenos=True, cssclass='highlight')
            target_dir = os.path.join(self.build_lib, 'pastetron/static')
            self.mkpath(target_dir)
            with open(os.path.join(target_dir, 'pygments.css'), 'w') as fh:
                fh.write(formatter.get_style_defs('.highlight'))
        build_py.run(self)


setup(
    name='pastetron',
    version='0.1.0',
    description='A pastebin application',
    long_description=open('README', 'r').read(),
    url='https://github.com/kgaughan/pastetron/',
    license='MIT',

    packages=find_packages(exclude='tests'),
    include_package_data=True,
    zip_safe=False,

    install_requires=(
        'dbkit==0.2.2',
        'mimeparse==0.1.3',
        'Pygments==1.6rc1',
        'python-creole==1.0.6',
        'web.py==0.37',
    ),

    tests_require=(
        'nose',
    ),
    test_suite='nose.collector',

    extras_require={
        'dev': (
            'coverage',
            'nose',
            'Paste',
            'PasteDeploy',
            'PasteScript',
        ),
    },

    entry_points={
        'paste.app_factory': (
            'main=pastetron:paste',
        ),
    },
    cmdclass={
        'build_py': ExtraAssets,
    },

    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ),

    author='Keith Gaughan',
    author_email='k@stereochro.me',
)
