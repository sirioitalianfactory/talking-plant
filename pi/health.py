"""Plant profiles and deterministic health evaluation (illustrative ranges)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Profile:
    name: str
    soil: tuple[float, float]
    light: tuple[float, float]
    temperature: tuple[float, float]

PROFILES = (
    Profile("Monstera", (35, 65), (300, 800), (18, 28)),
    Profile("Snake Plant", (20, 45), (150, 700), (16, 30)),
    Profile("Fiddle-leaf Fig", (40, 60), (400, 900), (18, 27)),
)

def metric(value: float, bounds: tuple[float, float]) -> str:
    low, high = bounds
    if low > high:
        raise ValueError("Invalid profile bounds")
    if low <= value <= high:
        return "good"
    tolerance = (high - low) * 0.15
    if low - tolerance <= value <= high + tolerance:
        return "warn"
    return "bad"

def evaluate(soil: float, light: float, temperature: float, profile: Profile):
    states = {
        "soil": metric(soil, profile.soil),
        "light": metric(light, profile.light),
        "temperature": metric(temperature, profile.temperature),
    }
    bad = sum(state == "bad" for state in states.values())
    warn = sum(state == "warn" for state in states.values())
    mood = ("sad" if bad >= 2 else "worried" if bad == 1 or warn >= 2
            else "neutral" if warn else "happy")
    return mood, states
