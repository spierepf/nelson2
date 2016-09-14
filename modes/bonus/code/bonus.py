from mpf.system.mode import Mode
from mpf.system.timing import Timer

class Bonus(Mode):
    def mode_init(self):
        self.count_experience_points_timer = Timer(callback=self.add_experience_point, frequency=1.0/10.0)
        self.apply_multiplier_timer = Timer(callback=self.apply_multiplier, frequency=1.0)
        self.compute_bonus_timer = Timer(callback=self.compute_bonus, frequency=1.0)

    def mode_start(self, **kwargs):
        self.log.info("Starting Bonus Mode")
        if not self.player.is_player_var('experience_points'):
            self.player.experience_points = 10000000

        self.player.counted_experience_points = 0
        self.player.counted_multiplier = 0
        self.player.counted_bonus = 0

        self.count_experience_points()

    def mode_stop(self, **kwargs):
        pass

    def count_experience_points(self):
        self.log.info("Counting Experience Points")
        self.machine.timing.add(self.count_experience_points_timer)

    def add_experience_point(self):
        self.player.counted_experience_points += 1000000
        self.machine.events.post("bonus_update_experience_points")
        if self.player.counted_experience_points == self.player.experience_points:
            self.machine.timing.remove(self.count_experience_points_timer)
            self.machine.timing.add(self.apply_multiplier_timer)

    def apply_multiplier(self):
        self.log.info("Applying Multiplier")
        self.player.counted_multiplier = 2
        self.machine.events.post("bonus_update_multiplier")
        self.machine.timing.remove(self.apply_multiplier_timer)
        self.machine.timing.add(self.compute_bonus_timer)

    def compute_bonus(self):
        self.log.info("Computing Bonus")
        self.player.counted_bonus = self.player.counted_multiplier * self.player.counted_experience_points
        self.machine.events.post("bonus_update_bonus")
        self.machine.timing.remove(self.compute_bonus_timer)

