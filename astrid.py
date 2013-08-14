# coding: utf-8
# stdlib
import datetime

__author__ = "Claus Conrad <webmaster@clausconrad.com>"

class AstridTask(object):
    def __init__(self, csv_row):
        self.title = csv_row["Title"].decode("utf-8")
        self.created_by = csv_row["Created By"].decode("utf-8") if csv_row["Created By"] else None
        self.assigned_to = csv_row["Assigned to"].decode("utf-8") if csv_row["Assigned to"] else None
        self.created_on = datetime.datetime.strptime(csv_row["Created On"], "%Y-%m-%d %H:%M:%S")
        try:
            self.due_date = datetime.datetime.strptime(csv_row["Due Date"], "%Y-%m-%d %H:%M:%S")
        except:
            try:
                self.due_date = datetime.datetime.strptime(csv_row["Due Date"], "%Y-%m-%d")
            except:
                self.due_date = None
        self.importance = int(csv_row["Importance"])
        self.repeat = csv_row["Repeat"].decode("utf-8") if csv_row["Repeat"] else None
        self.lists = csv_row["Lists"].decode("utf-8").split(",") if csv_row["Lists"] else None
        self.description = csv_row["Description"].decode("utf-8") if csv_row["Description"] else None
        try:
            self.completed_on = datetime.datetime.strptime(csv_row["Completed On"], "%Y-%m-%d %H:%M:%S")
        except:
            self.completed_on = None
        self.comments = csv_row["Comments"].decode("utf-8")
        self.time_estimate = csv_row["Time Estimate"].decode("utf-8") if csv_row["Time Estimate"] else None
        self.time_elapsed = csv_row["Time Elapsed"].decode("utf-8") if csv_row["Time Elapsed"] else None
        # Only included here for IDE IntelliSense
        self.rtm_list = None
