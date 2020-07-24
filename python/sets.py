### sets are unordered, no element can appear more than once (every element must be unique)

# Create empty set
s = set()

# add elements to set
s.add(1)
s.add(2)
s.add(3)
s.add(4)
print(s)
s.add(2)
print(s)

s.remove(2)
print(s)

print(len(s))