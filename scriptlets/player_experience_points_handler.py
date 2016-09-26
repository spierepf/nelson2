from mpf.system.scriptlet import Scriptlet

class PlayerExperiencePointsHandler(Scriptlet):
    def on_load(self):
        self.experience_points_multipliers = [1, 2, 3, 5]

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
        self.machine.events.add_handler("upper_lanes_complete", self.handle_upper_lanes_complete)

    def handle_award_jackpot(self, **kwargs):
    	player = self.machine.game.player
    	player.score += 1000 * player.experience_points * self.experience_points_multipliers[player.experience_points_multiplier]

    def handle_player_experience_points(self, **kwargs):
        self.log.info("handle_player_experience_points")

    def handle_upper_lanes_complete(self, **kwargs):
        player = self.machine.game.player
        if player.experience_points_multiplier < len(self.experience_points_multipliers)-1:
            player.experience_points_multiplier += 1
        else:
        	self.machine.events.post("award_jackpot")
