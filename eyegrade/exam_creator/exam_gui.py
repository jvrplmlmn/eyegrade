# -*- coding: utf-8 -*-

from PyQt4.QtGui import (QAction,
                         QApplication,
                         QDialog,
                         QDialogButtonBox,
                         QHBoxLayout,
                         QMainWindow,
                         QIcon,
                         QKeySequence,
                         QLabel,
                         QMenu,
                         QPushButton,
                         QVBoxLayout,
                         QWidget)

from PyQt4.QtCore import Qt

from eyegrade.utils import (resource_path,
                            program_name,
                            version,
                            web_location,
                            source_location)
import eyegrade.utils as utils

class DialogAbout(QDialog):
    def __init__(self, parent):
        super(DialogAbout, self).__init__(parent)
        text = \
             """
             <center>
             <p><img src='{0}' width='64'> <br>
             {1} {2} <br>
             (c) 2013 Javier Palomo Almena <br>
             <a href='{3}'>{3}</a> <br>
             <a href='{4}'>{4}</a>

             <p>
             This program is free software: you can redistribute it<br>
             and/or modify it under the terms of the GNU General<br>
             Public License as published by the Free Software<br>
             Foundation, either version 3 of the License, or (at your<br>
             option) any later version.
             </p>
             <p>
             This program is distributed in the hope that it will be<br>
             useful, but WITHOUT ANY WARRANTY; without even the<br>
             implied warranty of MERCHANTABILITY or FITNESS FOR A<br>
             PARTICULAR PURPOSE. See the GNU General Public License<br>
             for more details.
             </p>
             <p>
             You should have received a copy of the GNU General Public<br>
             License along with this program.  If not, see<br>
             <a href='http://www.gnu.org/licenses/gpl.txt'>
             http://www.gnu.org/licenses/gpl.txt</a>.
             </p>
             </center>
             """.format(resource_path('logo.svg'), program_name, version,
                        web_location, source_location)
        self.setWindowTitle('About')
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        label = QLabel(text)
        label.setTextInteractionFlags((Qt.LinksAccessibleByKeyboard
            | Qt.LinksAccessibleByMouse
            | Qt.TextBrowserInteraction
            | Qt.TextSelectableByKeyboard
            | Qt.TextSelectableByMouse))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(label)
        layout.addWidget(buttons)


class ActionsManager(object):
    """Creates and manages the toolbar buttons."""

    _actions_file_data = [
        ('exit', 'exit.svg', '&Exit', Qt.Key_Escape),
        ]

    _actions_help_data = [
        ('help', None, 'Online &Help', None),
        ('about', None, '&About', None),
        ]

    def __init__(self, window):
        """Creates a manager for the given toolbar object."""
        self.window = window
        self.menubar = window.menuBar()
        self.menus = {}
        self.actions_file = {}
        self.actions_help = {}
        action_lists = {'file': [], 'help': []}
        for key, icon, text, shortcut in ActionsManager._actions_file_data:
            self._add_action(key, icon, text, shortcut, self.actions_file,
                             action_lists['file'])
        for key, icon, text, shortcut in ActionsManager._actions_help_data:
            self._add_action(key, icon, text, shortcut, self.actions_help,
                             action_lists['help'])

        self._populate_menubar(action_lists)

    def register_listener(self, key, listener):
        actions = self._select_action_group(key[0])
        print 'ActionsManager.register_listener - key[1]: ', key[1]
        assert key[1] in actions
        actions[key[1]].triggered.connect(listener)

    def _select_action_group(self, key):
        print 'ActionsManager._select_action_group - key:', key
        if key == 'file':
            return self.actions_file
        elif key == 'help':
            return self.actions_help
        assert False, 'Undefined action group key: {0}.format(key)'

    def _add_action(self, action_name, icon_file, text, shortcut,
            group, actions_list):
        action = self._create_action(action_name, icon_file, text, shortcut)
        if action_name.startswith('+'):
            if action_name.startswith('++'):
                action_name = action_name[2:]
            else:
                action_name = action_name[1:]
        if not action.isSeparator():
            group[action_name] = action
        actions_list.append(action)

    def _create_action(self, action_name, icon_file, text, shortcut):
        if action_name == '*separator*':
            action = QAction(self.window)
            action.setSeparator(True)
        else:
            if icon_file:
                action = QAction(QIcon(resource_path(icon_file)),
                                 text, self.window)
            else:
                action = QAction(text, self.window)
        if shortcut is not None:
            action.setShortcut(QKeySequence(shortcut))
        if action_name.startswith('+'):
            action.setCheckable(True)
            if action_name.startswith('++'):
                action.setChecked(True)
        return action

    def _populate_menubar(self, action_lists):
        self.menus['file'] = QMenu('&File', self.menubar)
        self.menus['help'] = QMenu('&Help', self.menubar)
        self.menubar.addMenu(self.menus['file'])
        self.menubar.addMenu(self.menus['help'])
        for action in action_lists['file']:
            self.menus['file'].addAction(action)
        for action in action_lists['help']:
            self.menus['help'].addAction(action)

# class ExamView(QDialog):
#     def __init__(self):
#         super(ExamView, self).__init__()
#         self.label = QLabel('Label')
#         self.button = QPushButton('Button')
#         layout = QHBoxLayout()
#         layout.addWidget(self.label)
#         layout.addWidget(self.button)
#         self.setLayout(layout)
#         self.button.clicked.connect(self.close)

class ExamView(QWidget):
    def __init__(self, parent):
        super(ExamView, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label_examview = QLabel('Label (ExamView)')
        self.button = QPushButton('Button (ExamView)')
        layout.addWidget(self.label_examview)
        layout.addWidget(self.button)


class CenterView(QWidget):
    def __init__(self, parent=None):
        super(CenterView, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.examview = ExamView(self)
        self.label_up_centerview = QLabel('Label Up (CenterView)')
        self.label_down_centerview = QLabel('Label Down (CenterView)')
        layout.addWidget(self.label_up_centerview)
        layout.addWidget(self.examview)
        layout.addWidget(self.label_down_centerview)

    def register_listener(self, key, listener):
        """Registers listeners for the center view.

        Available listeners are:

        - ('_____', '_____'): description
        """

class MainWindow(QMainWindow):
    """
    * Manages the GUI application’s control flow and main settings.
    * Contains the main event loop, where all events from the window
        system and other sources are processed and dispatched.
    * It also handles the application’s initialization, finalization, and
        provides session management.
    * It handles most of the system-wide and application-wide settings.
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = CenterView()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Exam Creator")
        self.setWindowIcon(QIcon(resource_path('logo.svg')))
        self.adjustSize()
        self.setFixedSize(self.sizeHint())


class Interface(object):
    def __init__(self, file, argv):
        self.app = QApplication(argv)
        self.window = MainWindow()
        self.actions_manager = ActionsManager(self.window)
        self.window.show()
        self.window.raise_()
        self.register_listener(('actions', 'file', 'exit'),
                               self.window.close)
        self.register_listener(('actions', 'help', 'about'),
                               self.show_about_dialog)
        #self.register_listener((), self.show_about_dialog)
        #self.register_listener(('actions', 'help', 'about'),
        #                       self.show_about_dialog)


    def run(self):
        return self.app.exec_()

    def register_listeners(self, listeners):
        """Registers a dictionary of listeners for the events of the gui.

        The listeners are specified as a dictionary with pais
        event_key->listener. Keys are tuples of strings such as
        ('action', 'session', 'close').

        """
        for key, listener in listener.iteritems():
            self.register_listener((key), listener)

    def register_listener(self, key, listener):
        """Registers a single listener for the events of the gui.

        Keys are tuples of string such as ('action', 'session',
        close').
        """
        print 'Interface.register_listener - key[0]:', key[0]
        if key[0] == 'actions':
            self.actions_manager.register_listener(key[1:], listener)
        else:
            assert False, 'Unkown event key {0}'.format(key)


    def show_about_dialog(self):
        dialog = DialogAbout(self.window)
        dialog.exec_()
