# coding: utf-8
# stdlib
import csv
import sys
import webbrowser
# dependencies
from rtmapi import Rtm
# custom
from astrid import AstridTask
from db import Db
from rtm import RtmList

__author__ = "Claus Conrad <webmaster@clausconrad.com>"

RTM_API_KEY = "API_KEY_GOES_HERE"
RTM_SHARED_SECRET = "SHARED_SECRET_GOES_HERE"

if __name__=="__main__":
    # Path to tasks.csv extracted from Astrid backup zip should be given as first command-line argument!
    tasks_csv_filename = sys.argv[1]
    with open(tasks_csv_filename, 'rb') as tasks_csv_file:
        # Open tasks.csv from Astrid
        tasks_reader = csv.DictReader(tasks_csv_file, strict = True)
        tasks = [AstridTask(task_data) for task_data in tasks_reader]
    # Connect to local SQLite3 db
    db = Db()
    # Check RTM token || Authenticate and save token
    rtm = Rtm(RTM_API_KEY, RTM_SHARED_SECRET, "write", db.get_setting("token"))
    # Authentication block, see http://www.rememberthemilk.com/services/api/authentication.rtm
    # check for valid token
    if not rtm.token_valid():
        # use desktop-type authentication
        url, frob = rtm.authenticate_desktop()
        # open web browser, wait until user authorized application
        webbrowser.open(url)
        raw_input("Press Enter after authorizing the application in your web browser: ")
        # get the token for the frob
        rtm.retrieve_token(frob)
        db.set_setting("token", rtm.token)
    # Cache RTM lists
    result = rtm.rtm.lists.getList()
    temp_lists = [RtmList(list.attrib) for list in result._RtmObject__element._children[0]._children]
    rtm_lists = {rtm_list.name: rtm_list for rtm_list in temp_lists if not rtm_list.smart and not rtm_list.deleted and not rtm_list.archived}
    # Get mappings from Astrid lists to RTM lists (if any)
    list_mappings = db.get_list_mappings()
    # all updates require timeline (which =~ savepoint to which one can rollback)
    result = rtm.rtm.timelines.create()
    timeline = result.timeline.value
    # For each task, upload and set Migrated
    for task in tasks:
        # Map first Astrid list to RTM list
        if task.lists and task.lists[0] in list_mappings:
            task.rtm_list = rtm_lists[list_mappings[task.lists[0]]]
        if not task.rtm_list and task.lists and task.lists[0] in rtm_lists:
            task.rtm_list = rtm_lists[task.lists[0]]
        if not db.get_task_migrated(task):
            if task.rtm_list:
                result = rtm.rtm.tasks.add(timeline = timeline, list_id = str(task.rtm_list.id), name = task.title, parse = "0")
            else:
                result = rtm.rtm.tasks.add(timeline = timeline, name = task.title, parse = "0")
            list_id = result.list.id
            taskseries_id = result.list.taskseries.id
            task_id = result.list.taskseries.task.id
            if task.completed_on and not task.repeat:
                rtm.rtm.tasks.complete(timeline = timeline, list_id = list_id, taskseries_id = taskseries_id, task_id = task_id)
            if task.due_date:
                rtm.rtm.tasks.setDueDate(timeline = timeline, list_id = list_id, taskseries_id = taskseries_id, task_id = task_id, due = task.due_date.isoformat(), parse = "0")
            if task.importance != 4:
                rtm.rtm.tasks.setPriority(timeline = timeline, list_id = list_id, taskseries_id = taskseries_id, task_id = task_id, priority = str(task.importance))
            db.set_task_migrated(task)
            try:
                print "Created task %s" % (task.title.encode("utf-8", "ignore"), )
            except:
                print "Created task %s" % (task.title.encode("Windows-1252", "ignore"), )