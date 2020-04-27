from PyQt5 import QtCore,QtWidgets

import sys

class CheckDialog(object):

    def clickBox(self, state):

        if state == QtCore.Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')

    