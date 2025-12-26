# =========================
# Person Node (Tree Node)
# =========================

class Person:
    def __init__(self, name: str, gender: str):
        """
        gender must be: 'male' or 'female'
        """
        self.name = name
        self.gender = gender
        self.father = None
        self.mother = None
        self.children = []

    def set_father(self, father):
        if self.father is not None:
            raise ValueError(f"{self.name} already has a father")
        if father.gender != 'male':
            raise ValueError(f"Father must be male")
        self.father = father
        father.children.append(self)

    def set_mother(self, mother):
        if self.mother is not None:
            raise ValueError(f"{self.name} already has a mother")
        if mother.gender != 'female':
            raise ValueError(f"Mother must be female")
        self.mother = mother
        mother.children.append(self)

    def __repr__(self):
        return f"Person(name={self.name})"


# =========================
# Family Tree Structure
# =========================

class FamilyTree:
    def __init__(self):
        self.people = {}

    # ---- Person Management ----
    def add_person(self, name: str, gender: str):
        if name in self.people:
            raise ValueError("Person already exists in tree")
        person = Person(name, gender)
        self.people[name] = person
        return person

    def get_person(self, name: str):
        if name not in self.people:
            raise ValueError("Person not found in tree")
        return self.people[name]

    # ---- Relationship Connections ----
    def set_father(self, child_name: str, father_name: str):
        child = self.get_person(child_name)
        father = self.get_person(father_name)
        child.set_father(father)

    def set_mother(self, child_name: str, mother_name: str):
        child = self.get_person(child_name)
        mother = self.get_person(mother_name)
        child.set_mother(mother)

    # ---- Utility / Debug ----
    def show_person(self, name: str):
        person = self.get_person(name)
        print(f"Name: {person.name}")
        print(f"Gender: {person.gender}")
        print(f"Father: {person.father.name if person.father else None}")
        print(f"Mother: {person.mother.name if person.mother else None}")
        print(f"Children: {[child.name for child in person.children]}")


# =========================
# Simple Test (Structure Only)
# =========================

if __name__ == "__main__":
    tree = FamilyTree()

    # Add persons
    tree.add_person("Hasan", "male")
    tree.add_person("Fatemeh", "female")
    tree.add_person("Reza", "male")
    tree.add_person("Zahra", "female")
    tree.add_person("Ali", "male")

    # Build tree
    tree.set_father("Reza", "Hasan")
    tree.set_mother("Reza", "Fatemeh")

    tree.set_father("Zahra", "Hasan")
    tree.set_mother("Zahra", "Fatemeh")

    tree.set_father("Ali", "Reza")

    # Debug output
    tree.show_person("Hasan")
    print("-----------")
    tree.show_person("Ali")