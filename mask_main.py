from system_lib import *
from PyQt5.QtCore import pyqtSignal, QThread, QMutex


class MaskSystem(QThread):
    """
    main thread
    """

    msg_signal = pyqtSignal(str)
    mask_dispense_signal = pyqtSignal(int)

    def __init__(self):
        super(MaskSystem, self).__init__()
        self.system = System()

    def run(self):

        while not self.isInterruptionRequested():
            if self.system.reset_button.is_pushed():
                self.system.reset()

            # check tray is empty
            if self.system.is_mask_tray_empty():
                self.system.report_empty()
                self.system.HALT()
                
                continue

            self.system.display_stack_level()

            if self.system.is_mask_in_transit():
                self.system.report_fault()
                self.system.HALT()
               
                continue
            else:
                self.system.turn_on_led(LED_READY)
                # The mask machine is started, waiting for the customer to issue a mask request
                self.system.wait_request()

            # Here it means that a customer has come to the door
            self.system.dispensing_mask()
            
            # maybe time.sleep()

            # Check if the mask has been removed from the stack correctly
            if not self.system.is_mask_in_waiting_position():
                self.system.report_fault()
                self.system.HALT()
                
                continue

            # Hand out the mask and wait until
            self.system.release_mask_partially_and_wait()

            # Detect if the mask has been taken by the guest, and if not, force the mask to be pushed out completely
            if self.system.is_mask_still_waiting_collection():
                self.system.release_mask_totally()
               
                # maybe time.sleep()
                
            if self.system.is_mask_still_waiting_collection():
                self.system.report_fault()
                self.system.HALT()
                
                continue

            # Close the door, and send data to the GUI
            self.system.close_door()
            self.system.stack_count -= 1
            self.send_mask_dispensed()
            self.send_msg("dispensed mask")
            self.system.reset_report_led()
            
            # maybe time.sleep()

    def send_mask_dispensed(self):
        self.mask_dispense_signal.emit(self.system.stack_count)

    def send_msg(self, string):
        self.msg_signal.emit(string)
