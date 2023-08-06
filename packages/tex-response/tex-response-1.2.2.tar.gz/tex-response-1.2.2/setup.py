# -*- coding: utf-8 -*-

"""
For installing with pip
"""

from distutils.core import setup
import setuptools  # keep!

setup(
    name='tex-response',
    version='1.2.2',
    author=u'Mark V',
    author_email='markv.nl.dev@gmail.com',
    packages=['tex_response'],
    include_package_data=True,
    url='https://github.com/mverleg/django_tex_response',
    license='revised BSD license; see LICENSE.txt',
    description='Simple Django code that lets you use your installed luatex compiler to render a .tex template to a pdf-file response.',
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # 'Topic :: Utilities',
    ],
    install_requires=[
        'django',
    ],
)
