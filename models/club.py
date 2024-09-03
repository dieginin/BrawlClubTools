class Club:
    def __init__(self, tag: str, name: str) -> None:
        self.tag = tag
        self.name = name

    def to_dict(self) -> dict[str, str]:
        return {"tag": self.tag, "name": self.name}

    @staticmethod
    def from_dict(data) -> "Club":
        return Club(tag=data.get("tag"), name=data.get("name"))
