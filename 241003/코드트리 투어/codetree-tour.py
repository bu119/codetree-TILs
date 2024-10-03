# 가중치 -> 다익스트라, 신장트리
# 도시의 수 n 과 간선의 수 m, 그리고 m 개의 간선
# 간선 정보 (vi, ui, wi): 도시 vi와 도시 ui는 가중치가 wi인 간선으로 연결

# <여행 상품 생성>
# (id, revenue_id, dest_id) 여행 상품을 추가 -> 관리 목록에 추가
# 고유한 식별자 id, 얻게되는 매출은 revenue_id, 이 상품의 도착지는 dest_id

# <여행 상품 취소>
# 고유 식별자 id 에 해당하는 여행 상품이 존재하는 경우, 해당 id 의 여행 상품을 관리 목록에서 삭제

# <최적의 여행 상품 판매>
# 관리 목록에서 조건에 맞는 최적의 여행 상품을 선택하여 판매

# 선택 조건
# 1. 여행사의 상품 판매 이득 [revenue_id - cost_id]가 최대인 상품을 우선적으로 고려
# 2. 같은 값을 가지는 상품이 여러 개 있을 경우 id 가 가장 작은 상품을 선택
# cost_id 는 현재 여행 상품의 출발지로부터 id 상품의 도착지 dest_id 까지 도달하기 위한 최단거리

# 판매 불가능 상품
# 1. 출발지로부터 dest_id 에 도달하는 것이 불가능
# 2. revenue_id < cost_id

# 판매 가능 상품
# 1. 우선순위가 높은 상품을 1개를 판매, 이 상품의 id 를 출력한 뒤 이 상품을 관리 목록에서 제거
# 2. 판매 가능한 상품이 전혀 없다면 −1 을 출력하고 상품을 제거하지 않게 됨

# <여행 상품의 출발지 변경>
# 여행 상품의 출발지를 전부 s 로 변경하는 명령
# 출발지가 변경됨에 따라 각 상품의 cost_id가 변경될 수 있음

import heapq

# 출발지에서 각 점까지의 최단거리
def dijkstra(start):
    # 모든 정점사이의 거리를 최댓값으로 초기화
    # 최단 거리 저장
    visited = [INF]*(n+1)
    heap = []
    # 최단거리, 출발 위치 저장
    heapq.heappush(heap, (0, start))
    visited[start] = 0
    while heap:
        # start부터 현재 위치까지 최단거리, 현재 위치
        currDist, currCity = heapq.heappop(heap)

        # 이미 저장된 거리가 새로 측정된 거리보다 짧으면 탐색하지 않는다.
        if visited[currCity] < currDist:
            continue

        # 이동 가능한 다음 위치, 다음 위치까지 거리
        for nextCity, dist in graph[currCity]:
            totalDist = currDist + dist
            # 새로 구한 거리가 저장된 거리보다 짧으면 갱신
            if totalDist < visited[nextCity]:
                visited[nextCity] = totalDist
                heapq.heappush(heap, (totalDist, nextCity))
    # 출발지에서 각 지점까지 최단거리 반환
    return visited


def find_product_benefits():
    # 각 여행 상품의 이득 저장 (이득, 고유 id)
    heap = []
    
    for productId in travelProducts:
        revenue, dest = travelProducts[productId] 
        cost = costs[dest]
        # 판매 불가 상품
        if revenue < cost:
            continue

        heapq.heappush(heap, (-(revenue - cost), productId))
        
    return heap


def find_best_product():

    while productBenefits:
        _, productId = heapq.heappop(productBenefits)
        # managementProducts에서 취소상품이 아닌지 확인
        # managementProducts에 취소상품은 없음
        # productBenefits에는 취소 상품도 있음 -> 제외해야함.
        if productId in managementProducts:
            del travelProducts[productId]
            return productId
    
    return -1
    

q = int(input())
INF = 20000000000
s = 0
travelProducts = dict()
managementProducts = set()

for _ in range(q):
    type, *info = list(map(int, input().split()))
    
    if type == 100:
        # 코드트리 랜드 건설
        n = info[0]
        m = info[1]
        graph = [[] for _ in range(n+1)]
        
        for i in range(2, m*3, 3):
            v, u, w = info[i], info[i+1], info[i+2]
            graph[v].append((u, w))
            graph[u].append((v, w))
            
        # 출발지로부터 각 도시의 최단거리
        costs = dijkstra(s)
        
    elif type == 200:
        # 여행 상품 생성
        id, revenue, dest = info
        travelProducts[id] = (revenue, dest)
        managementProducts.add(id)
    
    elif type == 300:
        # 여행 상품 취소
        id = info[0]
        # 여행 상품이 존재하는 경우 삭제
        if id in travelProducts:
            del travelProducts[id]
            managementProducts.remove(id)
            
    elif type == 400:
        # 최적의 여행 상품 판매 
        # 매번 이득 계산 -> 시간 초과
        # 출발점이 같으면 계산되 이득도 같다. -> 저장 해놓은 것을 쓰자.
        if s == 0:
            productBenefits = find_product_benefits()
        print(find_best_product())
    
    else:
        # 여행 상품의 출발지 변경
        s = info[0]
        costs = dijkstra(s)
        productBenefits = find_product_benefits()