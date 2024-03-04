import keyboard

class GlobalShortcuts:
    def __init__(self, main_page):
        self.main_page = main_page
        keyboard.add_hotkey('page up', self.on_previous_song)
        keyboard.add_hotkey('page down', self.on_next_song)
        keyboard.add_hotkey('up', self.on_volume_up)
        keyboard.add_hotkey('down', self.on_volume_down)
        keyboard.add_hotkey('ctrl+alt+up', self.small)

    def on_previous_song(self):
        self.main_page.previous_song()

    def on_next_song(self):
        self.main_page.next_song()

    def on_volume_up(self):
        self.main_page.TurnUpTheVolume()

    def on_volume_down(self):
        self.main_page.TurnDownVolume()

    def start(self):
        pass  # Not needed for keyboard library

    def stop(self):
        keyboard.clear_all_hotkeys()

    def small(self):
        try:
            self.main_page.small_page()
        except Exception as e:
            print(f"small: {e}")
