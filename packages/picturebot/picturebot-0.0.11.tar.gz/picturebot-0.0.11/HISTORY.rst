=======
History
=======

0.0.1 (2019-07-29)
------------------

* First release on PyPI.
* Create workplace
* Rename files
* Added a config file
* Updated tox config files
* Updated travis config files
* Empty unit tests

0.0.2 (2019-08-01)
------------------

* Upgrade from argparse to click
* Added unit test
* Added config file location command

0.0.3 (2019-08-04)
------------------

* Added a shorthand notation to call the program from the command line

0.0.4 (2019-08-04)
------------------

* A workspace can only be created within the declared workspace directory specified within the config file
* Files can only be renamed within the baseflow directory
* Bug fix: Only changed files names are listed in the output 
* Bug fix: Only missing project flows are getting added when renaming files
* Added command to check the script version

0.0.5 (2019-08-17)
------------------

* Create a backup of the baseflow directory
* Added a backup attribute within the config file

0.0.6 (2019-08-17)
------------------

* Automatically open the config file
* Bug fix: Only create none existing flows

0.0.7 (2019-08-18)
------------------

* Display copied files progress
* Added a selection attribute within the config file
* Added an attribute within the config file
* Check whether all the pictures within a shoot are edited

0.0.8 (2019-08-21)
------------------

* Checking whether a certain shoot is finished isn't limited to the workspace folder anymore

0.0.9 (2019-09-15)
------------------

* Renames filenames with their hashed values
* Updated output of the renaming command

0.0.10 (2019-09-16)
-------------------

* Improvement: Use guard method to check whether the cwd is within the correct directory
* Open the edited folder from within the selection folder

0.0.11 (2019-09-18)
-------------------

* Hash files are sorted by creation date
* Updated: Renamed files are sorted by creation date instead of modification date