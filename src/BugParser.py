from xml.etree.ElementTree import parse, XMLParser

import fogbugz
import tqdm

import FbSettings
from Bug import Bug, Comment, BugList


def run_import():

    parser = XMLParser()

    # deal correctly with bad elements
    parser.parser.UseForeignDTD(True)

    # parse the structure
    tree = parse(FbSettings.PATH)
    root = tree.getroot()
    bug_list = BugList()

    # get all of the bugs
    for current_bug in root.iter('bug'):
        handle_bug(bug_list, current_bug, FbSettings.PRINT_DEBUG_INFO)

    # only do bug submission to the DB if it is enabled
    if FbSettings.DO_SUBMISSION:
        submit_bugs_to_db(bug_list)

    # print out some general info on completion
    print_on_completion(bug_list)


def print_on_completion(bug_list):
    print('Processed ' + str(len(bug_list.bugs)) + ' bugs...\n')
    print('Covering ' + str(len(bug_list.projects)) + ' projects:')
    for project in bug_list.projects:
        print(project)
    print('\n')
    print('Assigned to ' + str(len(bug_list.users)) + ' users:')
    for user in bug_list.users:
        print(user)


def submit_bugs_to_db(bug_list):
    iterator = 0
    # log into the API
    fb = fogbugz.FogBugz(FbSettings.URL, FbSettings.TOKEN)
    # iterate through the bugs, via tqdm for progress reporting
    for bug in tqdm.tqdm(bug_list.bugs):

        iterator += 1
        comments = concat_comments(bug)

        # submit the bug
        try:
            response = fb.new(
                sProject=bug.project,
                sTitle=bug.name,
                sEvent='Imported from Bugzilla. Original Bug ID: ' +
                       bug.id + '\n\nOriginal comments: \n\n'
                                '====================\n\n' + comments,
                sPersonAssignedTo=bug.assignee,
                ixStatus=bug.fogStatus,
                ixPriority=bug.priority
            )
        except fogbugz.FogBugzAPIError:
            print(
                """An API error has occurred, submitting bug with
                 bugzilla ID """ + bug.id + '.')
            break  # break on API errors

        # if the current bug is resolved, attempt to resolve and close the
        # last submitted bug
        if bug.status == 'RESOLVED':
            try:
                resolve_bug(bug, fb, response)
            except fogbugz.FogBugzAPIError:
                print(
                    """An API error has occurred, resolving/closing
                     bug with bugzilla ID """ + bug.id + '.')
                break  # break on API errors


def concat_comments(bug):
    comments = ''
    # concat all the comments together
    if len(bug.comments) > 0:
        for comment in bug.comments:
            comments += comment.who + ' said on ' + comment.when + \
                        ':\n----------\n' + comment.text + '\n\n'
    else:
        comments = 'No comments.'

    return comments


def resolve_bug(bug, fb, response):
    fb.resolve(ixBug=response.case[
        'ixbug'], ixStatus=bug.fogStatus)
    fb.close(ixBug=response.case['ixbug'])


def handle_bug(bug_list, current_bug, print_debug):
    bug_object = add_metadata(current_bug)
    # deal with all of the comments
    for comment in current_bug.iter('long_desc'):
        add_comment(bug_object, comment)

    # now we adjust the metadata to match accounts in FogBugz...
    bug_object.fix_bug()
    # print the resulting bug, if we want to
    if print_debug:
        bug_object.print_details()

    # add unique objects to their sets
    bug_list.bugs.add(bug_object)
    bug_list.projects.add(bug_object.project)
    bug_list.users.add(bug_object.assignee)


def add_comment(bug_object, comment):
    # get comment info
    comment_object = Comment()
    comment_object.who = comment.find('who').attrib.get('name')
    comment_object.text = comment.find('thetext').text
    comment_object.when = comment.find('bug_when').text
    # if no comments exist, make some placeholder text
    if comment_object.text is None:
        comment_object.text = """No comment body. Check bugzilla
                 for attachments"""

    # append comment to current bug's comment list
    bug_object.comments.append(comment_object)


def add_metadata(current_bug):
    # deal with all the bug metadata
    bug_object = Bug()
    bug_object.id = current_bug.find('bug_id').text
    bug_object.name = current_bug.find('short_desc').text
    bug_object.project = current_bug.find('product').text
    bug_object.component = current_bug.find('component').text
    bug_object.status = current_bug.find('bug_status').text
    bug_object.resolution = current_bug.find('resolution').text
    bug_object.priority = current_bug.find('priority').text
    bug_object.severity = current_bug.find('bug_severity').text
    bug_object.assignee = current_bug.find('assigned_to').get('name')
    return bug_object


if __name__ == '__main__':
    run_import()
