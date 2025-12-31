from Person_node import Person


class FamilyTree:
    def __init__(self):
        self.people = {}

    def add_person(self, name, gender):
        if name in self.people:
            raise ValueError("Person already exists in tree")
        person = Person(name, gender)
        self.people[name] = person
        return person

    def get_person(self, name):
        if name not in self.people:
            raise ValueError(f"{name} Person not found in tree")
        return self.people[name]

    def set_father(self, child_name, father_name):
        child = self.get_person(child_name)
        father = self.get_person(father_name)
        child.set_father(father)

    def set_mother(self, child_name, mother_name):
        child = self.get_person(child_name)
        mother = self.get_person(mother_name)
        child.set_mother(mother)

    def find_path(self, start_name, target_name):
        start_person = self.get_person(start_name)
        target_person = self.get_person(target_name)
        visited = set()
        path = []

        def dfs(person):
            if person in visited:
                return False
            
            visited.add(person)

            if person == target_person:
                return True

            if person.father:
                path.append('father')
                if dfs(person.father):
                    return True
                path.pop()
                
            if person.mother:
                path.append('mother')
                if dfs(person.mother):
                    return True
                path.pop()

            for child in person.children:
                if child.gender == 'female':
                    path.append('daughter')
                else:
                    path.append('son')
                
                if dfs(child):
                    return True
                path.pop()
                        
            return False

        if dfs(start_person):
            return path
        else:
            return None

    def to_dict(self):
        return {name: person.to_dict() for name, person in self.people.items()}
