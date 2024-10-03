import heapq

# 현재 여행 상품의 출발지로부터 각 도시의 최단거리
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


# 상품이 생기면 이득 추가
def add_product_benefits(productId):
    revenue, dest = travelProducts[productId] 
    cost = costs[dest]
    # 판매 불가 상품아 아닐 때, 이득 계산
    if revenue >= cost:
        heapq.heappush(productBenefits, (-(revenue - cost), productId))

# 전체 상품의 이득 생성
def find_product_benefits():
    benefits = []
    for productId in travelProducts:
        revenue, dest = travelProducts[productId]
        cost = costs[dest]
        # 판매 불가 상품
        if revenue < cost:
            continue
        # 판매 이득 [revenue - cost]가 최대인 상품을 우선함
        # 같은 값을 가지는 상품이 여러 개 있을 경우, id 가 가장 작은 상품
        heapq.heappush(benefits, (-(revenue - cost), productId))
    
    return benefits

# 최적의 여행 상품 찾기
def find_best_product():
    # 이득도 남아있고 여행 상품도 남아 있을 때, 최적 상품 반환
    while productBenefits and travelProducts:
        _, productId = heapq.heappop(productBenefits)
        # 판매 가능한 상품
        if productId in travelProducts:
            # 관리 목록에서 제거
            del travelProducts[productId]
            return productId
    # 판매 가능한 상품이 전혀 없다면 −1 반환
    return -1


q = int(input())
INF = 20000000000
travelProducts = dict()
# 각 여행 상품의 이득 저장 (이득, 고유 id)
productBenefits = []

for _ in range(q):
    type, *info = list(map(int, input().split()))
    
    if type == 100:
        # 코드트리 랜드 건설
        # 도시의 수 n, 간선의 수 m
        n = info[0]
        m = info[1]
        graph = [[] for _ in range(n+1)]

        for i in range(2, m*3, 3):
            # 도시 v와 도시 u는 가중치가 w인 간선으로 연결
            v, u, w = info[i], info[i+1], info[i+2]
            graph[v].append((u, w))
            graph[u].append((v, w))
            
        # 출발지로부터 각 도시의 최단거리
        costs = dijkstra(0)
        
    elif type == 200:
        # 여행 상품 생성
        # 고유한 식별자 id, 매출 revenue, 도착지 dest
        id, revenue, dest = info
        travelProducts[id] = (revenue, dest)
        # 상품 생성시 이득 계산
        add_product_benefits(id)
    
    elif type == 300:
        # 여행 상품 취소
        id = info[0]
        # 해당하는 여행 상품이 존재하는 경우, 여행 상품을 관리 목록에서 삭제
        if id in travelProducts:
            del travelProducts[id]
    
    elif type == 400:
        # 최적의 여행 상품 판매
        # 매번 이득 계산 -> 시간 초과
        # 출발점이 같으면 계산되 이득도 같다. -> 상품 생성 될 때 저장 해놓고 쓰자.
        print(find_best_product())     
   
    else:
        # 여행 상품의 출발지 변경
        s = info[0]
        # 출발지가 변경됨에 따라 각 상품의 cost_id가 변경
        costs = dijkstra(s)
        # 각 상품 이득 새로 계산
        productBenefits = find_product_benefits()