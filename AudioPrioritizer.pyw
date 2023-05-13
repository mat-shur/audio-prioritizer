import signal, ctypes, sys, base64, subprocess, datetime
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('AudioPrioritizer.AudioPrioritizer.AudioPrioritizer.0.1')
icon_data = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFKUlEQVR4nO1Za2wUVRSeuiAiCpbSveduFwpLFa3GCCUKTfeebRUpkGgQqiAPlcQfhpdvSfyhUWMqSaOYtIq0s1qkO6nG+I5/jInxFXzESGyZQUwEq0ZjG1IRG6xj7rrTOTuZ2e5sd6kl+yU3pHfunvt99zzuA0UpoogiijgrwRjGgIu3GRdfAOBT1dXV5yoTBQB4D3AcBo6m1RjHF5X/P5oCAOJZStxuYrCqqnGKP1v4pvwdAG5SCg3Oa84HwDfSVh3ERwzwd+vvstm1oezt4aW2HeyfM6eutIDkcRZw8WnaigNqlZV4HgD25SJAUZoCDEQvsddcEPKMRecxQN1BXk5WIr/nLkCRv20iXjgJUFeeV/KhkFgIXPxMyA8zjtscJEYEbN/V2dje1esqgvPo9TJUZNjJcEx1lzDAL+2FEQ/njXwwFLsWOJ4g8X4KILbGOY4K2PPCQTOuGZ+72QMQCeLB+0fm4eJW0t+nKDWTsycZbGDBYF3E2RjD2xngEE0yzkXUzQbnsZ8cAvrcxrGQ2EIW40d736iZzEAcJ15YmZH0zJlXT2dctAEXv7iXw/TGAI8B1FW72XrptZ6yyPxVQ9kIUJJE8QdrLOditfVF5hQpx3FP8owtm8ZAHM6GeMrYoXC4ocLN1r7uI1VxTTcuWXCjmZ0ARWEcH7U3PvEKEbCYeltRcJKrAbnlOwhKLxx1a4yLVysr8SI3O2riSG1cM36La4bpJkAmaWqP6JfJ61H7dWJSJvMx2zvRRe4CuDhkDZLJo+SAji5jrarppyR5LwGMRRtIYn5Cf884PiGjgPPoBsfiHiDHku1eAk5bgzzdlAFqwtgZ1/Rhi7yXAOk5BuKvVP8/jOHc0WwzFt066rmKho+XIbmZAIjNdFPp7jYDakJ/jhLPJOA/O+J1Eu8PZVm2rfD60JeAzs6vp8U1vU3G9cJFG5Lf5b9uhLMVIEME7BV9x8mlrKz2wjQBwboIKbPHfQlQNWOvRYiOGYuAUKh+AbH1fbqXhZqq+SqtkKS4/OFTgN6fbwFyvwHb1gky3TnAxd+pUBmyu3ESEXDalwBKKF8CSkuvm0FCYsCaq7wcLyBEBwmNEpnwVuJbh8VxE+AVQowtDdJ9yOqX9wE3weMmAAA3uiWx3KRI/7e2Z+rne+XMOAlIK6MPjnCA6G1kjm5bWGz5qGWUAf5pDQqHl0wtlADnRgZQXznCgWOLvUuLR2xh4j4iuM3DA+IzEn+7Z1WIi2X9bWn92LRaPgRkPEoAvUaKFaT/6REBLLrV3QMct1GCo7VcBWRzmAMuBuWdOv1Emrz9fSMT3VVAsgaT2MzcYmPKAfcFFI+5xb9flLAQ3gFcvAWAhjw6X3b5TcPVV6w1ZZsXWZEk37BsR14FhMNLpjKOv7pdaMYMVTPiXgQ7Dhw2793VZT7Z8v6YBHCOd6aXyaaA/U2slt993Ycp9u83pscTuqom9AEnwfWbdycnDYXrzbt27MtZAJBLPed4t9UfDIkb/JxafYNxfJ7mxrqNzaaa0HPwQNTtWUXaP1iQZxUL8l6QNglHc/mqB8z2l3t8J7ETaasPeDJT9cn7u+g1S7eYrR1fjUFAU4Bx7CH7xTMFIe+YsJWKuPKqdebcSGNOAnjaBV8MyPdX5UwgyMVO5/8NyBapWpmsWH48AGfyeZ2CMXFz8qmRCFhzy+NWYmedA+MK+Vonr4QVsxveW7+p+TtSmSaGAIo97xpT4gmjSwpQNf0DZaKivat38d7uozPGm0cRRZxN+BeIFgQuVPlcdAAAAABJRU5ErkJggg=="

required_modules = ['tendo', 'PyQt5', 'pycaw']
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        subprocess.check_call(['pip', 'install', module])

from tendo import singleton

from PyQt5.QtWidgets import QSystemTrayIcon, QScrollBar, QMenu, QAction, QFrame, QApplication, QSlider, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QIcon, QFont, QPixmap

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioMeterInformation


class UnselectableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.items = {}

        self.prio_items = []
        self.unprio_items = []
        self.totalmute_items = []

        self.setSelectionMode(self.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)

        self.vertical_scroll = QScrollBar(Qt.Vertical)
        self.horizontal_scroll = QScrollBar(Qt.Horizontal)

        self.vertical_scroll.setStyleSheet("QScrollBar:vertical {width: 5px} QScrollBar::handle:vertical {background: white} QScrollBar::add-line:vertical {background: none;} QScrollBar::add-page:vertical {background: none;} QScrollBar::sub-line:vertical {background: none;} QScrollBar::sub-page:vertical {background: none;}")
        self.horizontal_scroll.setStyleSheet("QScrollBar:horizontal {height: 5px;} QScrollBar::handle:horizontal {background: white;} QScrollBar::add-line:horizontal {background: none;} QScrollBar::add-page:horizontal {background: none;} QScrollBar::sub-line:horizontal {background: none;} QScrollBar::sub-page:horizontal {background: none;}")

        self.setVerticalScrollBar(self.vertical_scroll)
        self.setHorizontalScrollBar(self.horizontal_scroll)

        self.setStyleSheet("color: white; background-color: #2b2b2b; border: none; outline: none;")
        self.setMaximumWidth(220)
        self.setMaximumHeight(120)

    def is_lower_prio(self, name):
        other_indices = [i for i, item in enumerate(self.prio_items) if item != name and self.items[item]['is_playing']]
        if other_indices:
            if self.prio_items.index(name) > min(other_indices):
                return True

        return False

    def update_other_buttons(self):
        for item in self.items:
            if item in self.prio_items:
                self.items[item]['widget'].button_prio.setText(str(self.prio_items.index(item) + 1))
            else:
                self.items[item]['widget'].button_prio.setText("")

    def is_any_playing(self):
        for item in self.items:
            if self.items[item]['is_playing'] and item not in self.totalmute_items:
                return True

    def is_prio_playing(self):
        for item in self.prio_items:
            if self.items[item]['is_playing']:
                return True

        return False

    def remove_item(self, name):
        for i in range(self.count()):
            item = self.item(i)

            if item is not None:
                widget = self.itemWidget(item)

                if widget.item_name == name:
                    self.takeItem(i)
                    break


class ItemWidget(QWidget):
    def __init__(self, item_name, list_widget, parent=None):
        super().__init__(parent)

        self.item_name = item_name
        self.list_widget = list_widget

        self.label = QLabel(self.item_name, self)

        self.button_prio = QPushButton(self)
        self.button_prio.clicked.connect(self.on_button_prio_clicked)
        self.button_prio.setFont(QFont('Times', 5))
        self.button_prio.setFixedSize(10, 10)
        self.button_prio.setStyleSheet("border-radius: 5px; background-color: gray; border: none;")

        self.button_unprio = QPushButton(self)
        self.button_unprio.clicked.connect(self.on_button_unprio_clicked)
        self.button_unprio.setFixedSize(10, 10)
        self.button_unprio.setStyleSheet("border-radius: 5px; background-color: #FFEF00; border: none;")

        self.button_muted = QPushButton(self)
        self.button_muted.clicked.connect(self.on_button_muted_clicked)
        self.button_muted.setFixedSize(10, 10)
        self.button_muted.setStyleSheet("border-radius: 5px; background-color: gray; border: none;")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.button_prio)
        self.layout.addWidget(self.button_unprio)
        self.layout.addWidget(self.button_muted)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.setStyleSheet("color: white; background-color: #2b2b2b; border: none; outline: none;")

    def on_button_prio_clicked(self):
        if self.item_name not in self.list_widget.items:
            return

        self.button_prio.setStyleSheet("border-radius: 5px; background-color: #00FF00; border: none;color: black")
        self.button_unprio.setStyleSheet("border-radius: 5px; background-color: gray; border: none;")
        self.button_muted.setStyleSheet("border-radius: 5px; background-color: gray; border: none;")

        if self.item_name not in self.list_widget.prio_items:
            self.list_widget.prio_items.append(self.item_name)
            self.button_prio.setText(str(self.list_widget.prio_items.index(self.item_name) + 1))

        if self.item_name in self.list_widget.unprio_items:
            self.list_widget.unprio_items.remove(self.item_name)

        if self.item_name in self.list_widget.totalmute_items:
            self.list_widget.totalmute_items.remove(self.item_name)

    def on_button_unprio_clicked(self):
        if self.item_name not in self.list_widget.items:
            return

        self.button_prio.setStyleSheet("border-radius: 5px; background-color: gray; border: none;")
        self.button_unprio.setStyleSheet("border-radius: 5px; background-color: #FFEF00; border: none;")
        self.button_muted.setStyleSheet("border-radius: 5px; background-color: gray; border: none;")

        if self.item_name not in self.list_widget.unprio_items:
            self.list_widget.unprio_items.append(self.item_name)

        if self.item_name in self.list_widget.prio_items:
            self.list_widget.prio_items.remove(self.item_name)
            self.button_prio.setText('')
            self.list_widget.update_other_buttons()

        if self.item_name in self.list_widget.totalmute_items:
            self.list_widget.totalmute_items.remove(self.item_name)

    def on_button_muted_clicked(self):
        if self.item_name not in self.list_widget.items:
            return

        self.button_prio.setStyleSheet("border-radius: 5px; background-color: gray; border: none;")
        self.button_unprio.setStyleSheet("border-radius: 5px; background-color: gray; border: none;")
        self.button_muted.setStyleSheet("border-radius: 5px; background-color: #D32F2F; border: none;")

        if self.item_name not in self.list_widget.totalmute_items:
            self.list_widget.totalmute_items.append(self.item_name)

        if self.item_name in self.list_widget.prio_items:
            self.list_widget.prio_items.remove(self.item_name)
            self.button_prio.setText('')
            self.list_widget.update_other_buttons()

        if self.item_name in self.list_widget.unprio_items:
            self.list_widget.unprio_items.remove(self.item_name)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.parallel_timer = QTimer()
        self.parallel_timer.setInterval(100)
        self.parallel_timer.timeout.connect(self.audio_prioritizer)
        self.parallel_timer.start()

        self.layout = QVBoxLayout(self)

        self.close_button = QPushButton('X')
        self.close_button.setStyleSheet("QPushButton:hover {color: #D32F2F;};")
        self.close_button.clicked.connect(self.hide_to_tray)

        self.title_layout = QHBoxLayout()
        self.title_layout.addWidget(QLabel('AudioPrioritizer'))
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button)

        self.layout.addLayout(self.title_layout)

        self.line_header = QFrame()
        self.line_header.setFrameShape(QFrame.HLine)
        self.line_header.setFrameShadow(QFrame.Sunken)
        self.line_header.setStyleSheet("background-color: #2b2b2b;")

        self.layout.addWidget(self.line_header)

        self.list_widget = UnselectableListWidget(self)

        self.layout.addWidget(self.list_widget)

        self.line_footer = QFrame()
        self.line_footer.setFrameShape(QFrame.HLine)
        self.line_footer.setFrameShadow(QFrame.Sunken)
        self.line_footer.setStyleSheet("background-color: #2b2b2b;")

        self.layout.addWidget(self.line_footer)

        self.slider_label = QLabel('Mute level:', self)

        self.mute_level_value = QLabel('0.10', self)
        self.mute_level_value.setStyleSheet('color: #3388FF;')

        self.slider_label_layout = QHBoxLayout(self)
        self.slider_label_layout.addWidget(self.slider_label)
        self.slider_label_layout.addWidget(self.mute_level_value)
        self.slider_label_layout.setAlignment(Qt.AlignLeft)

        self.layout.addLayout(self.slider_label_layout)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1000)
        self.slider.setStyleSheet("QSlider::groove:horizontal {height: 8px; border-radius: 4px; background-color: #3d3d3d;} QSlider::handle:horizontal {width: 9px; height: 9px; border-radius: 3px; background-color: #fff;} QSlider::handle:horizontal:hover {background-color: #3388FF;}")
        self.slider.valueChanged.connect(self.update_slider_label)

        self.layout.addWidget(self.slider)

        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(QCoreApplication.instance().quit)

        self.icon_pixmap = QPixmap()
        self.icon_pixmap.loadFromData(base64.b64decode(icon_data))

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.icon_pixmap))

        self.tray_menu = QMenu(self)
        self.tray_menu.addAction(self.quit_action)
        self.tray_menu.setStyleSheet("QMenu::item:selected {background-color: #2b2b2b;}")

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowTitle('AudioPrioritizer')
        self.setStyleSheet("color: white; background-color: #1e1e1e; border: none; outline: none;")
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon(self.icon_pixmap))

        self.setMouseTracking(True)
        self.drag_pos = None

    def update_slider_label(self, value):
        self.mute_level_value.setText('{:.2f}'.format(value / 100))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.drag_pos is not None:
            self.move(self.mapToGlobal(event.pos()) - self.drag_pos + self.pos())
            self.drag_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = None

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()
            self.tray_icon.hide()

    def hide_to_tray(self):
        self.hide()
        self.tray_icon.show()

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.tray_icon.hide()
            event.accept()
        else:
            event.ignore()

    def nativeEvent(self, event_type, message):
        if event_type == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())

            if int(msg.message) == 536 and msg.wParam == 4:
                if self.parallel_timer.isActive():
                    self.parallel_timer.stop()

            elif int(msg.message) == 536 and msg.wParam == 18:
                if not self.parallel_timer.isActive():
                    self.parallel_timer.start()

        return super().nativeEvent(event_type, message)

    def audio_prioritizer(self):
        sessions = AudioUtilities.GetAllSessions()

        for session in sessions:
            if session.Process:
                p_name = session.Process.name()

                # reg
                if p_name not in self.list_widget.items:
                    item, widget = QListWidgetItem(), ItemWidget(p_name, self.list_widget, self)
                    item.setSizeHint(widget.sizeHint())
                    self.list_widget.addItem(item)
                    self.list_widget.setItemWidget(item, widget)

                    self.list_widget.items[p_name] = {}
                    self.list_widget.items[p_name]['widget'] = widget
                    self.list_widget.items[p_name]['session'] = session
                    self.list_widget.items[p_name]['is_playing'] = False
                    self.list_widget.items[p_name]['muted'] = False
                    self.list_widget.items[p_name]['actual_sound'] = -1
                    self.list_widget.items[p_name]['user_max_level'] = -1
                    self.list_widget.items[p_name]['reg_time'] = datetime.datetime.now().timestamp()

        # update
        for name in list(self.list_widget.items):
            volume = self.list_widget.items[name]['session']._ctl.QueryInterface(IAudioMeterInformation)
            self.list_widget.items[name]['is_playing'] = self.list_widget.items[name]['actual_sound'] > 0
            self.list_widget.items[name]['actual_sound'] = volume.GetPeakValue()
            if not self.list_widget.items[name]['muted']:
                volume = self.list_widget.items[name]['session']._ctl.QueryInterface(ISimpleAudioVolume)
                self.list_widget.items[name]['user_max_level'] = volume.GetMasterVolume()

                # delete forgotten processes
                if name not in self.list_widget.prio_items and name not in self.list_widget.totalmute_items:
                    if self.list_widget.items[name]['reg_time'] + 5*60 < datetime.datetime.now().timestamp():
                        del self.list_widget.items[name]
                        self.list_widget.remove_item(name)

        # mute unprio
        if self.list_widget.is_prio_playing():
            for name in self.list_widget.items:
                volume = self.list_widget.items[name]['session']._ctl.QueryInterface(ISimpleAudioVolume)
                if name not in self.list_widget.prio_items:
                    if name not in self.list_widget.totalmute_items:
                        if volume.GetMasterVolume != self.slider.value()/100:
                            volume.SetMasterVolume((self.slider.value()/100), None)
                            self.list_widget.items[name]['muted'] = True
                elif len(self.list_widget.prio_items) > 1:
                    if self.list_widget.is_lower_prio(name):
                        if volume.GetMasterVolume != self.slider.value()/100:
                            volume.SetMasterVolume((self.slider.value()/100), None)
                            self.list_widget.items[name]['muted'] = True
                else:
                    if volume.GetMasterVolume != self.list_widget.items[name]['user_max_level']:
                        volume.SetMasterVolume(self.list_widget.items[name]['user_max_level'], None)
                        self.list_widget.items[name]['muted'] = False
        else:
            for name in self.list_widget.items:
                if name not in self.list_widget.totalmute_items:
                    volume = self.list_widget.items[name]['session']._ctl.QueryInterface(ISimpleAudioVolume)
                    if volume.GetMasterVolume != self.list_widget.items[name]['user_max_level']:
                        volume.SetMasterVolume(self.list_widget.items[name]['user_max_level'], None)
                        self.list_widget.items[name]['muted'] = False

        # total mute
        if self.list_widget.totalmute_items:
            if self.list_widget.is_any_playing():
                for name in self.list_widget.totalmute_items:
                    volume = self.list_widget.items[name]['session']._ctl.QueryInterface(ISimpleAudioVolume)
                    if volume.GetMasterVolume != self.slider.value()/100:
                        volume.SetMasterVolume((self.slider.value()/100), None)
                        self.list_widget.items[name]['muted'] = True
            else:
                for name in self.list_widget.totalmute_items:
                    volume = self.list_widget.items[name]['session']._ctl.QueryInterface(ISimpleAudioVolume)
                    if volume.GetMasterVolume != self.list_widget.items[name]['user_max_level']:
                        volume.SetMasterVolume(self.list_widget.items[name]['user_max_level'], None)
                        self.list_widget.items[name]['muted'] = False


def terminal_kill_handler(_, __):
    QCoreApplication.instance().quit()


if __name__ == '__main__':
    # Singleton (only 1 application)
    try:
        me = singleton.SingleInstance()
    except Exception as e:
        exit()

    # Detect terminal kill
    signal.signal(signal.SIGINT, terminal_kill_handler)

    # Main window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Start
    sys.exit(app.exec_())
