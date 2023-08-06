from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'SHORT_README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='google_search_results',
      version='1.5.2',
      description='Scrape and search localized results from Google, Bing, Baidu at scale using SerpApi.com',
      url='https://github.com/serpapi/google-search-results-python',
      author='vikoky',
      author_email='victor@serpapi.com',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
    install_requires = ["requests"],
    packages=['lib'],
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
