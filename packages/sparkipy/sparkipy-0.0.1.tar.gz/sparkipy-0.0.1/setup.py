from setuptools import setup, find_packages

REQUIRED_PACKAGES = ['unicodedata']

setup(name='sparkipy',
      install_requires=REQUIRED_PACKAGES,
      version='0.0.1',
      author="Wajdi FATHALLAH",
      author_email="wfathallah@valuraise.com",
      url="https://github.com/Valuraise/sparkipy",
      description='Framework for pyspark jobs',
      test_suite='tests',
      packages=find_packages(),
      zip_safe=False)
