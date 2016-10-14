from mpf.system.mode import Mode
from mpf.system.timing import Timer

class VendorBumper:
    def __init__(self, machine, variable_name, hit_color, flash_color, leds):
        self.machine = machine
        self.variable_name = variable_name
        self.hit_color = hit_color
        self.flash_color = flash_color
        self.leds = leds
        self.on = False
        self.reset()

    def reset(self):
        for led in self.leds:
            led.color([0,0,0])

    def update(self):
        player = self.machine.game.player
        count = player[self.variable_name]

        for i in range(0, count):
            self.leds[i].color(self.hit_color)

        self.on = not self.on
        for i in range(count, len(self.leds)):
            if(self.on):
                self.leds[i].color(self.flash_color)
            else:
            	self.leds[i].color([0, 0, 0])

class vendor(Mode):
    def mode_init(self):
        self.timer = Timer(callback=self.tick, frequency=1.0/5.0)

        self.left_bumper = VendorBumper(self.machine, "pop_bumper_left_hits_count", [255, 255, 0], [255/3, 255/3, 0/3], [
                                self.machine.leds['l_pop_bumper_left_a'],
                                self.machine.leds['l_pop_bumper_left_b'],
                                self.machine.leds['l_pop_bumper_left_c'],
                                self.machine.leds['l_pop_bumper_left_d'],
                                self.machine.leds['l_pop_bumper_left_e'],
                                self.machine.leds['l_pop_bumper_left_f'],
                                self.machine.leds['l_pop_bumper_left_g'],
                                self.machine.leds['l_pop_bumper_left_h'],
                                self.machine.leds['l_pop_bumper_left_i'],
                                self.machine.leds['l_pop_bumper_left_j'],
                                self.machine.leds['l_pop_bumper_left_k'],
                                self.machine.leds['l_pop_bumper_left_l'],
                            ])

        self.right_bumper = VendorBumper(self.machine, "pop_bumper_right_hits_count", [255, 255, 0], [255/3, 255/3, 0/3], [
                                self.machine.leds['l_pop_bumper_right_a'],
                                self.machine.leds['l_pop_bumper_right_b'],
                                self.machine.leds['l_pop_bumper_right_c'],
                                self.machine.leds['l_pop_bumper_right_d'],
                                self.machine.leds['l_pop_bumper_right_e'],
                                self.machine.leds['l_pop_bumper_right_f'],
                                self.machine.leds['l_pop_bumper_right_g'],
                                self.machine.leds['l_pop_bumper_right_h'],
                                self.machine.leds['l_pop_bumper_right_i'],
                                self.machine.leds['l_pop_bumper_right_j'],
                                self.machine.leds['l_pop_bumper_right_k'],
                                self.machine.leds['l_pop_bumper_right_l'],
                            ])

        self.bottom_bumper = VendorBumper(self.machine, "pop_bumper_bottom_hits_count", [255, 255, 0], [255/3, 255/3, 0/3], [
                                self.machine.leds['l_pop_bumper_bottom_a'],
                                self.machine.leds['l_pop_bumper_bottom_b'],
                                self.machine.leds['l_pop_bumper_bottom_c'],
                                self.machine.leds['l_pop_bumper_bottom_d'],
                                self.machine.leds['l_pop_bumper_bottom_e'],
                                self.machine.leds['l_pop_bumper_bottom_f'],
                                self.machine.leds['l_pop_bumper_bottom_g'],
                                self.machine.leds['l_pop_bumper_bottom_h'],
                                self.machine.leds['l_pop_bumper_bottom_i'],
                                self.machine.leds['l_pop_bumper_bottom_j'],
                                self.machine.leds['l_pop_bumper_bottom_k'],
                                self.machine.leds['l_pop_bumper_bottom_l'],
                            ])

    def mode_start(self, **kwargs):
        self.machine.timing.add(self.timer)

    def mode_stop(self, **kwargs):
        self.machine.timing.remove(self.timer)
        self.left_bumper.reset()
        self.right_bumper.reset()
        self.bottom_bumper.reset()

    def tick(self, **kwargs):
        if self.machine.game == None:
            self.log.info("Vendors.tick() called outside game")
            self.machine.timing.remove(self.timer)
        else:
            self.left_bumper.update()
            self.right_bumper.update()
            self.bottom_bumper.update()
