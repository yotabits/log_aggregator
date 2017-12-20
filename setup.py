from setuptools import setup

setup(name='log_aggregator',
      version='0.1',
      description='Create a configurable Tarball of various files in the file system',
      author='Thomas Kostas',
      author_email='tkostas75@gmail.com',
      license='MIT',
      packages=['log_aggregator'],
      scripts=['bin/log_aggregator'],
      install_requires=['pycurl',
                        'appjar'
      ],
      zip_safe=False)