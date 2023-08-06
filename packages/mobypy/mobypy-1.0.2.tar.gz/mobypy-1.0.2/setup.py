from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read().replace(
        "|build| |issues| |coverage| |codesize| |reposize| |license|", ""
        ).replace(".. |build| image:: https://img.shields.io/badge/build-passing-success\n.. |issues| image:: https://img.shields.io/github/issues/blainemccarthy/mobypy\n.. |license| image:: https://img.shields.io/github/license/blainemccarthy/mobypy\n.. |coverage| image:: https://img.shields.io/badge/coverage-100%25-success\n.. |codesize| image:: https://img.shields.io/github/languages/code-size/blainemccarthy/mobypy\n.. |reposize| image:: https://img.shields.io/github/repo-size/blainemccarthy/mobypy", "")

    print(long_description)

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
    author_email="42183028+blainemccarthy@users.noreply.github.com",
    url="https://github.com/blainemccarthy/mobypy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    version="1.0.2",
    packages=["mobypy"],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    )
