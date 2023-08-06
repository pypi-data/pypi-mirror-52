from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="mobypy",
    description="Python module for searching the Moby thesaurus",
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Python Software Foundation License',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: Microsoft :: Windows',
      'Operating System :: POSIX',
      'Programming Language :: Python',
      'Topic :: Text Processing :: Linguistic',
     ],
     keywords=[
        'moby', 'thesaurus', 'synonyms', 'language', 'python'
     ],
    author="Blaine McCarthy",
    url="https://github.com/blainemccarthy/mobypy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    version="1.0",
    packages=["mobypy"],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    )
