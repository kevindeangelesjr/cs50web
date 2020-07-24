people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"}
]


#def f(person):
#    return person["name"]

### Lambda - represent short one line function
# This lambda replaces above function
people.sort(key=lambda person: person["name"])

print(people)