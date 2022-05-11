from Lib.ULSensor_maynard import distance


class ULSensor(object):
    """
    UL class
    """

    

    def __init__(self):
        self.current_read = 0  # current reading

    def read_data(self):
        self.current_read = distance()
       
        return self.current_read
