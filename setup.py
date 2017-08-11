"""
PyRO-Tools
----------------
Ragnarok Online Data Tools.
"""
from setuptools import setup, find_packages

setup(
    name='PyRO-Tools',
    version='0.1',
    url='https://github.com/ilya-chistyakov/pyro-tools',
    license='BSD',
    author='Ilya Chistyakov',
    author_email='ilchistyakov@gmail.com',
    description=(
        'Ragnarok Online Data Tools.'
    ),
    packages=find_packages('.', exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'pillow',
    ],
)
