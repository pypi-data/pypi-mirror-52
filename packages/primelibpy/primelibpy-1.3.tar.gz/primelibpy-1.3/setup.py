from distutils.core import setup
'''
setup(
  name = 'primelibpy',         # How you named your package folder (MyLib)
  packages = ['primelibpy'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library can be used in cryptoanalysis and some compatitive exams. It cover many different types of prime number and three factorization algorithems. Using this library any one generate random spacific prime number. To use this library you mast have python 3.x',   # Give a short description about your library
  author = 'MIT',                   # Type in your name
  author_email = 'mitbpatel0128@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/mit1280/primelibpy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/mit1280/primelibpy/archive/v1.3.tar.gz',    # I explain this later on
  keywords = ['Mersenne Prime', 'Twin Prime', 'Wilson Prime','Sophie Germain prime',' Wieferich prime','Factorial Prime','Circular Prime','Cousin Prime'
  ,'Balanced Prime','Palindromic Prime','Reversible Prime','Pythagorean Prime','Permutable Prime','Wagstaff Prime','Fermat Pseudoprime','Semi Prime','Lucas Prime'
  ,'Primorial prime','Gaussian Prime','Good Prime','Truncatable Prime','Left Truncatable Prime','Right Truncatable Prime','Home Prime','python','prime','factor','pollard','rho','fermat'],   # Keywords that define your package best
  install_requires=[           
          'gmpy2'
      ],
  classifiers=[
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
'''

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="primelibpy",
    version="1.3",
    author="MIT",
    author_email="mitbpatel0128@gmail.com",
    description = 'This library can be used in cryptoanalysis and some compatitive exams. It cover many different types of prime number and three factorization algorithems. Using this library any one generate random spacific prime number. To use this library you mast have python 3.x',   # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/mit1280/primelibpy",
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
    python_requires='>=3.0',
)
