from distutils.dir_util import copy_tree
from ..utils.utils import resource_path
from ..model.export_avatar_params import ExportAvatarParams
import os
import json
import win32com.shell.shell as shell

TASK_PARAMS_FILE_NAME = 'nowyou_task_params.txt'


def export_avatar(
        vstitcher_data_path: str,
        vstitcher_launcher_file: str,
        work_path: str,
        body_sizes: dict
) -> str:

    # copy plugin script to VStitcher folder
    plugin_path = os.path.join(vstitcher_data_path, 'Plugins\\Avatar_export')
    copy_tree(resource_path('\\vstitcher_plugins\\avatar_export'), plugin_path)

    # set up task params
    params = ExportAvatarParams(body_sizes, work_path)
    data = json.dumps(params)

    # save JSON params to file
    with open(os.path.join(TASK_PARAMS_FILE_NAME, plugin_path), 'w') as outfile:
        json.dump(data, outfile)

    # launch VStitcher
    se_ret = shell.ShellExecuteEx(fMask=0x140, lpFile=r"{}".format(vstitcher_launcher_file), nShow=1)

    # wait for task finish
    # close VStitcher
    # process result
