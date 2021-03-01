# Nix-shell environment switcher for sublime text 3

WARNING: Not at all done, don't use yet.

To try it out:

1. Somehow install the package.
   I have no idea how this is supposed to work yet, so here's what I did:

   ```
   cd ~/.config/sublime-text-3/Packages/User
   ln -s NixShellCommand.py /path/to/sublime-nix/src/NixShellCommand.py
   ln -s nix_shell /path/to/sublime-nix/src
   ```

2. Restart sublime: `subl`.
3. Right-click the directory that you want to load the `shell.nix` from.
   Select "Reload nix-shell Environment".

   Optional: Open your console using "View > Show Console" to see what's happening.

Your PATH variable should now be loaded from the `shell.nix` file.
