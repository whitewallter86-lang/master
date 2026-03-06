
def dfs(graph, visited, node):
    visited[node] = True
    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs(graph, visited, neighbor)

n, m = map(int, input().split())

graph = [[] for _ in range(n + 1)]

for _ in range(m):
    i, j = map(int, input().split())
    graph[i].append(j)
    graph[j].append(i)

visited = [False] * (n + 1)
components = 0

for i in range(1, n + 1):
    if not visited[i]:
        dfs(graph, visited, i)
        components += 1

print(components)