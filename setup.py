from setuptools import setup

setup(
    name='Weppy',
    version='0.1',
    packages=['weppy'],
    package_dir={'': 'src'},
    install_requires=['WebOb==1.3.1'],
    author='Rodrigo A. Lima',
    description='A lightweight web framework that encourages clean design.',
    license='BSD',
    keywords='wsgi web',
)
