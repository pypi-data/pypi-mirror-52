2019-09-09
Change data to float as it is filtered.  This is to overcome a bug in pyqtgraph
which crashes if the image is flat (all zeros or same number).  This is common 
in this application if filters are correct.  This bug is in current 0.10 chain 
of pyqtgraph.  There is a fix in 0.11 but this is not yet released, so this is 
not on conda or pypi site.  Make a change in this code to make installs easier
separate connecting/unconnecting signals into methods that can be used when it
is necessary.
version number to 0.7

2019-07-05
Modified minixes.xml to create environment as minixes2 to match the 
environment in the bat files that will go into the scripts directory.
Added setup_rixs.bat to the Scripts directory.
Changed version number to 0.6.7 for these changes.



2019-05-23
The initial code in this repository was written by Brian Mattern, formerly
of the University of Washington.  This code was written to process X-Ray 
Emission Spectroscopy data collected at the Advanced Photon Source at 
Sector 20.  The initial version of this code was written with a Graphical
User Interface (GUI) written utilizing wxPython and was written to work
with images collected using a Pilatus 100k detector.
Work is underway to upgrade the instrumentation for this beamline and move
to sector 25.  The upgrade of this beamline is based around updating the 
detector to a Pilatus 2M detector (1679x1475 pixels vs 195x487 for the
Pilatus 100k) and a new set of analyzer crystals array (now laid out as a 
2D array of crystals).
To accomodate the larger detector and the new analyzer array, some rework 
was necessary.  This document will attemp to capture knowledge of the 
changes made to the code.

The original code was commited into the git repository at:

https://git.aps.anl.gov/hammonds/minixes2

The starting version is tagged there as Original_Code.  This was committed 
there about March 20, 2019.  

Initial work attempted to use as much of the code as possible.  Early on 
it was decided to migrate from wxPython GUI to PyQt GUI.  It was proving 
difficult to adapt especially the Image code there to the larger detector.
Could not get the images to properly resize.  The code is laid out in the 
repository with a Python package structure starting with the directory 
minixs.  The subpackage at minixs.gui contained files relevant to the 
wxPython GUI.  An additional subpackage minixs.gui.qtcalibrator was added 
for the main PyQt program and the qthelper was added to contain a few more.
The code at the root level "minixs" contain most of the code performing
manipulation of data.  The original code adhered well to the model/view 
framework so the code at this level was able to be used mostly untouched 
while changing the GUI from wxPython to PyQt.  With minor exceptions, code 
in minixs.gui.calibrator are abandoned (they relate to wxPython) along with 
those in the level minixs.gui.  When the code at minixs.gui was migrated to 
PyQt a parallel code was placed in minixs.gui.qthelpers.  

Below is discussion of modifications to the code processing code at the 
"minixs" level of the package.
Some other changes were made to start a migration from Python 2 to Python
3.

calibrate.py
Python logging was adopted in place of adding print statements.  Mostly 
debug level comments were added which should not be seen unless a proper 
config file is installed.
A mechanism to present progress to the user was added.  This amounted to 
adding an extra parameter to find_combined_maxima, calbrate, and 
calibrator.calibrate which defines a method to run in order to provide 
progress information in the GUI.
The python zip module's izip method was used in the original code to 
combine arrays & such during iteration steps.  In Python 3 this will be 
done by Python 3's built in zip function.  Import and use of this was changed
to make it possible to run Python 3 or Python 3 in this situation.
It seemed in the find Maxima method the use of 'direction' was not proper
if changing from Down to Up or Right.  This reference would have given 
lists a 2 or 3 for the index when it only has 2 possibilites.  Switch to 
rolldir which defined to indicate VERTICAL or HORIZONTAL.

constants.py
Switched Up and Down.  The PyQt Gui has pixel [0,0]  in the lower left 
as opposed to the wxPython which was upper left.  Up and Down have changed 
relative direction.  This should be the only change needed here.  The
calcs are the same as before, just reverse the naming involved.

emission.py
Add some pythong logging to trace some of the code.
izip from itertools package is used to iterate over energies and exposures 
together.  For Python 3 this will just use the Python zip built in
function.  Added code to make running Python 2 or 3 possible.
Provide full path for module imports.  All of this code now is in a 
python package structure, full path to the modules is needed.

exposure.py
izip from itertools package is used to iterate over energies and exposures 
together.  For Python 3 this will just use the Python zip built in
function.  Added code to make running Python 2 or 3 possible.
Add some python logging to help with debugging.
Enclose prints with parens for Python 3 compatibility.

filetype.py
Fix a problem converting string to lower case.

filter.py
add Python logging for debug purposes.
Moved Filter titles to local variable.

misc.py
exposure.py
izip from itertools package is used to iterate over energies and exposures 
together.  For Python 3 this will just use the Python zip built in
function.  Added code to make running Python 2 or 3 possible.
Add some python logging to help with debugging.
Some modifications to find_xtal_boundaries to make it work with all 
detectors.  This method is still not totally reliable in the general case
the option is currently (5/23/2019) disabled in the GUI in favor of 
manually finding the crystals and drawing ROI.

rixs.py
izip from itertools package is used to iterate over energies and exposures 
together.  For Python 3 this will just use the Python zip built in
function.  Added code to make running Python 2 or 3 possible.
Add some python logging to help with debugging.
Add complete package path in imports.

scanfile.py
In load remove seek command.  Doesnt seem relevant and relative seek does
not work.
change use of xrange to range for Python 3 compatibility

spectrometer.py
izip from itertools package is used to iterate over energies and exposures 
together.  For Python 3 this will just use the Python zip built in
function.  Added code to make running Python 2 or 3 possible.
Use complete package path in imports.
Add logging for debugging purpose
put parens around print for Python 3 compatibility


