class Person:
    def __init__(self, name: str, gender: str):
        self.name = name
        self.gender = gender
        self.father = None
        self.mother = None
        self.children = []

    def set_father(self, father):
        if father.gender != 'male':
            raise ValueError(f"Father must be male")
        self.father = father
        if self not in father.children:
            father.children.append(self)

    def set_mother(self, mother):
        if mother.gender != 'female':
            raise ValueError(f"Mother must be female")
        self.mother = mother
        if self not in mother.children:
            mother.children.append(self)

    def to_dict(self):
        return {
            'name': self.name,
            'gender': self.gender,
            'father': self.father.name if self.father else None,
            'mother': self.mother.name if self.mother else None,
            'children': [child.name for child in self.children]
        }
