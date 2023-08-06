from setuptools import setup, find_packages

setup(
    name='pypcc',
    version='0.0.3',
    url='https://github.com/caiocarneloz/pycc',
    license='MIT License',
    author='Caio Carneloz',
    author_email='caiocarneloz@gmail.com',
    keywords='Semi-supervised',
    description=u'Semi-supervised method particle competition and cooperation',
    packages=find_packages(),
    install_requires=['numpy'],
)