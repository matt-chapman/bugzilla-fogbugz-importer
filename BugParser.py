import xml.etree.ElementTree as ET

import fogbugz
from tqdm import tqdm

import FbSettings
from Bug import Bug, Comment, BugList

# should we submit to the DB?
doSubmission = True
printDebug = False

parser = ET.XMLParser()
# deal correctly with bad elements
parser.parser.UseForeignDTD(True)

# parse the structure
tree = ET.parse(FbSettings.PATH)
root = tree.getroot()

bugList = BugList()

# get all of the bugs
for currentbug in root.iter('bug'):

    # deal with all the bug metadata
    bugObject = Bug()
    bugObject.id = currentbug.find('bug_id').text
    bugObject.name = currentbug.find('short_desc').text
    bugObject.project = currentbug.find('product').text
    bugObject.component = currentbug.find('component').text
    bugObject.status = currentbug.find('bug_status').text
    bugObject.resolution = currentbug.find('resolution').text
    bugObject.priority = currentbug.find('priority').text
    bugObject.severity = currentbug.find('bug_severity').text
    bugObject.assignee = currentbug.find('assigned_to').get('name')

    # deal with all of the comments
    for comment in currentbug.iter('long_desc'):

        # get comment info
        commentObject = Comment()
        commentObject.who = comment.find('who').attrib.get('name')
        commentObject.text = comment.find('thetext').text
        commentObject.when = comment.find('bug_when').text

        if commentObject.text is None:
            commentObject.text = 'No comment body. Check bugzilla for attachments'

        # apppend comment to current bug's comment list
        bugObject.comments.append(commentObject)

    # now we adjust the metadata to match accounts in FogBugz...
    bugObject.fixbug()

    # print the resulting bug, if we want to
    if printDebug:
        bugObject.printdetails()

    # add unique objects to their sets
    bugList.bugs.add(bugObject)
    bugList.projects.add(bugObject.project)
    bugList.users.add(bugObject.assignee)

# only do bug submission to the DB if it is enabled
if doSubmission:
    iterator = 1

    # log into the API
    fb = fogbugz.FogBugz(FbSettings.URL, FbSettings.TOKEN)

    for bug in tqdm(bugList.bugs):

        iterator += 1
        comments = ''

        # concat all the comments together
        if len(bug.comments) > 0:
            for comment in bug.comments:
                comments += comment.who + ' said on ' + comment.when + ':\n----------\n' + comment.text + '\n\n'
        else:
            comments = 'No comments.'

        # submit the bug
        response = fb.new(
                    sProject=bug.project,
                    sTitle=bug.name,
                    sEvent='Imported from Bugzilla. Original Bug ID: ' + bug.id + '\n\nOriginal comments: \n\n'
                                                                                  '====================\n\n' + comments,
                    sPersonAssignedTo=bug.assignee,
                    ixStatus=bug.fogStatus,
                    ixPriority=bug.priority
                    )

        # if the current bug is resolved, attempt to resolve and close the last submitted bug
        if bug.status == 'RESOLVED':
            try:
                fb.resolve(ixBug=response.case['ixbug'], ixStatus=bug.fogStatus)
                fb.close(ixBug=response.case['ixbug'])
            except fogbugz.FogBugzAPIError:
                print 'API error'

# print out some general info on completion
print ('Processed ' + str(len(bugList.bugs)) + ' bugs...\n')
print ('Covering ' + str(len(bugList.projects)) + ' projects:')
for project in bugList.projects:
    print (project)
print ('\n')
print ('Assigned to ' + str(len(bugList.users)) + ' users:')
for user in bugList.users:
    print (user)
