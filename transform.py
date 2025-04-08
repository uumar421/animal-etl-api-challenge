from datetime import datetime, timezone

def transform_animal(animal):
    # split friends into a list
    friends = animal.get("friends", "")
    if friends:
        friends_list = [f.strip() for f in friends.split(",")]
    else:
        friends_list = []

    # convert born_at to ISO 8601 UTC format if not None
    born_at = animal.get("born_at")
    if born_at is not None:
        dt = datetime.fromtimestamp(born_at / 1000, tz=timezone.utc)
        born_at_iso = dt.isoformat()
    else:
        born_at_iso = None

    return {
        "id": animal["id"],
        "name": animal["name"],
        "friends": friends_list,
        "born_at": born_at_iso
    }