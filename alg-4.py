
n, a0 = map(int, input().split())
friends = []
for i in range(n):
    a, b = map(int, input().split())
    friends.append((a, b, i + 1))

positive = []
non_positive = []

for a, b, idx in friends:
    if b >= 0:
        positive.append((a, b, idx))
    else:
        non_positive.append((a, b, idx))

positive.sort(key=lambda x: x[0])

non_positive.sort(key=lambda x: x[0] + x[1], reverse=True)

result = []
current_authority = a0

for a, b, idx in positive:
    if current_authority >= a:
        result.append(idx)
        current_authority += b

for a, b, idx in non_positive:
    if current_authority >= a:
        result.append(idx)
        current_authority += b

print(len(result))
if result:
    print(*result)