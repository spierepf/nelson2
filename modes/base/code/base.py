from mpf.system.mode import Mode
from mpf.system.timing import Timer
from mpf.devices.ball_save import BallSave

class base(Mode):
    def mode_init(self):
        self.log.info("Initializing Base Mode")
        self.extra_ball_threshold = 5000
        self.ball_save_leds = [
            self.machine.leds['l_ball_save_s'],
            self.machine.leds['l_ball_save_r'],
            self.machine.leds['l_ball_save_q'],
            self.machine.leds['l_ball_save_p'],
            self.machine.leds['l_ball_save_o'],
            self.machine.leds['l_ball_save_n'],
            self.machine.leds['l_ball_save_m'],
            self.machine.leds['l_ball_save_l'],
            self.machine.leds['l_ball_save_k'],
            self.machine.leds['l_ball_save_j'],
            self.machine.leds['l_ball_save_i'],
            self.machine.leds['l_ball_save_h'],
            self.machine.leds['l_ball_save_g'],
            self.machine.leds['l_ball_save_f'],
            self.machine.leds['l_ball_save_e'],
            self.machine.leds['l_ball_save_d'],
            self.machine.leds['l_ball_save_c'],
            self.machine.leds['l_ball_save_b'],
            self.machine.leds['l_ball_save_a'],
        ]

    def mode_start(self, **kwargs):
        self.log.info("Starting Base Mode")
        self.machine.events.add_handler('player_base_ball_save_tick', self.player_base_ball_save_tick)
        self.machine.events.add_handler('player_score', self.player_score_handler)
        for led in self.ball_save_leds:
            led.color([255, 0, 0])

    def mode_stop(self, **kwargs):
        self.log.info("Stopping Base Mode")
        self.machine.events.remove_handler_by_event('player_base_ball_save_tick', self.player_base_ball_save_tick)

    def fill_bar(self, leds, fg_count, fg, bg=[0,0,0]):
        for i in range(0, len(leds)):
            leds[i].color(fg if i < fg_count else bg)

    def player_base_ball_save_tick(self, **kwargs):
        self.fill_bar(self.ball_save_leds, kwargs['value'], [255,0,0])

    def player_score_handler(self, **kwargs):
        pass
        # if kwargs['prev_value'] < self.extra_ball_threshold and kwargs['value'] > self.extra_ball_threshold:
        #     self.machine.game.award_extra_ball()
