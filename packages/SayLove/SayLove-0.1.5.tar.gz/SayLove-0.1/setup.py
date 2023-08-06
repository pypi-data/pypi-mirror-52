from distutils.core import setup
setup(
  name = 'SayLove',         # How you named your package folder (MyLib)
  packages = ['SayLove'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'My first python package to show love quotes',   # Give a short description about your library
  author = 'Cara Wang',                   # Type in your name
  author_email = 'bookview@126.com',      # Type in your E-Mail
  url = 'https://github.com/testcara/SayLove',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/testcara/SayLove/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['First Python Package', 'Love Quotes'],   # Keywords that define your package best
  include_package_data=True,
  #package_dir={'SayLove': 'src/mypkg'},
  package_data={'SayLove': ['*']},
  install_requires=[            # I get to this in a second
  #        'os',
  #        'beautifulsoup4',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Utilities', # For more topics, please refer to https://pypi.org/pypi?%3Aaction=list_classifiers
    'License :: OSI Approved :: MIT License',   # Again, pick a license    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
