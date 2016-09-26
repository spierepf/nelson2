from mpf.system.mode import Mode

class Bonus(Mode):
    def mode_init(self):
        pass

    def mode_start(self, **kwargs):
        self.player.counted_experience_points = 0
        self.player.previous_score = self.player.score
        self.player.score += self.player.jackpot_value

        self.machine.events.post("count_experience_points")
        pass

    def mode_stop(self, **kwargs):
        pass
