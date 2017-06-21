import socket
import getpass
import datetime

import sublime
import sublime_plugin


def get_modif_line_header(view, edit):
    if (view.file_name().split('/')[-1] == "Makefile"):
        comment = "##"
    else:
        comment = "**"
    return comment + " Last update " + \
        format_date(datetime.datetime.now()) + \
        ' ' + getpass.getuser()


def format_date(date_to_format):
    return date_to_format.strftime("%a %b %d %H:%M:%S %Y")


class EpitechHeaderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        header = "/*\n" + self.get_first_line_header(edit)
        header += "\n**\n** Made by " + getpass.getuser()
        header += "\n** Login   <" + \
            getpass.getuser() + "@" + socket.gethostname() + ">"
        header += "\n**\n** Started on  " + \
            format_date(datetime.datetime.now()) + \
            ' ' + getpass.getuser()
        header += "\n" + get_modif_line_header(self.view, edit)
        header += "\n*/\n\n"
        if (self.view.file_name().split('/')[-1] == "Makefile"):
            header = header.replace("/*", "##")
            header = header.replace("**", "##")
            header = header.replace("*/", "##")
        self.view.insert(edit, 0, header)

    def get_first_line_header(self, edit):
        filename = self.view.file_name().split('/')
        header = "** " + filename[-1] + " for " + filename[-1].split('.')[0]
        header += " in " + "/".join(filename[0:-1])
        return header


class EpitechHeaderReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        region = \
            self.view.find("^\W+Last update \w+ \w+ \d+ \d+:\d+:\d+ \d+ \w+.*",
                           0)
        if not region.empty():
            self.view.replace(edit, region, get_modif_line_header(self.view,
                                                                  edit))


class EpitechHeaderListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        view.run_command("epitech_header_replace")
