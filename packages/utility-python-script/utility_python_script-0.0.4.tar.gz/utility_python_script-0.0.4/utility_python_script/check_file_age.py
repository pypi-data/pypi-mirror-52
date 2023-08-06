"""
# check_file_age
Gather the file age and do an evaluation based on the file age.

## app
### app_virt_backup
Get the file age of the `virt_backup` tar-files; if the file age is older than the configured
`max_age`, then a warning mail is sent out.
"""
import datetime
import json
import re
from collections import defaultdict
from os import listdir
from os.path import isfile, join

from gymail.core import send_mail
from helputils.core import format_exception


class CheckFileAge():

    def app_virt_backup(self, app_config):
        """Example filename: 20190826-231404_18_cx03.tar"""
        age_dict = defaultdict(list)
        date_today = datetime.datetime.now()
        regex = "([0-9]+)-[0-9]+_[-]?[0-9]+_(.*)\.tar"
        for path in app_config["directory"]:
            files = [_file for _file in listdir(path) if isfile(join(path, _file))]
            for _file in files:
                match = re.match(regex, _file)
                if match:
                    backup_date = datetime.datetime.strptime(match[1], "%Y%m%d")
                    age = (date_today - backup_date).days
                    age_dict[match[2]].append(age)
        return ("app_virt_backup", age_dict)

    def get_config(self):
        with open('/etc/utility-python-script/monitor-file-age.json') as config_file:
            self.conf = json.load(config_file)

    def evaluate_age(self, app_ages, app_config):
        app, age_dict = app_ages
        for host, age in age_dict.items():
            if min(age) > app_config["max_age"]:
                sbj = "(ERROR) %s %s is %s days old" % (app, host, min(age))
                msg = sbj
                send_mail(event="error", subject=sbj, message=msg)

    def main(self):
        self.get_config()
        for app, app_config in self.conf.items():
            if app in self.registered_app():
                print("(RUN APP) %s" % app)
                _app = getattr(self, app)
                try:
                    app_ages = _app(app_config)
                except Exception as e:
                    sbj = "(ERROR) %s failed" % (app)
                    msg = "Exception message: %s" % format_exception(e)
                    send_mail(event="error", subject=sbj, message=msg)
            if app_config["evaluate_method"] in self.registered_evaluation():
                print("(RUN EVAL) %s" % app_config["evaluate_method"])
                evaluate_method = getattr(
                    self,
                    self.registered_evaluation().get(app_config["evaluate_method"])
                )
                try:
                    evaluate_method(app_ages, app_config)
                except Exception as e:
                    sbj = "(ERROR) %s failed" % app_config["evaluate_method"]
                    msg = "Exception message: %s" % format_exception(e)
                    send_mail(event="error", subject=sbj, message=msg)

    def registered_app(self):
        registered_app = [
            "app_virt_backup",
        ]
        return registered_app

    def registered_evaluation(self):
        registered_eval = {
            "default": "evaluate_age",
            "evaluate_age": "evaluate_age",
        }
        return registered_eval


def main():
    CheckFileAge().main()
