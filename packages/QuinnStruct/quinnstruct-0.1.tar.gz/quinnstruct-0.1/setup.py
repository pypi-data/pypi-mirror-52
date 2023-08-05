from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='quinnstruct',
      version='0.1',
      description='My personal data-struct library',
      long_description='This is a data-structure library that I wrote in Python at CodeFellows in Summer 2019',
      url='http://github.com/marvincolgin/quinnstruct',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='classic data structures',
      author='Marvin Colgin',
      author_email='me@marvincolgin.com',
      license='GNU GPLv3',
      packages=['quinnstruct'],
      install_requires=[
            'os',
            'sys',
            'inspect',
            'typing',
            'collections',
            'json',
            'enum'
      ],
      include_package_data=True,
      zip_safe=False)


