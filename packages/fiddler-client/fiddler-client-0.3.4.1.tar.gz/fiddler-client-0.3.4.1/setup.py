import setuptools

with open('Readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='fiddler-client',
    version='0.3.4.1',
    author='Fiddler Labs',
    description='Python client for Fiddler Service',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://fiddler.ai',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>3.6.3',
)
