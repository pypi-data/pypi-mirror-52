## 1.2.1 (2019-09-09)

### New

* Added LANL benchmark model. [Jason Liu]

### Changes

* Added bucket for uncountable quantities (as opposed of using store), and added muxtree example. [Jason Liu]


## 1.2.0 (2019-08-14)

### New

* Finished parallel simulation tutorial. [Jason Liu]

* Changed simulator's run() to run up to but not including the given time; updated parallel simulation tutorial. [Jason Liu]

* Changed argparse to happen at import time; added simulator.sync() function; fixed phold.py in advanced example. [Jason Liu]

* Added ability for sync to have multiple runs and enabled runtime performance reporting. [Jason Liu]

* Added parallel simulation support, including SPMD (using MPI), SMP (using processes), and both. [Jason Liu]

* Preliminary performance tuning; disabled expensive debug logging; added context manager for resource. [Jason Liu]

### Changes

* Some UI updates and added parallel simulation tutorial. [Jason Liu]

## 1.1.5 (2019-07-26)

### New

* Added logging support and runtime performance metrics. [Jason Liu]

* Added jupyter notebooks for queuing models. [Jason Liu]

* Tagged 1.1.4 and release. [Jason Liu]


## 1.1.4 (2019-07-17)

### New

* Added support for dynamic process priorities. [Jason Liu]

* Added data collector support; tagged 1.1.3. [Jason Liu]

### Changes

* Changed RunStats name to DataSeries, and QDIS.RANDOM to QDIS.SIRO. [Jason Liu]

* Removed dependence on runstats. [Jason Liu]


# Changelog


## 1.1.3 (2019-07-15)

### New

* Updated data collectors for resources and facilities. [Jason Liu]

* Tag and release version 1.1.2. [Jason Liu]

* Added mechanisms for consistent, independent random number generators. [Jason Liu]

### Changes

* Restructured tutorial document.


## 1.1.2 (2019-07-10)

### New

* Added documentation for mailbox and examples. [Jason Liu]

### Changes

* Added section on using store with examples. [Jason Liu]


## 1.1.1 (2019-07-09)

### New

* Sphinx generated documents for simulus api. [Jason Liu]

### Changes

* Moved to github, fixed pipenv requirements, changed cancel() to also kill process, and made trappable a public interface with retval. 

* Updated README.md from readme.ipynb; updated tutorial. [Jason Liu]

### Other

* Set theme jekyll-theme-cayman. [liuxfiu]

* Tagged and published version 1.1.0. [Jason Liu]


## 1.1.0 (2019-07-07)

### New

* Added sections to explain the use of resource and store in tutorial; also added readme jupyter notebook.

* Added store facility and some examples, including most simpy examples. [Jason Liu]

* Added a couple simpy examples (carwash, moviegoers). [Jason Liu]

* Changed sched() and process() to allow arbitrary functions; examples and documents have been updated accordingly. [Jason Liu]

* Added regression pytest and tox support. [Jason Liu]

* Changed the use of super() in init methods. 

* Changed tomjerry.py; gauss distribution may return negative time. [Jason Liu]

## 1.0.5 (2019-07-04)

### New

* New trappables and conditional waits (1.0.5). 

* Added support for changelogs generated from git logs. 

* Changed resource reserve to acquire. [Jason Liu]

* Redesigned trappables; the processes, events, semaphores, traps, and resources now work with a more intuitive interface design. [Jason Liu]

* Added initial implementation of resource and qstats. [Jason Liu]


## 1.0.4 (2019-07-04)

### New

* Finished trappables and timed waits implementation and accompanying documents (1.0.4). [Jason Liu]

* Updated documents for using trappables and timed wait; and a bug fix. [Jason Liu]

* Added support for conditional wait (wait on multiple trappables and timed wait). [Jason Liu]


## 1.0.1 (2019-07-04)

### New

* Pip ready; simulus has been published on pypi (1.0.1, 1.0.2, 1.0.3). [Jason Liu]


## 0.0.3 (2019-07-04)

### New

* Adding trapping mechanisms for inter-process communication. [Jason Liu]


## 0.0.2 (2019-07-04)

### New

* Added some examples using processes for user document. [Jason Liu]

* Added useful functions for direct event scheduling (including resched, cancel, peek, step, and show_calendar). [Jason Liu]

* Added phold example (to test processes). [Jason Liu]

### Changes

* Restructured examples directory (0.0.2). [Jason Liu]

### Fix

* Fixed process scheduling issue. [Jason Liu]


## 0.0.1 (2019-07-04)

### New

* First implementation of simulus, with support of events, processes, semaphores, and simulators; and also the jupyter notebook establishing the simple use cases. [Jason Liu]

* This project got started in the evening on June 14, 2019 with a simple idea of creating an easy-to-use python simulator to replace our somewhat dilapitated Simian simulator and also outdoing the esoteric SimPy simulator. [Jason Liu]

### Changes

* Updated the jupyter notebooks. [Jason Liu]

* Updated README.md (mindless update). [Jason Liu]

* Updated README.md. [Jason Liu]


