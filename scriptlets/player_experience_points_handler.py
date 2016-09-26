from mpf.system.scriptlet import Scriptlet
from mpf.system.timing import Timer

import math

class PlayerExperiencePointsHandler(Scriptlet):
    def on_load(self):
        self.experience_point_value = 1000
        self.experience_point_multipliers = [1, 2, 3, 5]

        self.xp_bar_leds = [
            self.machine.leds['l_xp_bar_a'],
            self.machine.leds['l_xp_bar_b'],
            self.machine.leds['l_xp_bar_c'],
            self.machine.leds['l_xp_bar_d'],
            self.machine.leds['l_xp_bar_e'],
            self.machine.leds['l_xp_bar_f'],
            self.machine.leds['l_xp_bar_g'],
            self.machine.leds['l_xp_bar_h']
        ]

        self.xp_bar_colours = [
            [255, 0, 0],        # RED
            [255, 127, 0],      # ORANGE
            [255, 255, 0],      # YELLOW
            [0, 255, 0],        # GREEN
            [0, 0, 255],        # BLUE
            [75, 0, 130],       # INDIGO
            [127, 0, 255]       # VIOLET
        ]

        self.xp_multiplier_leds = [
            [
                self.machine.leds['l_xp_multiplier_2_a'],
                self.machine.leds['l_xp_multiplier_2_b'],
                self.machine.leds['l_xp_multiplier_2_c'],
                self.machine.leds['l_xp_multiplier_2_d'],
                self.machine.leds['l_xp_multiplier_2_e'],
                self.machine.leds['l_xp_multiplier_2_f'],
                self.machine.leds['l_xp_multiplier_2_g']
            ],
            [
                self.machine.leds['l_xp_multiplier_3_a'],
                self.machine.leds['l_xp_multiplier_3_b'],
                self.machine.leds['l_xp_multiplier_3_c'],
                self.machine.leds['l_xp_multiplier_3_d'],
                self.machine.leds['l_xp_multiplier_3_e'],
                self.machine.leds['l_xp_multiplier_3_f'],
                self.machine.leds['l_xp_multiplier_3_g']
            ],
            [
                self.machine.leds['l_xp_multiplier_5_a'],
                self.machine.leds['l_xp_multiplier_5_b'],
                self.machine.leds['l_xp_multiplier_5_c'],
                self.machine.leds['l_xp_multiplier_5_d'],
                self.machine.leds['l_xp_multiplier_5_e'],
                self.machine.leds['l_xp_multiplier_5_f'],
                self.machine.leds['l_xp_multiplier_5_g']
            ]
        ]

        self.machine.events.add_handler("award_jackpot", self.handle_award_jackpot)
        self.machine.events.add_handler("player_experience_points", self.handle_player_experience_points)
        self.machine.events.add_handler("player_experience_point_multiplier_index", self.handle_player_experience_point_multiplier_index)
        self.machine.events.add_handler("upper_lanes_complete", self.handle_upper_lanes_complete)
        self.machine.events.add_handler("count_experience_points", self.handle_count_experience_points)

        self.count_experience_points_timer = Timer(callback=self.count_experience_point, frequency=1.0/10.0)

    def fill_xp_bar(self, value):
        if value < len(self.xp_bar_leds):
            bg = [0,0,0]
            fg = self.xp_bar_colours[0]
            fg_count = value
        else:
            bg = self.xp_bar_colours[int(math.floor(value / len(self.xp_bar_leds)) - 1) % len(self.xp_bar_colours)]
            fg = self.xp_bar_colours[int(math.floor(value / len(self.xp_bar_leds))) % len(self.xp_bar_colours)]
            fg_count = value % len(self.xp_bar_leds)

        for i in range(0, len(self.xp_bar_leds)):
            self.xp_bar_leds[i].color(fg if i < fg_count else bg)

    def handle_award_jackpot(self, **kwargs):
        player = self.machine.game.player
        player.score += player.jackpot_value

    def update_jackpot_value(self):
        player = self.machine.game.player

        if not player.is_player_var('experience_points'):
            player.experience_points = 0
            self.handle_player_experience_points()

        if not player.is_player_var('experience_point_multiplier_index'):
            player.experience_points_multiplier_index = 0
            self.handle_player_experience_point_multiplier_index()

        player.jackpot_value = self.experience_point_value * player.experience_points * player.experience_point_multiplier
        self.log.info("Player Jackpot Value: {}".format(player.jackpot_value))

    def handle_player_experience_points(self, **kwargs):
        self.fill_xp_bar(self.machine.game.player.experience_points)
        self.update_jackpot_value()

    def handle_player_experience_point_multiplier_index(self, **kwargs):
        player = self.machine.game.player
        for i in range(0, len(self.xp_multiplier_leds)):
            c = [0, 255, 0] if i < player.experience_point_multiplier_index else [0, 0, 0]
            for led in self.xp_multiplier_leds[i]:
                led.color(c)
        player.experience_point_multiplier = self.experience_point_multipliers[player.experience_point_multiplier_index]
        self.update_jackpot_value()

    def handle_upper_lanes_complete(self, **kwargs):
        player = self.machine.game.player
        if player.experience_point_multiplier_index < len(self.experience_point_multipliers)-1:
            player.experience_point_multiplier_index += 1
        else:
            self.machine.events.post("award_jackpot")

    def handle_count_experience_points(self, **kwargs):
        self.log.info("Counting Experience Points")
        self.machine.timing.add(self.count_experience_points_timer)

    def count_experience_point(self):
        player = self.machine.game.player
        player.counted_experience_points += 1
        player.counted_experience_points_value += self.experience_point_value
        if player.counted_experience_points == player.experience_points:
            self.machine.timing.remove(self.count_experience_points_timer)
            self.machine.events.post("count_experience_points_complete")
