import sublime
import sublime_plugin
import subprocess
import sys
import os
import distutils.spawn
import re
from pathlib import Path

class NixShellReloadCommand(sublime_plugin.WindowCommand):
  def run(self, dirs):
    if not dirs:
      return # Do nothing
    shellFile   = None
    curDir = Path(dirs[0])
    shellFile = curDir.joinpath('shell.nix')
    if not shellFile.exists():
        print("No shell file found at " + str(shellFile))
        return
    nixShellPath = distutils.spawn.find_executable("nix-shell")
    args = [nixShellPath, "--command", "export"]

    # We remove the LD_PRELOAD to make sure we don't run into segfaults.
    os.environ.pop("LD_PRELOAD", None)

    process = subprocess.Popen(args,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     env = os.environ,
                     cwd = str(shellFile.parent))
    stdout, stderr = process.communicate()


    regex = r'declare -x (\w+)="((?:\\.|[^"\\])+)"'

    new_env = dict(re.findall(regex, stdout.decode('utf8')))
    os.environ = new_env
