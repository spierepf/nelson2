from mpf.system.mode import Mode
import copy

class CarouselItem:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<CarouselItem: " + self.name + ">"

class CarouselSelect(Mode):
    def mode_init(self):
        self.items = [CarouselItem('carousel_1'), CarouselItem('carousel_2'), CarouselItem('carousel_3')]
        self.next_item_events = ['sw_carousel_next_item']
        self.select_item_events = ['sw_carousel_select_item', 'balldevice_plunger_lane_ball_left']

    def mode_start(self, **kwargs):
        self.log.info("Carousel Mode Starting")

        self.register_handlers(self.next_item_events, self.next_item)
        self.register_handlers(self.select_item_events, self.select_item)

        player = self.machine.game.player
        if not player.is_player_var('available_modes') or player['available_modes'] == None or player['available_modes'] == []:
            self.log.info("Available modes: " + str(self.items))
            player.available_modes = copy.copy(self.items)
        player.highlighted_mode_index = 0

        self.update_highlighted_mode()

    def mode_stop(self, **kwargs):
        self.log.info("Carousel Mode Stopping")

        self.deregister_handlers(self.next_item_events, self.next_item)
        self.deregister_handlers(self.select_item_events, self.select_item)

    def register_handlers(self, events, handler):
        for event in events:
            self.machine.events.add_handler(event, handler)

    def deregister_handlers(self, events, handler):
        for event in events:
            self.machine.events.remove_handler_by_event(event, handler)

    def highlighted_mode(self):
        player = self.machine.game.player
        return player.available_modes[player.highlighted_mode_index]

    def release_current_mode(self):
        self.log.info("Releasing mode: " + str(self.highlighted_mode()))
        self.machine.events.post(self.highlighted_mode().name + "_unhighlighted")

    def update_highlighted_mode(self):
        self.log.info("Highlighted mode: " + str(self.highlighted_mode()))
        self.machine.events.post(self.highlighted_mode().name + "_highlighted")

    def next_item(self, **kwargs):
        player = self.machine.game.player

        self.release_current_mode()
        
        player.highlighted_mode_index += 1
        if player.highlighted_mode_index >= len(player.available_modes):
            player.highlighted_mode_index = 0

        self.update_highlighted_mode()

    def select_item(self, **kwargs):
        self.log.info("Selected mode: " + str(self.highlighted_mode()))

        self.machine.events.post(self.highlighted_mode().name + "_selected")
        self.machine.events.post("carousel_mode_selected")
