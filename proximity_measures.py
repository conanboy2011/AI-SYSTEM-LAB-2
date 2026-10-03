from pow_distance import *
from tree.genre_node import GenreVisualNode
from tree.tree_tools import *
from tree.node import Node

# https://ecocyb.narod.ru/513/MSM/msm2_2.htm
# Евклидово расстояние
def calc_euclidean_measure(leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items() if name not in ('name', 'type')] # [1.0, 0.12, 0.6666666666666666]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items() if name not in ('name', 'type')] # [1.0, 0.12, 0.6666666666666666]
    # print(leaf_1.name, leaf_2.name, attributes1, attributes2)
    return calc_distance_in_pow(attributes1, attributes2, 2)

# Манхэттенское расстояние (Расстояние городских кварталов)
def calc_manhattan_measure(leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items() if name in ('name', 'type')]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items() if name in ('name', 'type')]
    return calc_distance_in_pow(attributes1, attributes2, 1)

# Косинусная мера близости
def Cosine_measure(leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items()] # [1.0, 0.05, 0.0, 0.12, 0.6666666666666666]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items()] # [1.0, 0.05, 0.0, 0.12, 0.6666666666666666]
    # print(attributes1)
    sumMulty = 0
    for elem in range(len(attributes1)):
        sumMulty += attributes1[elem] * attributes2[elem]
    
    sum1 = 0
    for elem in range(len(attributes1)):
        sum1 += pow(attributes1[elem], 2)
    sum1 = pow(sum1, 1/2)
    
    sum2 = 0
    for elem in range(len(attributes2)):
        sum2 += pow(attributes2[elem], 2)
    sum2 = pow(sum2, 1/2)
    # print(sumMulty)
    return (sumMulty / (sum1 * sum2))

# Мера Жаккарда
def Jaccard_measure(leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    attributes1 = leaf_1.values_coffee # ['ШОКОЛАД', 'additives', 'cappuccino', 'Espresso-based', '12', 'average']
    attributes2 = leaf_2.values_coffee
    # print(attributes1)
    node1_set = set(attributes1)
    node2_set = set(attributes2)
    
    shared = node1_set.intersection(node2_set)
    total = node1_set.union(node2_set)
    
    return len(shared) / len(total)

# Ассоциативная мера близости
def calc_associative_measure(leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items()] # [1.0, 0.05, 0.0, 0.12, 0.6666666666666666]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items()] # [1.0, 0.05, 0.0, 0.12, 0.6666666666666666]
    
    cnt_similars = 0
    cnt = 0
    for elem in range(len(attributes1)):
        if attributes1[elem] == attributes2[elem]:
            cnt_similars += 1
        cnt += 1
    # print(attributes1)
    return cnt_similars / cnt

def calc_tree_distance_measure(
        tree: Node,
        leaf_1: GenreVisualNode,
        leaf_2: GenreVisualNode,
        max_distance_between_nodes: int
):
    return calc_distance_between_nodes(tree, leaf_1.name, leaf_2.name) / max_distance_between_nodes


def generalizing_proximity_measure(tree: Node, leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    max_distance_between_coffee = calc_max_distance_between_nodes(tree)
    euclidean_proximity = calc_euclidean_measure(leaf_1, leaf_2)
    manhattan_proximity = calc_manhattan_measure(leaf_1, leaf_2)
    associative_proximity = calc_associative_measure(leaf_1, leaf_2)
    tree_distance = calc_tree_distance_measure(tree, leaf_1, leaf_2, max_distance_between_coffee)
    generalizing_proximity = euclidean_proximity + manhattan_proximity / 10 + associative_proximity + tree_distance
    return generalizing_proximity