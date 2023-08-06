from setuptools import setup
import tsconv

description = 'Convert unix timestamp in sec/millisec/microsec/nanosec to human readable time'

setup(name='tsconv',
      version=tsconv.VERSION,
      description=description,
      long_description=description,
      author='Xiaoyong Guo',
      author_email='guo.xiaoyong@gmail.com',
      url='https://github.com/guoxiaoyong/tsconv',
      install_requires=['pytz'],
      setup_requires=['pytz'],
      packages=['tsconv'],
      include_package_data=True,
      entry_points={
         'console_scripts': ['tsconv=tsconv:main'],
      },
)
