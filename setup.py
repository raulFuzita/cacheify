from setuptools import setup, find_packages

setup(
    name='cacheify',
    version='0.0.1',
    url='https://github.com/raulFuzita/cacheify',
    author='Raul Macedo Fuzita',
    author_email='raul_fuzita@hotmail.com',
    python_requires='>=3.8',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)