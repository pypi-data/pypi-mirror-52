# GSselect
This repository provides a python example of using the 
Gemini Observatory API for triggering template observations
that are On Hold. Details of the ToO activation process are
given [here](https://www.gemini.edu/sciops/observing-gemini/phase-ii-and-s/w-tools/too-activation).
The document [urltoo_readme.txt](https://github.com/bryanmiller/gsselect/blob/master/urltoo_readme.txt)
give more details about the API.

The example triggering script is urltrigger.py but most of the 
code is for selecting a guide star. The triggering API does
not support the new automated guide star selection features 
in the Observing Tool. The script gsselect.py mimics these 
features and should find an appropriate guide star if one is 
available in the UCAC4 catalog. It can also display the guide
star candidates and the wavefront sensor field of view on a 
DDS image of the field.

Gsselect also has a 'find' position angle (PA) feature
that we never implemented in the OT. This will pick the best guide
star available and set the PA so that it is reachable. This is 
useful with the GMOS and F2 OIWFS guide probes if the PA
is unimportant.

## Installation
The scripts require a standard python distribution that includes 
numpy (at least 1.15.4), matplotlib, astropy, requests, and [aplpy](http://aplpy.github.io). 

Then install the scripts by downloading and unpacking the zip
file or use git, e.g.

git clone https://github.com/bryanmiller/gsselect.git

The gsselect guide star selection routines can also be installed as a pip package with

pip install gsselect

## Authentication
Authentication for the trigger requires a 'user key' for the 
Observing Tool that is associated with an email address that
is included in the active program. See [this page](https://www.gemini.edu/sciops/observing-gemini/phase-ii-and-s/w-tools/observing-tool/science-program-editor/keychain-manage)
for more information on user keys and how to obtain one.

