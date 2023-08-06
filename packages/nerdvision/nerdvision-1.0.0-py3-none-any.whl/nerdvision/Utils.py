import uuid

import sys


class Utils(object):

    @staticmethod
    def is_python_3():
        return sys.version_info[0] == 3

    @staticmethod
    def generate_uid():
        return uuid.uuid4().hex
