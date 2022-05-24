class DeterMineChromaticNumber:

    def isSafe(self, node, color, graph, n, col):
        k = 0
        while k < n:
            if (k != node) and (graph[k][node] == 1) and (color[k] == col):
                return False
            k += 1
        return True

    def solve(self, node, color, m, N, graph):
        # base condition
        if node == N:
            return True
        i = 1
        while i <= m:
            # if it is safe to color current vertex with ith color
            if self.isSafe(node, color, graph, N, i):
                # color current vertex with ith color
                color[node] = i
                # move to next level in recursion to check for other vertices
                if self.solve(node + 1, color, m, N, graph):
                    return True
                # un-color the vertex while moving up in recursion
                color[node] = 0
            i += 1
        return False

    def getChromaticNumber(self, graph):
        N = len(graph)
        color = [0 for _ in range(N)]
        lo = 1
        hi = N
        ans = N
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if self.solve(0, color, mid, N, graph):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans
