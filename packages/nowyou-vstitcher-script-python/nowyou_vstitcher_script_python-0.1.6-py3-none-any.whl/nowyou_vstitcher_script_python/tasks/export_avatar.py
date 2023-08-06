from ..utils.utils import resource_path
from ..model.export_avatar_params import ExportAvatarParams
import os
import json
import zipfile
import shutil
import win32com.shell.shell as shell

TASK_PARAMS_FILE_NAME = 'nowyou_task_params.txt'
PLUGIN_PATH_NAME = 'nowyou_autorun'


def export_avatar(
        vstitcher_data_path: str,
        vstitcher_launcher_file: str,
        work_path: str,
        body_sizes: dict
) -> str:

    # copy plugin script to VStitcher folder
    with zipfile.ZipFile(resource_path('\\vstitcher_plugins\\avatar_export.zip'), 'r') as zip_ref:
        plugin_path = os.path.join(vstitcher_data_path, 'Plugins')

        # clean previous version of plugin
        plugin_folder = os.path.join(plugin_path, PLUGIN_PATH_NAME)
        if os.path.exists(plugin_folder) and os.path.isdir(plugin_folder):
            shutil.rmtree(plugin_folder)

        zip_ref.extractall(plugin_path)

    # set up task params
    params = {
        body_sizes,
        work_path
    }
    data = json.dumps(params)

    # save JSON params to file
    with open(os.path.join(TASK_PARAMS_FILE_NAME, plugin_path), 'w') as outfile:
        json.dump(data, outfile)

    # launch VStitcher
    se_ret = shell.ShellExecuteEx(fMask=0x140, lpFile=r"{}".format(vstitcher_launcher_file), nShow=1)

    # wait for task finish
    # close VStitcher
    # delete plugin
    # process result
