from dataclasses import dataclass, field


@dataclass
class Relationship:
    sentiment: float = 0
    trust: float = 0
    player: "Player" = field(default_factory=None)

    def increase_sentiment(self):
        self.sentiment += 1

    def decrease_sentiment(self):
        self.sentiment -= 1

    def increase_trust(self):
        self.trust += 1

    def decrease_trust(self):
        self.trust -= 1
