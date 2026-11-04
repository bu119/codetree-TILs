N, M = map(int, input().split())

# Please write your code here.
def dfs(i, n):
    global ans

    if n == M:
        print(' '.join(map(str, ans)))
        return

    for j in range(i+1, N+1):
        ans.append(j)
        dfs(j, n+1)
        ans.pop()

ans = []
dfs(0,0)