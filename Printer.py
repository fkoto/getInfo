class Printer:
    """This class is just a helper class,
    responsible to print in stdout all incoming
    strings, and also filter if verbose mode is off."""

    def __init__(self, mode):
        self.verboseMode = mode

    def doprint(self, strline, bypass=False):
        if bypass:
            print strline
            return

        if self.verboseMode:
            print strline
