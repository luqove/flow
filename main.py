import sys

import time
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QMutex
from PyQt5.QtWidgets import QApplication, QMainWindow

from MaskUi import Ui_MainWindow
from mask_main import MaskSystem

mutex = QMutex()


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    main window
    """

    # Initialize 
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # connection slot function
        # button
        self.Clear_status_btn.clicked.connect(self.clear_feedback_bro)

        self.Demo_btn.clicked.connect(self.start_mask_mech)
        self.Stop_Demo_btn.clicked.connect(self.stop_mask_mech)

        # menu
        self.actionRefill_mask.triggered.connect(lambda: self.set_mask_num(50))
        self.actionEmpty_mask.triggered.connect(lambda: self.set_mask_num(0))
        self.actionRemove_1mask.triggered.connect(lambda: self.mask_num_decrease_by(1))
        self.actionRemove_50mask.triggered.connect(lambda: self.mask_num_decrease_by(50))
        self.actionAdd_1mask.triggered.connect(lambda: self.mask_num_increase_by(1))
        self.actionAdd_50mask.triggered.connect(lambda: self.mask_num_increase_by(50))

    # Each call, reduce the corresponding number of masks
    # num_decrease is the amount to be reduced
    def mask_num_decrease_by(self, num):
        mask_number = int(self.Mask_number_bro.toPlainText())
        mask_number -= num
        self.set_mask_num(mask_number)
        
        # if mask_number == 0:
        #     if hasattr(self, 'timer'):
        #         mutex.lock()
        #         self.timer.requestInterruption()
        #         self.timer.quit()
        #         mutex.unlock()
        #         del self.timer

    # Add the number of masks
    def mask_num_increase_by(self, num):
        mask_number = int(self.Mask_number_bro.toPlainText())
        mask_number += num
        self.set_mask_num(mask_number)

    # is empty
    def empty_feedback(self):
        self.Feedback_bro.append(">>is empty\n")

    # error
    def error_occor(self):
        self.Feedback_bro.append(">>dispenser failure\n")

    # display messafe
    def display_msg(self, string):
        self.Feedback_bro.append(string)

    # Set the number of masks in the mask machine
    # The current maximum number is 9999
    def set_mask_num(self, num):
        if num == 0:
            self.empty_feedback()
      
        elif num < 0 or num > 9999:
            self.error_occor()
            return
        
        display = str(num)
        if len(str(num)) <= 4:
            for a in range(4 - len(str(num))):
                display = "0" + display
        self.Mask_number_bro.setText(display)
        self.Mask_number_bro.setAlignment(Qt.AlignCenter)

    def clear_feedback_bro(self):
        self.Feedback_bro.clear()

    # main thread
    def start_mask_mech(self):
        self.mask_system = MaskSystem()
        self.timer.timer_signal[int].connect(self.set_mask_num)
        self.mask_system.msg_signal[str].connect(self.display_msg)
        self.mask_system.start()

    # end main thread
    def stop_mask_mech(self):
        if hasattr(self, "mask_system"):
            mutex.lock()
            self.mask_system.requestInterruption()
            self.mask_system.quit()
            mutex.unlock()
            del self.mask_system

    # Demo empty
    # TODO Here is the Demo demo, delete it later
    def demo(self):
        self.timer = TimerCount(0.1)
        self.timer.timer_signal.connect(lambda: self.mask_num_decrease_by(1))
        self.timer.start()


class TimerCount(QThread):

    timer_signal = pyqtSignal()

    def __init__(self, time_gap):
        super(TimerCount, self).__init__()
        self.time_gap = time_gap
    
    def run(self):
        while not(self.isInterruptionRequested()):
            time.sleep(self.time_gap)
            self.timer_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
