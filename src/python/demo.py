from collections import Counter

with open("i.txt") as file:
    v = list(map(int, file.readlines()))

print("p1", sum(v))
print("p2", int(round(sum(v) / len(v))))

c = Counter(v)

cc = Counter()
for n in v:
    cc.update(list(str(n)))

print("p3", f"{c.most_common(1)[0][0]}{sorted(cc.items(), key=lambda x: x[-1])[0][0]}")
