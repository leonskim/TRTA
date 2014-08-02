import sys
import time
import datetime
import Queue
from PySide import QtCore, QtGui
import Timer

# Basic environment
APP_TITLE 		= "Tomato, rather than Apple"
APP_GUI_STYLE	= "plastique"

# Strings
STR_BTN_START			= "Start"
STR_BTN_PAUSE			= "Pause"
STR_BTN_RESET			= "Reset"
STR_BTN_EXIT			= "Exit"
STR_TIME_ZERO			= "0:00:00"
STR_PHASE_READY			= "Ready"
STR_PHASE_WORK			= "Work"
STR_PHASE_BREAK			= "Break"
STR_PHASE_LONGBREAK		= "Long break"


class TRTAQtWidget(QtGui.QDialog):
	def __init__(self):
		QtGui.QApplication.setStyle(APP_GUI_STYLE)
		self.app = QtGui.QApplication(sys.argv)
		QtGui.QDialog.__init__(self, None)

		# Message queue
		self.queue = Queue.Queue()

		# GUI init
		self.setWindowTitle(APP_TITLE)
		self.setMinimumSize(250, 200)
		self.vbox_layout = QtGui.QVBoxLayout() # Main layout
		self.hbox_top_layout = QtGui.QHBoxLayout() # Top layout
		self.hbox_bottom_layout = QtGui.QHBoxLayout() # Bottom layout
		self.phase_label = QtGui.QLabel(STR_PHASE_READY)
		self.time_label = QtGui.QLabel(STR_TIME_ZERO)
		self.time_font = self.time_label.font()
		self.phase_font = self.phase_label.font()
		self.time_font.setPointSize(20)
		self.phase_font.setPointSize(15)
		self.time_label.setFont(self.time_font)
		self.phase_label.setFont(self.phase_font)
		self.start_button = QtGui.QPushButton(STR_BTN_START)
		self.reset_button = QtGui.QPushButton(STR_BTN_RESET)
		self.exit_button = QtGui.QPushButton(STR_BTN_EXIT)
		self.hbox_top_layout.addWidget(self.phase_label)
		self.hbox_top_layout.addWidget(self.time_label)
		self.hbox_bottom_layout.addWidget(self.reset_button)
		self.hbox_bottom_layout.addWidget(self.exit_button)
		self.vbox_layout.addItem(self.hbox_top_layout)
		self.vbox_layout.addWidget(self.start_button)
		self.start_button.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.vbox_layout.addItem(self.hbox_bottom_layout)
		self.setLayout(self.vbox_layout)

		# Setter thread
		self.tickFetcher = Timer.TickFetcher(self.tickFetcherFunc, self.queue)
		self.tickFetcher.start()

		# Timer thread
		self.tickGenerator = None

		# Signals
		self.start_button.clicked.connect(self.start)
		self.reset_button.clicked.connect(self.reset)
		self.exit_button.clicked.connect(self.exit)

		# Run the application
		self.show()
		self.app.exec_()

	def closeEvent(self, event):
		if self.tickGenerator != None and self.tickGenerator.isAlive():
			self.tickGenerator.finish()
		if self.tickFetcher != None and self.tickFetcher.isAlive():
			self.tickFetcher.finish()

	@QtCore.Slot()
	def exit(self):
		self.close()

	@QtCore.Slot()
	def reset(self):
		if not self.tickGenerator == None:
			self.tickGenerator.finish()
			self.start_button.setText(STR_BTN_START)

	@QtCore.Slot()
	def start(self):
		if self.tickGenerator == None:
			self.tickGenerator = Timer.TickGenerator(self.queue)
			self.tickGenerator.start()

		if self.start_button.text() == STR_BTN_START: 
			self.tickGenerator.pause(False)
			self.start_button.setText(STR_BTN_PAUSE)
		else:
			self.tickGenerator.pause(True)
			self.start_button.setText(STR_BTN_START)

	def setPhase(self, phase):
		phase_str = STR_PHASE_READY

		if phase == Timer.PHASE_WORK:			phase_str = STR_PHASE_WORK
		elif phase == Timer.PHASE_BREAK:		phase_str = STR_PHASE_BREAK
		elif phase == Timer.PHASE_LONGBREAK:	phase_str = STR_PHASE_LONGBREAK
		elif phase == Timer.PHASE_FINISHED:
			self.tickGenerator = None
			self.start_button.setText(STR_BTN_START)
			phase_str = STR_PHASE_READY
			self.setTime(0)
		self.phase_label.setText(phase_str)

	def setTime(self, time):
		time_str = str(datetime.timedelta(seconds = time))
		self.time_label.setText(time_str)

	def notify(self, notify_msg):
		# TODO: show message(phase) on the screen and play sound
		pass

	def tickFetcherFunc(self, message):
		if message.type == Timer.MSG_TYPE_TIME:
			self.setTime(message.value1)
		elif message.type == Timer.MSG_TYPE_PHASE:
			self.setPhase(message.value1)
