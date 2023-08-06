""" A file management utility """

import os
import pkg_resources
from os.path import expanduser
from os.path import exists as path_exists
from os.path import isfile as file_exists
from os.path import sep as native_slash
from platform import python_version

from instapy_chromedriver import binary_path

from socialcommons.util import highlight_print
from socialcommons.exceptions import SocialPyError


def get_workspace(Settings):
    """ Make a workspace ready for user """
    if Settings.WORKSPACE["path"]:
        workspace = verify_workspace_name(Settings.WORKSPACE["path"], Settings)
    else:
        home_dir = get_home_path()
        workspace = "{}/{}".format(home_dir, Settings.WORKSPACE["name"])

    message = "Workspace in use: \"{}\"".format(workspace)
    highlight_print(Settings, Settings.profile["name"],
                    message,
                    "workspace",
                    "info",
                    Settings.logger)
    update_workspace(workspace, Settings)
    update_locations(Settings)
    return Settings.WORKSPACE


def set_workspace(Settings, path=None):
    """ Set a custom workspace for use """
    if not Settings.IS_RUNNING:
        if path:
            path = verify_workspace_name(path, Settings)
            workspace_is_new = differ_paths(WORKSPACE["path"], path)
            if workspace_is_new:
                update_workspace(path, Settings)
                update_locations(Settings)
                message = "Custom workspace set: \"{}\" :]".format(path)
                highlight_print(Settings, Settings.profile["name"],
                                message,
                                "workspace",
                                "info",
                                Settings.logger)

            else:
                message = "Given workspace path is identical as current :/"
                highlight_print(Settings, Settings.profile["name"],
                                message,
                                "workspace",
                                "info",
                                Settings.logger)

        else:
            message = "No any custom workspace provided.\t~using existing.."
            highlight_print(Settings, Settings.profile["name"],
                            message,
                            "workspace",
                            "info",
                            Settings.logger)

    else:
        message = ("Sorry! You can't change workspace after"
                   " FacebookPy has started :>\t~using existing..")
        highlight_print(Settings, Settings.profile["name"],
                        message,
                        "workspace",
                        "info",
                        Settings.logger)


def update_workspace(latest_path, Settings):
    """ Update the workspace constant with its latest path """

    latest_path = slashen(latest_path, "native")
    validate_path(latest_path)
    Settings.WORKSPACE.update(path=latest_path)


def move_workspace(old_path, new_path):
    """ Find data files in old workspace folder and move to new location """
    # write in future


def update_locations(Settings):
    """
    As workspace has changed, locations also should be updated

    If the user already has set a location, do not alter it
    """

    # update logs location
    if not Settings.log_location:
        Settings.log_location = Settings.localize_path("FacebookPy", "logs")

    # update database location
    if not Settings.DATABASE_LOCATION:
        Settings.DATABASE_LOCATION = Settings.localize_path(
            "FacebookPy", "db", Settings.platform_name + "py.db")

    # update chromedriver location
    if not Settings.chromedriver_location:
        Settings.chromedriver_location = Settings.localize_path(
            "FacebookPy", "assets", Settings.specific_chromedriver)
        if (not Settings.chromedriver_location
                or not path_exists(Settings.chromedriver_location)):
            Settings.chromedriver_location = Settings.localize_path(
                "FacebookPy", "assets", "chromedriver")


def get_home_path():
    """ Get user's home directory """

    if python_version() >= "3.5":
        from pathlib import Path
        home_dir = str(Path.home())   # this method returns slash as dir sep*
    else:
        home_dir = expanduser("~")

    home_dir = slashen(home_dir)
    home_dir = remove_last_slash(home_dir)

    return home_dir


def slashen(path, direction="forward"):
    """ Replace backslashes in paths with forward slashes """

    if direction == "forward":
        path = path.replace('\\', '/')

    elif direction == "backwards":
        path = path.replace('/', '\\')

    elif direction == "native":
        path = path.replace('/', str(native_slash))
        path = path.replace('\\', str(native_slash))

    return path


def remove_last_slash(path):
    """ Remove the last slash in the given path [if any] """

    if path.endswith('/'):
        path = path[:-1]

    return path


def verify_workspace_name(path, Settings):
    """ Make sure chosen workspace name is FacebookPy friendly """

    path = slashen(path)
    path = remove_last_slash(path)
    custom_workspace_name = path.split('/')[-1]
    default_workspace_name = Settings.WORKSPACE["name"]

    if default_workspace_name not in custom_workspace_name:
        if default_workspace_name.lower() not in custom_workspace_name.lower():
            path += "/{}".format(default_workspace_name)
        else:
            nicer_name = (custom_workspace_name.lower().replace(
                default_workspace_name.lower(), default_workspace_name))
            path = path.replace(custom_workspace_name, nicer_name)

    return path


def differ_paths(old, new):
    """ Compare old and new paths """

    if old and old.endswith(('\\', '/')):
        old = old[:-1]
        old = old.replace('\\', '/')

    if new and new.endswith(('\\', '/')):
        new = new[:-1]
        new = new.replace('\\', '/')

    return (new != old)


def validate_path(path):
    """ Make sure the given path exists """

    if not path_exists(path):
        try:
            os.makedirs(path)

        except OSError as exc:
            exc_name = type(exc).__name__
            msg = ("{} occured while making \"{}\" path!"
                   "\n\t{}".format(exc_name,
                                   path,
                                   str(exc).encode("utf-8")))
            raise SocialPyError(msg)


def get_chromedriver_location(Settings):
    """ Solve chromedriver access issues """
    CD = Settings.chromedriver_location

    if Settings.OS_ENV == "windows":
        if not CD.endswith(".exe"):
            CD += ".exe"

    if not file_exists(CD):
        workspace_path = slashen(Settings.WORKSPACE["path"], "native")
        assets_path = "{}{}assets".format(workspace_path, native_slash)
        validate_path(assets_path)

        CD = binary_path
        chrome_version = pkg_resources.get_distribution(
            "instapy_chromedriver").version
        message = "Using built in instapy-chromedriver" \
                  "executable (version {})".format(chrome_version)
        highlight_print(Settings, Settings.profile["name"],
                        message,
                        "workspace",
                        "info",
                        Settings.logger)

    # save updated path into settings
    Settings.chromedriver_location = CD
    return CD


def get_logfolder(username, multi_logs, Settings):
    if multi_logs:
        logfolder = "{0}{1}{2}{1}".format(Settings.log_location,
                                          native_slash,
                                          username)
    else:
        logfolder = (Settings.log_location + native_slash)

    validate_path(logfolder)
    return logfolder
