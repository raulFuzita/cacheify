from setuptools import setup, find_packages

setup(
    name='cacheify',
    version='0.0.1',
    url='https://github.com/rfuzita-nr/cacheify',
    author='Raul Macedo Fuzita',
    author_email='raul.macedofuzita@netreveal.ai',
    python_requires='>=3.9',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ]
)