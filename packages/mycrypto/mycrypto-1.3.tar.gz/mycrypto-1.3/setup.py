from distutils.core import setup
#from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:  
    long_description = fh.read()

setuptools.setup(name='mycrypto',
      version='1.3',
      description='A common cryptography encryption and decryption tools',
      long_description=long_description,
      long_description_content_type='text/markdown',
	  url='https://github.com/nightRainy/my_crypto',
      author='ZhiShi',
      author_email='foxfoxfox940@foxmail.com',
      license='MIT',
      packages=['mycrypto'],
      zip_safe=False)
