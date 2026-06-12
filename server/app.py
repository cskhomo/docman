import bcrypt

pass1 = "alan123"
pass2 = "ada123"
pass3 = "torvalds"
pass4 = "richard"


passes = []
passes.append(pass1)
passes.append(pass2)
passes.append(pass3)
passes.append(pass4)

print(passes, "\n")

hashes = []

for p in passes:
	hash = bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode('utf-8')
	print(hash)
