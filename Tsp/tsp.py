import math
import random

random.seed(0)

def vertex_dist(x1, y1, x2, y2):
    return math.dist([x1, y1], [x2, y2])

def create_dist_matrix(points):
    n = len(points)
    dist_matrix = {}

    for i in range(n-1):
        for j in range(i+1, n):
            (x1, y1) = points[i];
            (x2, y2) = points[j];
            dist_matrix[i, j] = vertex_dist(x1, y1, x2, y2)
            dist_matrix[j, i] = dist_matrix[i, j]

    return n, dist_matrix

def create_sorted_vertex(dist_matrix, n):
    dist_list = []
    for i in range(n):
        sorted_list = [[dist_matrix[i,j], j] for j in range(n) if j!=i]
        sorted_list.sort()
        dist_list.append(sorted_list)
    return dist_list

def tour_length(tour, dist_matrix):
    tour_len = dist_matrix[tour[-1], tour[0]]

    for i in range(1, len(tour)):
        tour_len += dist_matrix[tour[i], tour[i-1]]
    
    return tour_len

def random_tour(n):
    curr_tour = list(range(n))
    random.shuffle(curr_tour)
    return curr_tour

def nearest_node(last, unvisited, dist_matrix):
    node = unvisited[0]
    min_dist = dist_matrix[last, near]
    for i in unvisited[1:]:
        if dist_matrix[last, i] < min_dist:
            node = i
            min_dist = dist_matrix[last, near]
    
    return node

def nearest_neighbour(n, i, dist_matrix):
    unvisited = range(n)
    unvisited.remove(i)
    last = i
    tour = [i]
    while unvisited:
        node = nearest_node(last, unvisited, dist_matrix)
        tour.append(node)
        unvisited.remove(node)
        last = node
    return tour

def node_swap_cost(tour, i, j, dist_matrix):
    n = len(tour)
    a, b = tour[i], tour[(i+1) % n]
    c, d = tour[j], tour[(j+1) % n]
    return (dist_matrix[a, c] + dist_matrix[b, d]) - (dist_matrix[a,b] + dist_matrix[c, d])

def two_opt(tour, tinv, i, j):
    n = len(tour)
    if i > j: i, j = j, i
    assert i >= 0 and i < j-1 and j < n
    path = tour[i+1 : j+1]
    path.reverse()
    tour[i+1 : j+1] = path
    for k in range(i+1, j+1):
        tinv[tour[k]] = k

def improve_tour(tour, z, dist_matrix, dist_list ):
    n = len(tour)
    tinv = [0 for i in tour]
    for k in range(n):
        tinv[tour[k]] = k
    for i in range(n):
        a, b = tour[i], tour[(i+1) % n]
        dist_ab = dist_matrix[a, b]
        improved = False
        for dist_ac, c in dist_list[a]:
            if dist_ac >= dist_ab:
                break
            j = tinv[c]
            d = tour[(j+1) % n]
            dist_cd = dist_matrix[c, d]
            dist_bd = dist_matrix[b, d]
            delta = (dist_ac + dist_bd) - (dist_ab + dist_cd)
            if delta < 0:
                two_opt(tour, tinv, i, j)
                z += delta
                improved = True
                break
        if improved:
            continue

        for dist_bd, d in dist_list[b]:
            if dist_bd >= dist_ab:
                break
            j = tinv[d] - 1
            if j == -1:
                j = n-1
            c = tour[j]
            dist_cd = dist_matrix[c, d]
            dist_ac = dist_matrix[a, c]
            delta = (dist_ac + dist_bd) - (dist_ab + dist_cd)
            if delta < 0:
                two_opt(tour, tinv, i, j)
                z += delta
                break

    return z

def localsearch(tour, z, dist_matrix, dist_list=None):
    n = len(tour)
    if not dist_list:
        dist_list = create_sorted_vertex(dist_matrix, n)
    while 1:
        newz = improve_tour(tour, z, dist_matrix, dist_list)
        if newz < z:
            z = newz
        else:
            break
    return z


if __name__ == "__main__":
    coord = [(4,0),(5,6),(8,3),(4,4),(4,1),(4,10),(4,7),(6,8),(8,1)]
    n, dist_matrix = create_dist_matrix(coord)
    tour = random_tour(n)
    z = tour_length(tour, dist_matrix)
    print("initial random tour length {} \n".format(z))
    z = localsearch(tour, z, dist_matrix)
    print("optimized tour length {} \n".format(z))
    print(tour, z)
