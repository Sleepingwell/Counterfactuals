# Some Fiddling With Counterfactual Analysis

My counterfactual playground.



## Contents

### Folders

- ***notebooks***: Jypyter notebooks I have worked with during the project.

- ***package***: Python package I started developing to do stuff. Probably
  not of much interest as I did the bulk of the stuff in R in the DataLab.

- ***papers***: Papers I have collected (and mostly read) relating to this work.

- ***playground***: Misc stuff I fiddled with as I was going.

- ***report***: Report I am drafting as I go.



### Files

- ***aliases.sh***: Aliases for commands I use in this project.

- ***Dockerfile***: Docker build file for the environment I use for dev/test.gT

- ***PAT.Rproj***: RStudio project file.



## Building the proximity function

There is a binary module in *package/src*. One can build it with:

```
cd package/src
g++ -o ../counterfactuals/_prox.so -fopenmp -fpic -O3 --shared proximity.cpp
```

... this will of course be automated when I get around to adding a setup.py.



## Docker

The Dockerfile in the root directory builds the environment in which I run PAT.
The file *aliases.sh* contains some aliases I use for starting containers. These
are:

- ***patsrv***: Starts jupyter notebook running on port 8888.

- ***patshell***:: Starts a bash session inside a pat container. You are 'you' inside
  the container (see argument *-u*).

- ***patenvroot***: A bash session inside the container (I use this mainly for
  trying things out before updating *Dockerfile*.

- ***pattest***: Run the unit tests (this can also be done with `python -m pytest`
  from inside a container started with `patshell`).

Build the image with:

```
docker build -t pat .
```
