class TravelMemory:
    def __init__(self):
        self.preferences = {}

    def save_preferences(self, preferences):
        self.preferences.update(preferences)

    def get_preferences(self):
        return self.preferences

    def clear(self):
        self.preferences = {}