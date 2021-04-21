class RGBMatrixOptions:
    def __init__(self):
        self.hardware_mapping = 'EMULATED'
        self.rows = 32
        self.cols = 32
        self.chain_length = 1
        self.parallel = 1
        self.row_address_type = 0
        self.multiplexing = 0
        self.pwm_bits = 0
        self.brightness = 100
        self.pwm_lsb_nanoseconds = 130
        self.led_rgb_sequence = 'RGB'
        self.show_refresh_rate = 0
        self.gpio_slowdown = None
        self.disable_hardware_pulsing = False

        self.pixel_size = 16
    
    def window_size(self):
        return (self.cols * self.pixel_size, self.rows * self.pixel_size)