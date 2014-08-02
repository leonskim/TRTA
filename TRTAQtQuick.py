import sys
import math
import Queue
from PySide import QtCore, QtGui, QtDeclarative
import Timer

# Basic environment
APP_TITLE 		= "Tomato, rather than Apple"
APP_QML_PATH 	= "./qml/TRTA.qml"

# Strings
STR_BTN_START			= "Start"
STR_BTN_PAUSE			= "Pause"
STR_BTN_RESET			= "Reset"
STR_PHASE_WORK			= "Work"
STR_PHASE_BREAK			= "Break"
STR_PHASE_LONGBREAK		= "Long break"
STR_PHASE_NONE			= "" # finished or reset


class TRTAQtQuick(QtDeclarative.QDeclarativeView):

	sig_set_start_button_text = QtCore.Signal(str)
	sig_move_gauge = QtCore.Signal(float)
	sig_set_phase = QtCore.Signal(str)
	sig_set_progress = QtCore.Signal(int)

	def __init__(self, parent=None):
		self.app = QtGui.QApplication(sys.argv)
		super(TRTAQtQuick, self).__init__(parent)

		# Message queue
		self.queue = Queue.Queue()

		self.setWindowTitle(APP_TITLE)
		self.setSource(QtCore.QUrl.fromLocalFile(APP_QML_PATH))
		self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

		# QML signal binding
		self.root = self.rootObject()
		self.btn_start = self.root.findChild(QtCore.QObject, "btn_start")
		self.btn_reset = self.root.findChild(QtCore.QObject, "btn_reset")
		self.progress = self.root.findChild(QtCore.QObject, "progress")
		self.root.gaugeAniFinished.connect(self.gaugeAniFinished)
		self.btn_start.clicked.connect(self.start)
		self.btn_reset.clicked.connect(self.reset)
		self.sig_set_start_button_text.connect(self.root.setStartButtonText)
		self.sig_move_gauge.connect(self.root.moveMeter)
		self.sig_set_phase.connect(self.root.setPhase)
		self.sig_set_progress.connect(self.progress.setProgress)

		# Setter thread
		self.tickFetcher = Timer.TickFetcher(self.tickFetcherFunc, self.queue)
		self.tickFetcher.start()

		# Timer thread
		self.tickGenerator = None

		# Show!
		self.show()
		self.app.exec_()

	def closeEvent(self, event):
		if self.tickGenerator != None and self.tickGenerator.isAlive():
			self.tickGenerator.finish()
		if self.tickFetcher != None and self.tickFetcher.isAlive():
			self.tickFetcher.finish()

	@QtCore.Slot()	
	def start(self):
		if self.tickGenerator == None:
			self.tickGenerator = Timer.TickGenerator(self.queue)
			self.tickGenerator.start()
			self.sig_set_start_button_text.emit(STR_BTN_PAUSE)
		else:
			if self.tickGenerator.isPaused():
				self.tickGenerator.pause(False)
				self.sig_set_start_button_text.emit(STR_BTN_PAUSE)
			else:
				self.tickGenerator.pause(True)
				self.sig_set_start_button_text.emit(STR_BTN_START)

	@QtCore.Slot()
	def reset(self):
		if self.tickGenerator != None:
			self.tickGenerator.finish()
			self.sig_set_progress.emit(0)
			self.sig_set_phase.emit(STR_PHASE_NONE)

	@QtCore.Slot()
	def gaugeAniFinished(self):
		if self.tickGenerator != None and self.tickGenerator.isAlive():
			self.tickGenerator.pause(False)

	def setPhase(self, phase, progress):
		self.gaugeBefore = 0
		self.gaugeNow = .0

		# 1. Pause timer (in order to play the gauge animation)
		self.tickGenerator.pause(True)

		# 2. Finished?
		if phase == Timer.PHASE_FINISHED:
			self.tickGenerator = None
			self.sig_set_start_button_text.emit(STR_BTN_START)

		# 3. Set progress
		self.sig_set_progress.emit(progress)

		# 4. Set phase (set text and run animation)
		self.sig_set_phase.emit(phase)

		# 5. Resume timer (noting to do here though)
		# When the gauge animation is completed, gaugeAniFinished() will be called.

	def setTime(self, time):
		# gauge width: 290px (1min = 11.6px, 1sec = 0.1933333px, 100ms = 0.01933333px)
		self.gaugeNow += 0.0193333

		if self.gaugeBefore != math.floor(self.gaugeNow):
			self.gaugeBefore = math.floor(self.gaugeNow)
			self.sig_move_gauge.emit(-1)

	def notify(self, notify_msg):
		# TODO: show message(phase) on the screen and play sound
		pass

	def tickFetcherFunc(self, message):
		if message.type == Timer.MSG_TYPE_TIME:
			self.setTime(message.value1)
		elif message.type == Timer.MSG_TYPE_PHASE:
			self.setPhase(message.value1, message.value2)