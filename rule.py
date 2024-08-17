from dataclasses import dataclass

@dataclass
class Rule:
    criteria: str
    colour_by: str
    colour: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            criteria = data.get('criteria'),
            colour_by = data.get('colour_by'),
            colour = data.get('colour')
        )