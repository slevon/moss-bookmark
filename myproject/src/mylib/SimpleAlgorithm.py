def highestDegreeNode(graph):
    highestList = []
    highest = 0
    for node in graph:
        if len(graph[node]) > highest:
            highest = len(graph[node])
            highestList = [node]
        elif len(graph[node]) == highest:
            highestList.append(node)
    return highestList,highest
