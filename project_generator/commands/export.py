# Copyright 2014-2015 0xc0170
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import logging

from ..workspace import PgenWorkspace

help = 'Export a project record'


def run(args):
    if os.path.exists(args.file):
        workspace = PgenWorkspace(args.file, os.getcwd())
        if args.defdirectory:
            workspace.settings.update_definitions_dir(os.path.join(os.getcwd(), args.defdirectory))

        build_result = 0
        if args.project:
            export_result = workspace.export(args.project, args.tool, args.copy)

            if args.build:
                build_result = workspace.build(args.project, args.tool)
        else:
            export_result = workspace.export_all(args.tool, args.copy)

            if args.build:
                build_result = workspace.build_all(args.tool)
        if build_result == 0 and export_result == 0:
            return 0
        else:
            return -1
    else:
        # not project known by pgen
        logging.warning("%s not found." % args.file)
        return -1

def setup(subparser):
    subparser.add_argument(
        "-f", "--file", help="YAML projects file", default='projects.yaml')
    subparser.add_argument(
        "-p", "--project", help="Project to be generated")
    subparser.add_argument(
        "-t", "--tool", help="Create project files for provided tool (uvision by default)")
    subparser.add_argument(
        "-b", "--build", action="store_true", help="Build defined projects")
    subparser.add_argument(
        "-defdir", "--defdirectory",
        help="Path to the definitions, otherwise default (~/.pg/definitions) is used")
    subparser.add_argument(
        "-c", "--copy", action="store_true", help="Copy all files to the exported directory")