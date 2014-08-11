from PySide import QtCore, QtGui, QtDeclarative

# Basic environment
APP_NOTIFICATION_QML_PATH   = "./qml/Notification.qml"
SOUND_PATH                  = "./wav/notify.wav"

class Notification(QtDeclarative.QDeclarativeView):

    sig_set_size = QtCore.Signal(int, int)
    sig_set_text = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(Notification, self).__init__(parent)
        self.setSource(QtCore.QUrl.fromLocalFile(APP_NOTIFICATION_QML_PATH))
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | \
            QtCore.Qt.WindowStaysOnTopHint | \
            QtCore.Qt.Tool)
        self.viewport().setAutoFillBackground(False)

        # QML signal binding
        self.root = self.rootObject()
        self.sig_set_size.connect(self.root.setSize)
        self.sig_set_text.connect(self.root.setText)

        # Position
        #   Since it's impossible to know the screen size and position in QML(QtQuick1.1),
        #   Python should change it for the notification area and let QML know the size.
        self.move(0, 0)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setFixedSize(screen.width(), (screen.height() / 5))
        self.sig_set_size.emit(screen.width(), (screen.height() / 5))

        # Sound (default: ON)
        self.is_sound_enabled = True

        # Show!
        self.show()

    def notify(self, notify_msg):
        self.sig_set_text.emit(notify_msg)
        if self.is_sound_enabled:
            QtGui.QSound.play(SOUND_PATH) # Qt provides a simple audio(WAV) player. So simple!

    @QtCore.Slot(bool)
    def setSoundEnable(self, is_enabled):
        self.is_sound_enabled = is_enabled



