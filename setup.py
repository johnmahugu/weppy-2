from setuptools import setup, find_packages

setup(
    name='Weppy',
    version='0.1',
    packages=['weppy'],
    package_dir={'': 'src'},
    install_requires=['WebOb==1.3.1', 'redis==2.10.1', 'pymongo==2.7.2'],
    author='Rodrigo A. Lima',
    author_email='rodrigoalima99@gmail.com',
    description='A lightweight web framework that encourages clean design.',
    license='BSD',
    keywords='wsgi web',
    url='http://weppyweb.org'
)
