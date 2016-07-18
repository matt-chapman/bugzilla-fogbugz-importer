# Bugzilla -> FogBugz Importer

##What is this?
This Python script was born out of a need to migrate data I already had in a long-running Bugzilla instance, to a new hosted FogBugz solution.
It is fairly barebones, but it does work quite well.

##How do I use it?
This script has the following dependencies:

**Python 2.7** - **The fogbugz.py library is written for 2.7, so this script has been also.**

*fogbugz.py* - FogBugz python library for their (awesome) XML API.

*tdqm.py* - For the pretty progress bar

Use the dictionary objects in *Mappings.py* to map users, projects, states or priorities between Bugzilla and FogBugz, if they are not identical.

Fill your API details, along with the path to your XML export from Bugzilla in to the *FbSettings.py* file.

Run *BugParser.py*.
