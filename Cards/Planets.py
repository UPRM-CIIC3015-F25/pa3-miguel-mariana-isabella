class PlanetCard:
    def __init__(self, name, description, price=6, chips=0, mult=0, image=None, isActive=False):
        self.name = name
        self.description = description
        self.price = price
        self.chips = chips
        self.mult = mult
        self.image = image
        self.isActive = isActive

    def __str__(self):
        return f"{self.name}: {self.description}"

    def sellPrice(self):
        return int(self.price * 0.6)

# TODO (TASK 6.1): Implement the Planet Card system for Balatro.
#   Create a dictionary called PLANETS that stores all available PlanetCard objects.
#   Each entry should use the planet's name as the key and a PlanetCard instance as the value.
#   Each PlanetCard must include:
#       - name: the planet's name (e.g., "Mars")
#       - description: the hand it levels up or affects
#       - price: how much it costs to purchase
#       - chips: the chip bonus it provides
#       - mult: the multiplier it applies
#   Example structure:
#       "Gusty Garden": PlanetCard("Gusty Garden", "levels up galaxy", 6, 15, 7)
#   Include all planets up to "Sun" to complete the set.
#   These cards will be used in the shop and gameplay systems to upgrade specific poker hands.

PLANETS = {
    "Mercury": PlanetCard(
        name="Mercury",
        description="Levels up High Card",
        price=4,
        chips=10,
        mult=2
    ),
    "Venus": PlanetCard(
        name="Venus",
        description="Levels up Pair",
        price=5,
        chips=12,
        mult=3
    ),

    "Earth": PlanetCard(
        name="Earth",
        description="Levels up Two Pair",
        price=5,
        chips=14,
        mult=3
    ),
    "Mars": PlanetCard(
        name="Mars",
        description="Levels up Three of a Kind",
        price=6,
        chips=15,
        mult=4
    ),
    "Jupiter": PlanetCard(
        name="Jupiter",
        description="Levels up Straight",
        price=6,
        chips=18,
        mult=4
    ),
    "Saturn": PlanetCard(
        name="Saturn",
        description="Levels up Flush",
        price=7,
        chips=20,
        mult=5
    ),
    "Uranus": PlanetCard(
        name="Uranus",
        description="Levels up Full House",
        price=7,
        chips=22,
        mult=5
    ),
    "Neptune": PlanetCard(
        name="Neptune",
        description="Levels up Four of a Kind",
        price=8,
        chips=24,
        mult=6
    ),
    "Pluto": PlanetCard(
        name="Pluto",
        description="Levels up Straight Flush",
        price=8,
        chips=28,
        mult=6
    ),
    "Sun": PlanetCard(
        name="Sun",
        description="Levels up Royal Flush",
        price=10,
        chips=35,
        mult=8
    )
}
