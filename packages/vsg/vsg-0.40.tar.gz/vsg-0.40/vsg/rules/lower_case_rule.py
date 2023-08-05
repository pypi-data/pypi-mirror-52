
from vsg import rule
from vsg import fix
from vsg import check
from vsg import utils


class lower_case_rule(rule.rule):
    '''
    Checks for and fixes words that are not lowercase.

    Parameters
    ----------

    name : string
       The group the rule belongs to.

    identifier : string
       unique identifier.  Usually in the form of 00N.

    sTrigger : string
       The line attribute the rule applies to.

    sWord : string
       The word to lowercase.

    Attributes
    ----------

    self.phase : integer = 6
       Sets the phase the rule will run in.

    self.solution : string = None
       Instructions on how to fix the violation.
    '''

    def __init__(self, name=None, identifier=None, sTrigger=None, sWord=None):
        rule.rule.__init__(self, name, identifier)
        self.phase = 6
        self.solution = None
        self.sTrigger = sTrigger
        self.sWord = sWord

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.__dict__[self.sTrigger]:
            lLine = oLine.lineNoComment.split()
            for sCurrentWord in lLine:
                if self.sWord == utils.strip_semicolon_from_word(sCurrentWord.lower()):
                    check.is_lowercase(self, sCurrentWord, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.lower_case(self, oFile.lines[iLineNumber], self.sWord)
