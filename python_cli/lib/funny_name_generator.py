import random

adjectives = [
    "rapid",
    "blazing",
    "swift",
    "speedy",
    "quick",
    "fast",
    "hasty",
    "lightning",
    "flying",
    "rushing",
]
nouns = [
    "rocket",
    "cheetah",
    "sports car",
    "bullet",
    "jet",
    "motorcycle",
    "speedboat",
    "racehorse",
    "sprinter",
    "falcon",
]


def generate_name():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{adjective} {noun}"
