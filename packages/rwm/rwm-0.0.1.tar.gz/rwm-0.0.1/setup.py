from setuptools import setup

setup(
    name='rwm',
    version='0.0.1',
    packages=['rwm'],
    url='https://github.com/geraldo-labs/rwm',
    license='MIT',
    author='Geraldo Andrade',
    author_email='geraldo@geraldoandrade.com',
    description='RWM stands for Repository Webhook Manager.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
