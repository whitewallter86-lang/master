
def dfs(graph, start, visited):
    visited[start] = True
    count = 0
    for neighbor in range(len(graph)):
        if graph[start][neighbor] == 1 and not visited[neighbor]:
            count += 1 + dfs(graph, neighbor, visited)
    return count

n, s = map(int, input().split())
graph = []
for i in range(n):
    row = list(map(int, input().split()))
    graph.append(row)

visited = [False] * n
result = dfs(graph, s - 1, visited)
print(result)