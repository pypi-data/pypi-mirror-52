from setuptools import setup, find_packages
print(find_packages())
required_packages = []
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()
#print(reqs)

setup(
      name='pybaobab',
      version='0.1.0',
      author='Ji Won Park',
      author_email='jiwon.christine.park@gmail.com',
      packages=find_packages(),
      license='LICENSE.md',
      description='Data generator for hierarchically modeling strongly-lensed systems with Bayesian neural networks',
      long_description=open("README.md").read(),
      long_description_content_type='text/markdown',
      url='https://github.com/jiwoncpark/baobab',
      install_requires=required_packages,
      dependency_links=[
      'http://github.com/sibirrer/fastell4py/tarball/master#egg=fastell4py',
      'http://github.com/jiwoncpark/baobab/tarball/master#egg=baobab'],
      include_package_data=True,
      entry_points={
      'console_scripts': ['generate=baobab.generate:main',],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      classifiers=['Development Status :: 4 - Beta',
      'License :: OSI Approved :: BSD License',
      'Intended Audience :: Developers',
      'Intended Audience :: Science/Research',
      'Operating System :: OS Independent',
      'Programming Language :: Python'],
      keywords='physics'
      )