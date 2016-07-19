# Bugzilla -> FogBugz Importer

##What is this?
This Python script was born out of a need to migrate data I already had in a long-running Bugzilla instance, to a new hosted FogBugz solution. It is fairly barebones, but it does work quite well.

This is the first thing I have ever written in Python. It isn't pretty, I know. If you want to make changes or improvements, please submit a pull request, I would be glad to have some criticism!

##How do I use it?

This script has been written for **Python 2.7**. It has not been tested with Python 3.5.

###Dependencies

1. *fogbugz.py* - FogBugz python library for their (awesome) XML API.

2. *tdqm.py* - For the pretty progress bar

###Fogbugz & Bugzilla Preparation

Because Bugzilla and Fogbugz both use different workflows, there is some preparation that needs to be done.

1. Create users in Fogbugz, equivalent to those that exist in Bugzilla.
2. Create projects in Fogbugz, equivalent to those that exist in Bugzilla.
3. Create case states in Fogbuz, equivalent to those that exist in Bugzilla.
4. Export your Bugzilla bug list, by doing a search for the bugs that you want to export, and then pressing the 'XML' button on the results page.

You can use the dictionary objects in *Mappings.py* to map users, projects, states or priorities between Bugzilla and FogBugz, if they are not identical. For example, when using the example *Mappings.py* provided, any bugs assigned to 'OldUser' in Bugzilla will be assigned to 'NewUser' In Fogbugz.

Case states are also mapped in *Mappings.py*. Elements in the 'statuses' dictionary are intended for mapping the state of currently open cases. 'resolutions' are intended to map fixed bugs in Bugzilla onto the equivalent 'fixed (x)' states in Fogbugz. Unlike the 'users' and 'projects' dictionaries, these use the integer indices of the Fogbugz case states, rather than string identifiers.

The script will add a comment containing a bug's Bugzilla comments and previous 'Bugzilla ID', to each submitted case.

Cases marked as resolved in Bugzilla will be marked resolved in Fogbugz, and then closed.

Fill your API details, along with the path to your XML export from Bugzilla in to the *FbSettings.py* file.

Run *BugParser.py* to begin the import. You can do a dry parsing run by setting 'doSubmission' at the top of *BugParser.py* to 'False'. To print the contents of each bug, you can set 'printDebug' to 'True'.

##Considerations

I do not provide any warranty for this, obviously. Execute at your own risk, and do your own testing before executing this script against a production instance of Fogbugz. Running this script repeatedly *will* create duplicate bugs. You have been warned.

The script is very quick to parse the XML structure, but will take time to submit the bugs via the Fogbugz API. It took approximately 30 minutes to submit 734 bugs, when I used it.
