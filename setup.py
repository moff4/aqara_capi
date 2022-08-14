import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='aqara_capi',
    version='1.1.0',
    author='Komissarov Andrey',
    author_email='Komissar.off.andrey@gmail.com',
    description='Aqara Cloud API SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/moff4/aqara_capi',
    install_requires=[
        'requests>=2.28.1',
        'pydantic>=1.9.0',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
