from .visual_node import VisualNode
import sys
sys.path.append("..")
from coffee import COFFEE, types


class GenreVisualNode(VisualNode):
    def __init__(self, genre, name, oxidation, caffeine_content, type, additives=True, *args, **kwargs):
        self.genre = genre
        self.additives = 1 if additives else 0
        self.name = name
        self.type = type
        self.oxidation = oxidation
        self.caffeine_content = caffeine_content
        super().__init__(val=name, *args, **kwargs)

    @property
    def caffein(self) -> str:
        if self.caffeine_content < 50 and self.caffeine_content >= 0:
            return 'low'
        elif self.caffeine_content < 100 and self.caffeine_content >= 50:
            return 'average'
        elif self.caffeine_content >= 100:
            return 'high'
        else:
            raise ValueError('caffeine_content must be > 0')

    @property
    def values_str(self):
        attributes = []
        attributes.append(self.genre.upper())
        additive = 'additives' if self.additives == 1 else 'not_additives'
        attributes.append(additive)
        attributes.append(self.name)
        attributes.append(self.type)
        attributes.append(str(self.oxidation))
        attributes.append(self.caffein)
        return ' '.join(attributes)
    
    @property
    def values_coffee(self):
        attributes = []
        attributes.append(self.genre.upper())
        additive = 'additives' if self.additives == 1 else 'not_additives'
        attributes.append(additive)
        attributes.append(self.name)
        attributes.append(self.type)
        attributes.append(str(self.oxidation))
        attributes.append(self.caffein)
        return attributes

    @property
    def countable_attributes(self) -> dict:
        attributes = {}
        additive = (self.additives + 1) / 2
        attributes.update({'additive': additive})
        assert self.name in COFFEE
        name = COFFEE.index(self.name) / len(COFFEE)
        attributes.update({'name': name})
        assert self.type in types
        type = types.index(self.type) / len(types)
        attributes.update({'type': type})
        oxidation = self.oxidation / 100
        attributes.update({'oxidation': oxidation})
        if self.caffeine_content > 100:
            caffein = 3
        elif self.caffeine_content < 100 and self.caffeine_content >= 50:
            caffein = 2
        else:
            caffein = 1
        caffein = caffein / 3
        attributes.update({'caffein': caffein})
        return attributes
