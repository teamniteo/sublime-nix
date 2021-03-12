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
    print(dirs)
    if not dirs:
      print("No dirs passed to nix_shell plugin, exiting here.")
      return
    shellFile   = None
    curDir = Path(dirs[0])
    print("Beginning search for shell.nix in " + str(curDir))
    shellFile = curDir.joinpath('shell.nix')
    print(shellFile)
    if not shellFile.exists():
        print("No shell file found at " + str(shellFile))
        return
    bashPath = distutils.spawn.find_executable("bash")
    nixShellPath = distutils.spawn.find_executable("nix-shell")
    print("nix-shell found at " + nixShellPath)
    gitPath = distutils.spawn.find_executable("git")
    print("git found at " + gitPath)
    bashPath = distutils.spawn.find_executable("bash")
    print("bash found at " + bashPath)
    args = [nixShellPath, "--command", "export"]
    print("running " + ' '.join(args))
    print("in " + str(shellFile.parent))

    process = subprocess.Popen(args,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     # We empty the path to make sure LD_PRELOAD doesn't get in
                     # the way.  But we also need to make sure that git is
                     # there otherwise the `builtins.fetchGit` doesn't work.
                     env = { "PATH": str(Path(gitPath).parent) + ":" + str(Path(bashPath).parent) },
                     cwd = str(shellFile.parent))
    stdout, stderr = process.communicate()
    print ("code: " + str(process.returncode))
    print ("stdout: " + str(stdout))
    print ("stderr: " + str(stderr))


    regex = r'declare -x (\w+)="((?:\\.|[^"\\])+)"'

    new_env = dict(re.findall(regex, stdout.decode('utf8')))
    print(new_env)
    os.environ = new_env
