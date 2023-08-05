## ABOUT
**UNSIO** (**U**niversal **N**body **S**napshot **I**nput **O**utput) is an API which perform input/output operations in a generic way,
and on different kind of nbody files format (nemo, Gadget binaries 1 and 2, Gadget hdf5, Ramses). By using this API,
a user could write only one analysis program which will work on all known files format supported by UNSIO.
It's not necessary anymore to know how is implemented a file format, UNSIO will do transparently and automatically
all the hard work for you ! With UNSIO, you will spend less time to develop your analysis program.
UNSIO comes with an integrated sqlite3 database which can be used to retrieve automatically all your data
among terabytes of hard disks.

## Features

UNSIO can be used from different languages (C,C++,Fortran and Python)

## Supported files format :
* [**NEMO** (read and write)](https://teuben.github.io/nemo/)
* [**GADGET 1** (read)](http://www.mpa-garching.mpg.de/gadget/)
* **GADGET 2** (read an write)
* **GADGET 3/hdf5** (read and write)
* [**RAMSES** (read)](https://bitbucket.org/rteyssie/ramses)
* **List of files** stored in a file
* Simulations stored in **SQLITE3** database


## Installing python wrapper
```console
pip install python-unsio
```
## Usage

- example : load gas and stars component of an UNS compliant snapshot
```python
import unsio.input as uns_in

# we instantiate object
myfile="snashot.000"
my_in=uns_in.CUNS_IN(myfile,"gas,stars")

# load snapshot
if my_in.nextFrame():
  # read stars positions
  status,poss=my_in.getData("stars","pos")
  # read gas positions
  status,posg=my_in.getData("gas","pos")
  # read gas densities
  status,rho=my_in.getData("gas","rho")
  # read time
  status,timex=my_in.getData("time")

```
- example : save previously loaded data in gadget3 format
```python
import unsio.output as uns_out

# we instantiate object
myoutfile="snapshot.g3"
my_out=uns_out.CUNS_OUT(myoutfile,"gadget3")

# prepare data to be saved
# set time
status=my_out.setData(timex,"time")
# set positions for stars
status=my_out.setData(poss,"stars","pos")
# set positions for gas
status=my_out.setData(posg,"gas","pos")
# set density for gas
status=my_out.setData(rho,"gas","rho")

# save on disk
my_out.save()
# close
my_out.close()
```

## License
UNSIO is open source and released under the terms of the [CeCILL2 Licence](http://www.cecill.info/licences/Licence_CeCILL_V2-en.html)

## Webpage
PLease visit : https://projets.lam.fr/projects/unsio
