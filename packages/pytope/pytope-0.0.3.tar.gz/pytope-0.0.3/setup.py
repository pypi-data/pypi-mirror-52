from setuptools import setup


setup(name='pytope',
      version='0.0.3',
      description='Polytope operations --- minimal functionality',
      url='https://github.com/heirung/pytope',
      author='Tor Aksel N. Heirung',
      author_email='github@torheirung.com',
      license='MIT',
      packages=['pytope'],
      install_requires=[
        'numpy',
        'scipy',
        'pycddlib',
        'matplotlib'
      ],
      zip_safe=False)
