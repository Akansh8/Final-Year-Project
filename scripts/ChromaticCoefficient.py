class ChromaticCoefficient:
    def isSafe(self, node, color, graph, n, col):
        k = 0
        while k < n:
            if (k != node) and (graph[k][node] == 1) and (color[k] == col):
                return False
            k += 1
        return True

    def solve(self, node, color, m, N, graph):
        if node == N:
            myset = set([])
            for i in range(N):
                myset.add(color[i])
            if len(myset) == m:
                return 1
            return 0
        ways = 0
        i = 1
        while i <= m:
            if self.isSafe(node, color, graph, N, i):
                color[node] = i
                ways += self.solve(node + 1, color, m, N, graph)
                color[node] = 0
            i += 1
        return ways

    def getCoefficient(self,graph, m):
        N = len(graph)
        color = [0 for _ in range(N)]
        return self.solve(0, color, m, N, graph)
