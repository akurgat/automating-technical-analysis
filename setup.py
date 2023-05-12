import os
from setuptools import setup
import configparser
directory = os.path.abspath(os.path.dirname(__file__))
config = configparser.ConfigParser()
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()
  
config.read(os.path.join(directory, 'cli_config.ini'))
dev_verison = config['version']['cli_automating_technical_analysis_version']

# requirements.txt
# https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py
# with open('requirements.txt') as f:
#     required = f.read().splitlines()




setup(
    name='automating-technical-analysis',
    version=dev_verison,
    description='Financial trading using Technical and Timeseries Analysis.',
    author='akurgat',
    long_description=long_description,
    # install_requires=required,
    keywords='Financial', 
    py_modules=['cli'],
    entry_points={
        'console_scripts': [
            # cli->asserter->predict()
            'trade=cli.asserter:predict',
            
    

        ],
        
    },
    
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Financial :: Data Analytics',
    ]


)


# https://martin-thoma.com/software-development-stages/
