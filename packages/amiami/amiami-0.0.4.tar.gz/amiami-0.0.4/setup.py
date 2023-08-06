import setuptools

long_description = """
# Amiami API

A simple api wrapper around the amiami site.

Simple usage can be something like

```python
import amiami

results = amiami.search("fumofumo plush")
for item in results.items:
  print("{}, {}".format(item.productName, item.productURL))
```


Sometimes items tend to result in an unknown status because the flag -> state parsing is a bit rough. These items will be added to the list with a status of `Unknown status?`. They will also print out a message with the flags and item code. Good to check your log and see what's going on.
"""

setuptools.setup(
    name='amiami',
    version='0.0.4',
    author='marvinody',
    author_email='manny@sadpanda.moe',
    description='amiami api wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/marvinody/amiami/',
    packages=setuptools.find_packages(),
    install_requires=[
        "certifi == 2019.3.9",
        "chardet == 3.0.4",
        "idna == 2.8",
        "requests == 2.21.0",
        "urllib3 == 1.24.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
    ]
)
