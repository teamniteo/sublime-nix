import sublime
import sublime_plugin
import subprocess
import sys
import os
import distutils.spawn
from pathlib import Path

class NixShellReloadCommand(sublime_plugin.WindowCommand):
  def run(self, dirs):
    print(dirs)
    if not dirs:
      print("No dirs passed to nix_shell plugin, exiting here.")
      return
    shellFile = None
    curDir = Path(dirs[0])
    print("Beginning search for shell.nix in " + str(curDir))
    shellFile = curDir.joinpath('shell.nix')
    # while shellFile is None:
    #   candidate = curDir.joinpath('shell.nix')
    #   if candidate.exists():
    #     shellFile = candidate
    #     print("Found shell file: " + str(shellFile)
    #   else:
    #     print("did not find shell file")
    #     break
    #     # parent = candidate.parent
    #     # print(parent)
    #     # if parent == candidate:
    #     #     break # We're at root
    #     # else:
    #     #     curDir = candidate.parent
    print(shellFile)
    if not shellFile.exists():
        print("No shell file found at " + str(shellFile))
        return
    bashPath = distutils.spawn.find_executable("bash")
    nixShellPath = distutils.spawn.find_executable("nix-shell")
    print(nixShellPath)
    args = [nixShellPath, "--command", "echo $PATH"]
    print("running " + ' '.join(args))
    print("in " + str(shellFile.parent))
    print(sys.version_info)
    # output = subprocess.check_output("nix-shell", shell=True)
    # print(output)
    process = subprocess.Popen(args,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     env = {}, # To make sure LD_PRELOAD doesn't get in the way.
                     cwd = str(shellFile.parent))
    stdout, stderr = process.communicate()
    print ("code: " + str(process.returncode))
    print ("stdout: " + str(stdout))
    print ("stderr: " + str(stderr))
    # print ("currently in path:" + os.environ['PATH'])
    new_path=str(stdout) + ":" + str(Path(nixShellPath).parent) + ":" + str(Path(bashPath).parent)
    os.environ['PATH'] = new_path
    print ("New path:")
    print(os.environ['PATH'])
