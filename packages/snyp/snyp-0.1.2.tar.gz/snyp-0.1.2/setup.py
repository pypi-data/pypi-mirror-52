import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='snyp',
    version='0.1.2',
    author='Bujar Murati',
    author_email = 'bmurati95@gmail.com',
    description='Snyp is a command line utility that streamlines the process of creating text based documentation and programming tutorials in Markdown.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    url = 'https://github.com/BujarMurati/snyp',
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['snyp'],
    install_requires=[
        'Click',
        'configparser'
    ],
    include_package_data=True,
    entry_points='''
        [console_scripts]
        snyp=snyp:snyp
    ''',
)