from distutils.core import setup
from setuptools import find_packages

setup(name='gdmTool',
      version='0.0.2',
      description='A dataset tool for converting all images in a folder into neural network recognition',
      long_description='Gdm is a graphical data modeling product developed by the cosmosource company. The main functions are graphical development of machine learning tasks with Spark as the engine, and graphical development of deep learning tasks with Tensorflow as the engine.',
      author='cosmosource',
      author_email='gaoyuan@cosmosource.com',
      url='http://www.cosmosource.com/',
      license='GPLv3',
      install_requires=[
        'opencv-python>=4.1.1.26',
        'numpy>=1.15.0'
      ],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      )
