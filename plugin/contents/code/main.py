from PyKDE4 import plasmascript
from PyKDE4.plasma import Plasma
from PyKDE4.kdeui import KIcon, KMessageBox
from PyKDE4.kdecore import *

import os

class AutoJumpRunner(plasmascript.Runner):
 
    def init(self):
        # called upon creation to let us run any intialization
        # tell the user how to use this runner
		self.addSyntax(Plasma.RunnerSyntax("j :str:", "Jump to :str:"))
 
    def match(self, context):
        # called by krunner to let us add actions for the user
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
 
        f = os.popen('autojump --completion %s' % q)
        result = f.read()
        lines = result.split('\n')
        if len(lines) == 0:
            return
        
        for line in lines:
            if len(line) > 0:
                dir = line[line.find('/'):]
                # now create an action for the user, and send it to krunner
                m = Plasma.QueryMatch(self.runner)
                m.setText(dir)
                m.setType(Plasma.QueryMatch.ExactMatch)
                m.setIcon(KIcon("dialog-information"))
                m.setData(runInTerminal)
                context.addMatch(q, m)
      
    def run(self, context, match):
        # called by KRunner when the user selects our action,        
        runInTerminal = match.data()
        if runInTerminal.toString() == "false":
            KToolInvocation.startServiceByDesktopName("dolphin",match.text())
        else:
            KToolInvocation.invokeTerminal("",match.text())


        
def CreateRunner(parent):
    # called by krunner, must simply return an instance of the runner object
    return AutoJumpRunner(parent)
