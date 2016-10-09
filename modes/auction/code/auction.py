from mpf.system.mode import Mode
from mpf.system.timing import Timer

class auction(Mode):
    def mode_init(self):
        self.timer = Timer(callback=self.tick, frequency=1.0/5.0)

        self.player_bid_leds = [
            self.machine.leds['l_player_bid_a'],
            self.machine.leds['l_player_bid_b'],
            self.machine.leds['l_player_bid_c'],
            self.machine.leds['l_player_bid_d'],
            self.machine.leds['l_player_bid_e'],
            self.machine.leds['l_player_bid_f'],
            self.machine.leds['l_player_bid_g'],
            self.machine.leds['l_player_bid_h']
        ]

        self.opponent_bid_leds = [
            self.machine.leds['l_opponent_bid_a'],
            self.machine.leds['l_opponent_bid_b'],
            self.machine.leds['l_opponent_bid_c'],
            self.machine.leds['l_opponent_bid_d'],
            self.machine.leds['l_opponent_bid_e'],
            self.machine.leds['l_opponent_bid_f'],
            self.machine.leds['l_opponent_bid_g'],
            self.machine.leds['l_opponent_bid_h']
        ]

    def mode_start(self, **kwargs):
        self.machine.timing.add(self.timer)
        self.last_bid = 0

    def mode_stop(self, **kwargs):
        self.fill_bar(self.player_bid_leds, 0, [0,0,0])
        self.fill_bar(self.opponent_bid_leds, 0, [0,0,0])
        self.machine.timing.remove(self.timer)

    def fill_bar(self, leds, fg_count, fg, bg=[0,0,0]):
        for i in range(0, len(leds)):
            leds[i].color(fg if i < fg_count else bg)

    def update_bid(self, bid):
        if bid > self.last_bid:
            self.last_bid = bid
            self.machine.events.post("auction_bid_{}".format(self.last_bid))

    def tick(self, **kwargs):
        if self.machine.game == None:
            self.log.info("Auction.tick() called outside game")
            self.machine.timing.remove(self.timer)
        else:
            player = self.machine.game.player

            max_player_bid = float(self.config["logic_blocks"]["counters"]["player_bid"]["count_complete_value"])
            fg_count = int(len(self.player_bid_leds) * min(1.0, player["player_bid_count"] / max_player_bid))
            self.fill_bar(self.player_bid_leds, fg_count, [0, 255, 0])
            self.update_bid(fg_count)

            max_opponent_bid = float(self.config["timers"]["opponent_bid"]["end_value"])
            fg_count = int(len(self.opponent_bid_leds) * min(1.0, player["auction_opponent_bid_tick"] / max_opponent_bid))
            self.fill_bar(self.opponent_bid_leds, fg_count, [255, 0, 255])
            self.update_bid(fg_count)
