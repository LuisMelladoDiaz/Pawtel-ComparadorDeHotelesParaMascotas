import random

from rest_framework.decorators import api_view
from rest_framework.response import Response

PETS = [
    {
        "id": 1,
        "name": "Buddy",
        "species": "Dog",
        "image": "https://placedog.net/500?id=1",
    },
    {
        "id": 2,
        "name": "Mittens",
        "species": "Cat",
        "image": "https://loremflickr.com/500/500/cat?random=2",
    },
    {
        "id": 3,
        "name": "Charlie",
        "species": "Parrot",
        "image": "https://loremflickr.com/500/500/parrot?random=3",
    },
    {
        "id": 4,
        "name": "Luna",
        "species": "Rabbit",
        "image": "https://loremflickr.com/500/500/rabbit?random=4",
    },
    {
        "id": 5,
        "name": "Goldie",
        "species": "Fish",
        "image": "https://loremflickr.com/500/500/fish?random=5",
    },
    {
        "id": 6,
        "name": "Max",
        "species": "Dog",
        "image": "https://placedog.net/500?id=6",
    },
    {
        "id": 7,
        "name": "Whiskers",
        "species": "Cat",
        "image": "https://loremflickr.com/500/500/cat?random=7",
    },
    {
        "id": 8,
        "name": "Polly",
        "species": "Parrot",
        "image": "https://loremflickr.com/500/500/parrot?random=8",
    },
    {
        "id": 9,
        "name": "Thumper",
        "species": "Rabbit",
        "image": "https://loremflickr.com/500/500/rabbit?random=9",
    },
    {
        "id": 10,
        "name": "Bubbles",
        "species": "Fish",
        "image": "https://loremflickr.com/500/500/fish?random=10",
    },
]


@api_view(["GET"])
def random_pets(request):
    count = int(request.query_params.get("count", len(PETS)))
    indices = [random.randint(0, len(PETS) - 1) for _ in range(count)]
    return Response([PETS[i] for i in indices])
