import subprocess

from PyKDE4 import plasmascript
from PyKDE4.plasma import Plasma
from PyKDE4.kdeui import KIcon
from PyKDE4.kdecore import *


class AutoJumpRunner(plasmascript.Runner):

    def init(self):

        """"Method called when the runner is created. Tells the user how the 
        runner is used."""

        self.addSyntax(Plasma.RunnerSyntax("j :str:", "Jump to :str:"))

    def match(self, context):

        """Method called to determine matches for the runner and subsequent
        actions."""

        if not context.isValid():
            return

        q = context.query()
        runInTerminal = True
        # look for our keyword 'j' or 'jo'
        if q.startsWith("j "):
            q = q[1:]
        elif q.startsWith("jo "):
            q = q[2:]
            runInTerminal = False
        else:
            return

        # strip the keyword and leading space
        q = q.trimmed()

        output = subprocess.Popen('autojump --completion %s' % qi, 
                                  shell=True, stdout=subprocess.PIPE).stdout

        # FIXME: This breaks in case autojump is not installed and the shell
        # returns some error text

        lines = output.readlines()

        if not lines:
            return

        for line in lines:

            line = line.rstrip()  # Trim end of line

            if not line:
                continue

            directory = line[line.find('/'):]
            # now create an action for the user, and send it to krunner
            m = Plasma.QueryMatch(self.runner)
            m.setText(directory)
            m.setType(Plasma.QueryMatch.ExactMatch)
            m.setIcon(KIcon("dialog-information"))
            m.setData(runInTerminal)
            context.addMatch(q, m)

    def run(self, context, match):

        "Method called when the specific action is selected by the user."

        runInTerminal = match.data().toPyObject()

        if runInTerminal:
            KToolInvocation.startServiceByDesktopName("dolphin",match.text())
        else:
            KToolInvocation.invokeTerminal("",match.text())


def CreateRunner(parent):

    "Return an instance of the runner."

    return AutoJumpRunner(parent)
