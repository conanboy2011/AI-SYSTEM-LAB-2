import json
from .visual_node import VisualNode, Node
from .genre_node import GenreVisualNode


def load_tree_dict(filename='genres.json'):
    with open(filename, 'rb') as file:
        genres = json.load(file)
    return genres


def get_coffee(genre):
    with open('coffee.json', 'r', encoding='utf-8') as file:
        genres_with_coffee = json.load(file)
    coffee = genres_with_coffee[genre] if genre in genres_with_coffee.keys() else None
    return coffee


def create_node(node_name, children_dict):
    if not children_dict:  # this node is leaf
        coffee = get_coffee(node_name.lower())
        if coffee:
            leafs = []
            for artist, attributes in coffee.items():
                leafs.append(
                    GenreVisualNode(
                        node_name,
                        artist,
                        attributes['oxidation'],
                        attributes['caffeine_content'],
                        attributes['type'],
                        attributes['additives']))
            return leafs
        else:
            node = VisualNode(val=node_name)
    else:
        node = VisualNode(val=node_name)
    for child_name in children_dict.keys():
        if children_dict:
            res = create_node(child_name, children_dict[child_name])
            if isinstance(res, list):
                for artist_node in res:
                    node.add_child(artist_node)
            else:
                node.add_child(res)
    return node


def create_tree_from_json(filename='genres.json') -> VisualNode:
    tree_dict = load_tree_dict(filename)
    return create_node('Кофе', tree_dict['Кофе'])


