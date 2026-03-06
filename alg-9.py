
def find_connected_components():
    n, m = map(int, input().split())
    
    graph = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        i, j = map(int, input().split())
        graph[i].append(j)
        graph[j].append(i)
    
    visited = [False] * (n + 1)
    components = []
    
    def dfs(vertex, component):
        visited[vertex] = True
        component.append(vertex)
        for neighbor in graph[vertex]:
            if not visited[neighbor]:
                dfs(neighbor, component)
    
    for i in range(1, n + 1):
        if not visited[i]:
            component = []
            dfs(i, component)
            components.append(sorted(component))
    
    print(len(components))
    for component in components:
        print(len(component))
        print(*component)

find_connected_components()