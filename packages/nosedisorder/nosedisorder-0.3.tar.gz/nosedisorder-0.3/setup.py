import sys
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass
from setuptools import setup, find_packages

setup(
    name='nosedisorder',
    version='0.3',
    author='huzq',
    author_email = 'landhu@hotmail.com',
    description = 'randrom order without test_a or test_z',
    license='BSD License',
    py_modules = ['disorder'],
    #packages=find_packages(),
    platforms=["all"],
    url='https://github.com/landhu/disorder',
    entry_points = {
        'nose.plugins': [
            'disorder = disorder:Randomize'
            ]
        },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    

    )
