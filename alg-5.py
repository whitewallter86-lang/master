
n = int(input())
a = list(map(int, input().split()))
c = list(map(int, input().split()))

candies = [(a[i], c[i]) for i in range(n)]
candies.sort(key=lambda x: x[0] + x[1])

harm_level = 0
count = 0

for harm, limit in candies:
    if harm_level + harm <= limit:
        harm_level += harm
        count += 1

print(count)