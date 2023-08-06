Python Prime Library
====================

This official documentation of python prime library.

-  Generate Specific type of Prime numbers between given range
-  Generate Random Prime number
-  Factorization of given number

Installation!
=============

1. If you don’t have pip then follow below procedure else go to step 2.

-  For window Users

   -  Download `get-pip <https://bootstrap.pypa.io/get-pip.py>`__ to a
      folder on your computer.
   -  Put that file on Desktop
   -  Open cmd and run the following commands:
      ``sh   $ cd Desktop   $ python get-pip.py``

-  For Mac Users

   -  Install python 
       ``sh   $ brew install python``
   -  Run the following command: 
       ``sh   $ python get-pip.py``

-  For Linux Users

   -  Run the following commands for python(version > 2.0):
      ``sh   $ sudo apt-get install python-pip   
      $ sudo pacman -S python2-pip   
      $ sudo yum upgrade python-setuptools   
      $ sudo yum install python-pip python-wheel   
      $ sudo dnf upgrade python-setuptools   
      $ sudo dnf install python-pip python-wheel   
      $ sudo zypper install python-pip python-setupt ools python-wheel``
   -  Run the following commands for python(version > 3.0):
      ``sh   $ sudo apt-get install python3-pip   
      $ sudo pacman -S python-pip   
      $ sudo yum install python3 python3-wheel   
      $ sudo dnf install python3 python3-wheel   
      $ sudo zypper install python3-pip python3-setu ptools python3-wheel``

-  For Raspberry Users

   -  Run the following commands for python(version > 2.0):
      ``sh   $ sudo apt-get install python-pip``
   -  Run the following commands for python(version > 2.0):
      ``sh   $ sudo apt-get install python3-pip``

2. Import gmpy2 file

   -  This package is require to install primelibpy library
   -  Run following command 
       ``sh   $ pip install gmpy2==2.1.0a2``

3. Now, install prime python library using below command.

   -  Run following command 
       ``sh   $ pip install primelibpy``

4. How to use Library

   -  Inside of your python IDE
      ``sh   from primelibpy import Prime as p``
   -  Now, using ``p`` all function can be used in code
      e.g.
      ``sh   balancedNumberList = p.getBalancedPrime(2,100,2)``

Functions Description
=====================

-  .. rubric:: Prime Functions
      :name: prime-functions

   In all the prime numbers Start_Limit and End_Limit are the range of
   prime number user wants to print inclusively. #### Balanced Prime
   Syntex:
   ``sh getBalancedPrime(startLimit,endLimit,balancedMode)``
   Return Type: ``list`` 
   Description: Balanced_Mode is how number which
   decide balanced limit for prime.

Circular Prime
^^^^^^^^^^^^^^

   Syntex: ``getCircularPrime(startLimit,endLimit)`` 
   Return Type: ``list``

Cousin Prime
^^^^^^^^^^^^

   Syntex: ``getCousinPrime(startLimit,endLimit)`` 
   Return Type: ``list``
   Description: Cousin prime are in pair so return list is have list
   inside it e.g.[ [1,2], [2,3] ]

Double Mersenne Prime
^^^^^^^^^^^^^^^^^^^^^

   Syntex: ``getDoubleMersennePrime(startLimit,endLimit)`` 
   Return Type:``list``

Factorial Prime
^^^^^^^^^^^^^^^

   Syntex: ``getFactorialPrime(startLimit,endLimit)`` 
   Return Type:``list``

Good Prime
^^^^^^^^^^

   Syntex: ``getGoodPrime(startLimit,endLimit)`` 
   Return Type: ``list``

Mersenne Prime
^^^^^^^^^^^^^^

   Syntex: ``getMersennePrime(startLimit,endLimit)`` 
   Return Type:``list``

Palindromic Prime
^^^^^^^^^^^^^^^^^

   Syntex: ``getPalindromicPrime(startLimit,endLimit)`` 
   Return Type:``list``

Permutable Prime
^^^^^^^^^^^^^^^^

   Syntex: ``getPermutablePrime(startLimit,endLimit)`` 
   Return Type:``list``

Primorial Prime
^^^^^^^^^^^^^^^

   Syntex: ``getPrimorialPrime(startLimit,endLimit)`` 
   Return Type:``list``

Fermat Pseudo Prime
^^^^^^^^^^^^^^^^^^^

   Syntex: ``getFermatPseudoPrime(baseNumber,noPsedoPrime)`` 
   Return Type: ``list`` 
   Description: Base_number is halp to generate composite
   number ,and second argument is Total number of Pseudo primes

Pythagorean Prime
^^^^^^^^^^^^^^^^^

   Syntex: ``getPythagoreanPrime(startLimit,endLimit)`` 
   Return Type:``list``

Reversible Prime
^^^^^^^^^^^^^^^^

   Syntex: ``getReversiblePrime(startLimit,endLimit)`` 
   Return Type:``list``

Semi Prime
^^^^^^^^^^

   Syntex: ``getSemiPrime(startLimit,endLimit)`` 
   Return Type: ``list``

Sophie Germain Prime
^^^^^^^^^^^^^^^^^^^^

   Syntex: ``getSophieGermainPrime(startLimit,endLimit)`` 
   Return Type:``list``

Twin Prime
^^^^^^^^^^

   Syntex: ``getTwinPrime(startLimit,endLimit)`` 
   Return Type: ``list``
   Description: Twin prime are in pair so return list is have list
   inside it e.g.[ [1,2], [2,3] ]

Wagstaff Prime
^^^^^^^^^^^^^^

   Syntex: ``getWagstaffPrime(startLimit,endLimit)`` 
   Return Type:``list``

Wieferich Prime
^^^^^^^^^^^^^^^

   Syntex: ``getWieferichPrime(startLimit,endLimit)`` 
   Return Type:``list``

Wilson Prime
^^^^^^^^^^^^

   Syntex:\ ``getWilsonPrime(startLimit,endLimit)`` 
   Return Type:``list``

Left Truncatable Prime
^^^^^^^^^^^^^^^^^^^^^^

   Syntex: ``getLeftTruncatablePrime(startLimit,endLimit)`` 
   Return Type:``list``

Right Truncatable Prime
^^^^^^^^^^^^^^^^^^^^^^^

   Syntex: ``getRightTruncatablePrime(startLimit,endLimit)`` 
   Return Type: ``list``

Truncatable Prime
^^^^^^^^^^^^^^^^^

   Syntex: ``getTruncatablePrime(startLimit,endLimit)`` 
   Return Type:``list``

Gaussian Prime
^^^^^^^^^^^^^^

   Syntex: ``getGaussianPrime(startLimit,endLimit)`` 
   Return Type:``None``



-  .. rubric:: Factorization
      :name: factorization
      
      

Traditional Way for Factorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Syntex: ``getFactorTraditional(compositeNumber)`` 
   Return Type:``list``

Fermat Theorem for Factorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Syntex: ``getFactorFermatTheorem(compositeNumber)`` 
   Return Type:``tuple`` 
   Note: This is only for composite number who have only two
   prime factors except number itself e.g. 33 have two prime factors 3
   and 11.

Pollard Rho for Factorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Syntex: ``getFactorPollardRho(compositeNumber)`` 
   Return Type:``integer`` 
   Note: This will return any one factor of given number
   because this algorithem works on random numbers.

License
-------

MIT

**Free Software, Hell Yeah!**
