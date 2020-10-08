#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import os
import yaml
import re

COLOR_METHOD = '#7fb800'
COLOR_PARAM = '#00a6ed'
COLOR_INSTANCE_VAR = '#f8805a'
COLOR_NOTE = '#8E8E8E'
COLOR_WARNING = '#ED2F2F'

QUERY = re.compile(r'([cC]arla(\.[a-zA-Z0-9_]+)+)')


def create_hyperlinks(text):
    return re.sub(QUERY, r'[\1](#\1)', text)

def create_getter_setter_hyperlinks(text):
    return re.sub(QUERY, r'[\1](#\1)', text)

def join(elem, separator=''):
    return separator.join(elem)


class MarkdownFile:
    def __init__(self):
        self._data = ""
        self._list_depth = 0
        self.endl = '  \n'
    
    def data(self):
        return self._data

    def list_depth(self):
        if self._data.strip()[-1:] != '\n' or self._list_depth == 0:
            return ''
        return join(['    ' * self._list_depth])

    def textn(self, buf):
        self._data = join([self._data, self.list_depth(), buf, self.endl])



class Documentation:
    """Main documentation class"""

    def __init__(self, path):
        self._snipets_path = os.path.join(os.path.dirname(path), 'snipets')
        self._files = [f for f in os.listdir(self._snipets_path) if f.endswith('.py')]
        self._snipets = list()
        for snipet_file in self._files:
            current_snipet_path = os.path.join(self._snipets_path,snipet_file)
            #print("This is the new snipet path: "+current_snipet_path)
            self._snipets.append(current_snipet_path)

    def gen_body(self):
        """Generates the documentation body"""
        md = MarkdownFile()
        # Create header for snipets (div container and script to copy)
        md.textn(
        "[comment]: <> (=========================)\n"+
        "[comment]: <> (PYTHON API SCRIPT SNIPETS)\n"+
        "[comment]: <> (=========================)\n"+
        "<div id=\"snipets-container\" onmouseover='this.style[\"overflowX\"]=\"scroll\";'  onmouseout='this.style[\"overflowX\"]=\"visible\";' style=\"position: fixed; margin-left: 0px; overflow-y: auto; padding-left: 5px; border-left: 1px solid #767677; height: 95%; top: 70px; left: 1100px;\"></div>\n"+
        "<script>\n"+
        "function CopyToClipboard(containerid) {\n"+
        "if (document.selection) {\n"+
        "var range = document.body.createTextRange();\n"+
        "range.moveToElementText(document.getElementById(containerid));\n"+
        "range.select().createTextRange();\n"+
        "document.execCommand(\"copy\");\n"+
        "} \n"+
        "else if (window.getSelection) {\n"+
        "var range = document.createRange();\n"+
        "range.selectNode(document.getElementById(containerid));\n"+
        "window.getSelection().addRange(range);\n"+
        "document.execCommand(\"copy\");\n"+
        "}\n"+
        "}\n</script>\n")
        # Create content for every snipet
        for snipet_path in self._snipets:
            current_snipet = open(snipet_path, 'r')
            snipet_name = os.path.basename(current_snipet.name) # Remove path
            snipet_name = os.path.splitext(snipet_name)[0] # Remove extension
            # Header for a snipet
            md.textn("<div id =\""+snipet_name+"-snipet\" style=\"display: none;\">\n"+
            "<p class=\"SnipetFont\">\n"+
            "Snipet for "+snipet_name+"\n"+
            "</p>\n"+
            "<div id=\""+snipet_name+"-code\" style=\"width: 400px; margin-left: 10px\">\n\n```py\n")
            # The snipet code
            md.textn(current_snipet.read())
            # Closing for a snipet
            md.textn("\n```\n<button id=\"button1\" class=\"CopyScript\" onclick=\"CopyToClipboard('"+snipet_name+"-code')\">Copy snipet</button>\n</div>\n")
        # Closing div
        md.textn("\n</div>\n")
        #print(md.data())
        return md.data().strip()


    def gen_markdown(self):
        """Generates the whole markdown file"""
        return join([self.gen_body()], '\n').strip()


def main():
    """Main function"""
    print("Generating PythonAPI snipets...")
    script_path = os.path.dirname(os.path.abspath(__file__)+'/snipets')
    docs = Documentation(script_path)
    snipets_md_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(script_path))),'Docs/python_api_snipets.md')
    #print("The md path: "+snipets_md_path)
    with open(snipets_md_path, 'w') as md_file:
        #print(docs.gen_markdown())
        md_file.write(docs.gen_markdown())
    print("Done snipets!")


if __name__ == "__main__":
    main()