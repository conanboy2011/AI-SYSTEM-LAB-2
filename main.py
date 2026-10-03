from tree.visual_node import VisualNode, Node
from tree.genre_node import GenreVisualNode
from tree.node import Node
from tree.tree_tools import *
from tree.tree_loader import *
from tree.genre_node import GenreVisualNode
from proximity_measures import *
from plot import plot
from numpy import std
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from coffee import *


def get_pirson_coeff(x: list, y: list, n):
    x_avg = sum(x) / len(x)
    y_avg = sum(y) / len(y)
    sigma = 0
    for i in range(len(x)):
        sigma += (x[i] - x_avg) * (y[i] - y_avg)
    r_xy = sigma / ((n - 1) * std(x) * std(y))
    return r_xy


def format_print(values: list, column_width: list[int], number_symbols_after_comma=5):
    assert column_width
    current_column_width = 0
    for i, value in enumerate(values):
        if len(column_width) - 1 >= i:
            current_column_width = column_width[i]
        if isinstance(value, float):
            value = round(value, number_symbols_after_comma)
        print(str(value).ljust(current_column_width), end=' ')
    print()


def compare_measures(tree, coffee_pairs):
    euclidean_proximity = []
    manhattan_proximity = []
    associative_measure = []
    cosine_measure = []
    jaccard_measure = []
    tree_distance_proximity = []
    generalizing_proximity = []
    max_distance_between_coffee = calc_max_distance_between_nodes(tree)
    for coffee1, coffee2 in coffee_pairs:
        euclidean_proximity.append(calc_euclidean_measure(coffee1, coffee2))
        manhattan_proximity.append(calc_manhattan_measure(coffee1, coffee2))
        associative_measure.append(calc_associative_measure(coffee1, coffee2))
        cosine_measure.append(Cosine_measure(coffee1, coffee2))
        jaccard_measure.append(Jaccard_measure(coffee1, coffee2))
        tree_distance_proximity.append(calc_tree_distance_measure(tree, coffee1, coffee2, max_distance_between_coffee))
        generalizing_proximity.append(generalizing_proximity_measure(tree, coffee1, coffee2))

    coffee_names = [(coffee1.name + ' - ' + coffee2.name) for coffee1, coffee2 in coffee_pairs]
    format_print(['coffee', 'generalizing', 'euclidean', 'manhattan', 'associative', 'jaccard', 'cosine', 'tree distance'], [25, 15])
    for i in range(len(coffee_names)):
        format_print(
            [coffee_names[i], generalizing_proximity[i], euclidean_proximity[i], manhattan_proximity[i],
             associative_measure[i], jaccard_measure[i], cosine_measure[i], tree_distance_proximity[i]],
            column_width=[25, 15],
            number_symbols_after_comma=6
        )


if __name__ == '__main__':
    tree = create_tree_from_json('test.json')

    # tree.render_tree()
    # VisualNode.show_tree(tree)

    ## ноды для мер близости
    espresso = Node.get_child_by_name(tree, 'espresso')
    cappuccino = Node.get_child_by_name(tree, 'cappuccino')
    cortado = Node.get_child_by_name(tree, 'cortado')
    americano = Node.get_child_by_name(tree, 'americano')
    macchiato = Node.get_child_by_name(tree, 'macchiato')
    latte = Node.get_child_by_name(tree, 'latte')
    mocha = Node.get_child_by_name(tree, 'mocha')
    aeropress = Node.get_child_by_name(tree, 'aeropress')
    coffee = [espresso, cappuccino, cortado, americano, macchiato, latte]

    ## сравнение
    # coffee_pairs = [(cappuccino, cortado), (americano, cappuccino), (americano, cortado), (americano, espresso), (americano, macchiato), (americano, latte), (latte, macchiato), (mocha, aeropress)]
    coffee_pairs = [(mocha, aeropress)]
    compare_measures(tree, coffee_pairs)

    # Tạo một từ điển mới coffee_data để lưu trữ dữ liệu
    coffee_data = {}
    keys = []
    for i in COFFEE:
        name = i.lower()
        coffee_node = Node.get_child_by_name(tree, name)
        attributes = coffee_node.countable_attributes.items()
        # Duyệt qua các mục và thêm giá trị vào coffee_data
        for key, value in attributes:
            # Nếu key chưa có trong coffee_data, khởi tạo danh sách rỗng
            if key not in coffee_data:
                coffee_data[key] = []
            # Thêm giá trị vào danh sách tương ứng với key
            coffee_data[key].append(value)
            keys.append(key)
    # print(coffee_data)
    # Create a DataFrame
    df = pd.DataFrame(coffee_data)

    # Calculate the correlation matrix
    corr_matrix = df.corr()

    # Display the correlation matrix
    print(corr_matrix)

    sns.heatmap(corr_matrix, annot=True)
    plt.show()

    df.plot(x=keys[3], y=keys[2], style='o')
    plt.show()

    df.plot(x=keys[0], y=keys[2], style='o')
    plt.show()

    df.plot(x=keys[4], y=keys[1], style='o')
    plt.show()






