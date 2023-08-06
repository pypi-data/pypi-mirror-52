from __future__ import print_function

import os
import requests


class HostsIntegrator(object):

    __hosts = []
    __write_path = ""

    def __init__(self, directory=""):
        if directory == "":
            directory = os.getcwd()

        self.__write_path = os.path.join(directory, "hosts.txt")

    def add_hosts(self, url):
        res = requests.get(url)
        if res.status_code != 200:
            print("Unsuccessful download : " + url)
            return

        text = res.text
        text = text.replace("\t", " ")
        text = text.replace("  ", " ")
        text = text.replace("127.0.0.1 localhost", "")
        text = text.replace("::1 localhost", "")
        text = text.replace("0.0.0.0", "127.0.0.1")

        self.__hosts += [host for host in text.splitlines() if not host.startswith("#") and host != ""]
        self.__hosts = list(set(self.__hosts))

    def get_host(self):
        return self.__hosts

    def write_hosts(self, comments=None):

        if comments is None:
            comments = []
        with open(self.__write_path, "w", encoding="utf-8") as fp:
            for comment in comments:
                if not comment.startswith("#"):
                    comment = "#" + comment
                fp.write(comment + "\n")
            fp.write("\n")
            fp.write("127.0.0.1  localhost\n")
            fp.write("::1  localhost\n\n")
            for host in self.__hosts:
                fp.write(host + "\n")
