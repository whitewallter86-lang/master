
n = int(input())
lectures = []
for i in range(n):
    s, f = map(int, input().split())
    lectures.append((s, f))

lectures.sort(key=lambda x: x[1])

count = 0
last_end = 0

for start, end in lectures:
    if start >= last_end:
        count += 1
        last_end = end

print(count)