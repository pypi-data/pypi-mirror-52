from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='mLab-WalkSpeed-Radar-Tool',
      version='0.0.2',
      packages=['mLab_WalkSpeedRadar'],
      install_requires=[
          'pyserial','pyqtgraph'
      ],
      include_package_data=True,
      url='', license='MIT',
      author='Alex Kuan',
      author_email='agathakuannew@gmail.com',
      description='mLab WalkSpeed Radar UART tool and example code',
      long_description=long_description,
      long_description_content_type='text/markdown')