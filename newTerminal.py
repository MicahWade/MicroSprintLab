import sys
import shutil
import subprocess


def GetTerminal():
    if sys.platform.startswith("win"):
        if shutil.which("powershell"):
            return "powershell"
        elif shutil.which("wt"):
            return "wt"
        else:
            return "cmd"
    elif sys.platform == "darwin":
        return "open -a Terminal"
    elif sys.platform.startswith("linux"):
        for cmd in [
            "kitty",
            "x-terminal-emulator",
            "gnome-terminal",
            "konsole",
            "xfce4-terminal",
            "lxterminal",
            "xterm",
            "tilix",
            "mate-terminal",
            "terminator",
        ]:
            if shutil.which(cmd):
                return cmd
        raise OSError("Could Not Find your Linux Terminal")
    else:
        raise OSError("Unknown OS Please File a Bug Report")


def OpenOtherTerminal(command: str):
    terminal = GetTerminal()

    if sys.platform.startswith("win"):
        subprocess.Popen([terminal, "/K", command])
    elif sys.platform == "darwin":
        subprocess.Popen(f'{terminal} "{command}"', shell=True)
    else:
        if (
            terminal == "x-terminal-emulator"
            or terminal.endswith("-terminal")
            or terminal in ["xterm", "tilix", "terminator"]
        ):
            subprocess.Popen([terminal, "--", "bash", "-c", f"{command}; exec bash"])
        else:
            subprocess.Popen([terminal, "-e", "bash", "-c", f"{command}; exec bash"])
