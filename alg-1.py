n, k = map(int, input().split())
first_array = list(map(int, input().split()))

second_array = list(map(int, input().split()))

first_set = set(first_array)

for num in second_array:
    if num in first_set:
        print("YES")
    else:
        print("NO")