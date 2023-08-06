from setuptools import setup, find_packages

setup(
    name= 'csv2graph2web', # Application name:
    version= '0.1.0', # Version number

    author= 'Masayuki Tanaka', # Author name
    author_email= 'mastnk@gmail.com', # Author mail

    url='https://github.com/mastnk/csv2graph2web', # Details
    description='Gnerate graphs from csv fils and upload them to the web server.', # short description
    long_description='Gnerate graphs from csv fils and upload them to the web server.', # long description
    install_requires=[ # Dependent packages (distributions)
        'paramiko', 'scp', 'pandas', 'matplotlib', 'requests'
    ],

    entry_points={'console_scripts': ['cgw_copy=csv2graph2web.cgw_copy:main']},

    include_package_data=False, # Include additional files into the package
    packages=find_packages(exclude=('tests')),

    test_suite = 'tests',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]
)
