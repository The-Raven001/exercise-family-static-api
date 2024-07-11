
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        self.members = []

    def generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        if "id" not in member:
            member["id"] = self.generateId()
        member["last_name"] = self.last_name
        self.members.append(member)

    def delete_member(self, id):
        self.members = [member for member in self.members if member["id"] != id]
        return {"done": True}

    def update_member(self, id, updated_member):
        for member in self.members:
            if member["id"] == id:
                member.update(updated_member)
                member["id"] = id
                member["last_name"] = self.last_name
                break

    def get_member(self, id):
        for member in self.members:
            if member["id"] == id:
                return member
        return None

    def get_all_members(self):
        return self.members