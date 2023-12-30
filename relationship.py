from dataclasses import dataclass, field


@dataclass
class Relationship:
    sentiment: float = 0
    trust: float = 0
    convo_history: list = field(default_factory=list)
    event_history: list = field(default_factory=list)
    player: "Player" = field(default_factory=None)

    def increase_sentiment(self):
        self.sentiment += 1

    def decrease_sentiment(self):
        self.sentiment -= 1

    def increase_trust(self):
        self.trust += 1

    def decrease_trust(self):
        self.trust -= 1

    def add_convo(self, dialog: str):
        """
        Adds dialog to convo history.
        """
        self.convo_history.append(dialog)

    def add_event(self, event: str):
        """
        Adds event to event history.
        """
        self.event_history.append(event)
