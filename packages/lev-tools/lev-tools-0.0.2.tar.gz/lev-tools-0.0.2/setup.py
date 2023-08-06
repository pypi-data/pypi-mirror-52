import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='lev-tools',
    version='0.0.2',
    author='Levatius',
    description='Tools created by Lev',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Levatius/word-counter',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
