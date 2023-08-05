=======
History
=======

0.1.0 (2019-08-18)
------------------

* First release on PyPI.

0.1.1 (2019-08-19)
------------------

* Added land sea mask plugin

0.1.2 (2019-08-20)
------------------

* Added pypi classifiers

0.1.4 (2019-08-22)
------------------

* Added precipitation matching functionality

0.1.5 (2019-08-23)
------------------

* added conditional function that checks if rain rate and/or rain function exist in the output netcdf4 do not run functions to find rain rate and rain fraction

* added conditional check if the input h5 file does not exist to remove output netcdf file

0.1.6 (2019-08-23)
------------------

* testing a new way using c extension to match cloud top, base, and thickness

0.1.7 (2019-08-23)
------------------

* Added function to identify warm clouds

* Added function to match reanalysis (currently only tested with ERA-Interim) LTS to cloudsat objects

* LTS matching function currently written in pure python, but is being tested as a c-extension

0.1.8 (2019-08-26)
------------------

* added getcwd to functions imported from the os package in the cloud_type identification package

* Updated readme and began writing the usage part of the documentation

0.1.10 (2019-08-27)
-------------------

* added command line executable that matches total column water vapor (currently only using ERA-Interim) to cloudsat objects

0.1.11 (2019-09-09)
-------------------

* added command line executable that matches relative humidity below 3 km (currently only using ERA-Interim) to cloudsat objects
