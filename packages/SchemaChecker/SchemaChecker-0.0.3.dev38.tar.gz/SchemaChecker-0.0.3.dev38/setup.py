from distutils.core import setup

setup(
    name='SchemaChecker',
    version='0.0.3.dev38',
    package_dir={'': 'src'},
    packages=['schematron',
              'schematron.edo',
              'schematron.fns',
              'schematron.stat',
              'schematron.pfr'],
    install_requires=open('requirements.txt').read().splitlines(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)
