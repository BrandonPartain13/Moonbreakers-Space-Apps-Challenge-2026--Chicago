class Rocket:
    name = ""
    price_tier = ""

    def aircraft_price(self, prices_by_tier):
        return prices_by_tier[self.price_tier]


class CheapRocket(Rocket):
    name = "Falcon Heavy"
    price_tier = "cheap"
    price = 150_000_000
    tank_count = 4
    max_dry_mass_kg = 22_800


class MediumRocket(Rocket):
    name = "New Glenn"
    price_tier = "medium"
    price = 110_000_000
    tank_count = 2
    max_dry_mass_kg = 45_000


class ExpensiveRocket(Rocket):
    name = "Orion"
    price_tier = "expensive"
    price = 2_500_000_000
    tank_count = 4
    max_dry_mass_kg = 35_800
