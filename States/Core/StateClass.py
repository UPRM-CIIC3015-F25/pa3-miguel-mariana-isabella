import pygame
from abc import ABC, abstractmethod

from Deck.DeckManager import DeckManager

# DO NOT TOUCH THIS FILE

# ---------- Abstract State Class ----------
class State(ABC):
    deckManager = DeckManager()
    screen = None
    screenshot = None
    @classmethod
    def set_screen(cls, screen: pygame.Surface):
        cls.screen = screen
    def __init__(self, next_state: str = ""):
        self.nextState = next_state
        self.isFinished = False
        self.buttonSound =pygame.mixer.Sound('Graphics/Sounds/buttonSound.mp3')

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def userinput(self, events):
        pass