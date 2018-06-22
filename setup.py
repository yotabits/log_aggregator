from setuptools import setup

setup(name='log_aggregator',
      version='0.41',
      description='Create a configurable Tarball of various files in the file system',
      author='Thomas Kostas',
      url='https://github.com/yotabits/log_aggregator',
      author_email='tkostas75@gmail.com',
      license='MIT',
      packages=['log_aggregator'],
      scripts=['bin/log_aggregator'],
      install_requires=['pycurl',
                        'appjar',
                        'gopher_robot_version',
                        'pillow',
                        'tqdm'
      ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        ],
      zip_safe=False)
