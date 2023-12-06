from lark import Lark, Transformer, v_args
import numpy as np

# Define the grammar
grammar = """
    ?start: problem_name knapsack_data_type dimension number_items knapsack_capacity min_speed max_speed renting_ratio edge_weight_type node_coord_section items_section

    problem_name: "PROBLEM NAME:" STRING
    knapsack_data_type: "KNAPSACK DATA TYPE:" knapsack_types
    dimension: "DIMENSION:" NUMBER
    number_items: "NUMBER OF ITEMS:" NUMBER
    knapsack_capacity: "CAPACITY OF KNAPSACK:" NUMBER
    min_speed: "MIN SPEED:" NUMBER
    max_speed: "MAX SPEED:" NUMBER
    renting_ratio: "RENTING RATIO:" NUMBER
    edge_weight_type: "EDGE_WEIGHT_TYPE:" STRING

    node_coord_section: "NODE_COORD_SECTION" "(" "INDEX, X, Y" "):" node+

    items_section: "ITEMS SECTION" "(" "INDEX," "PROFIT," "WEIGHT," "ASSIGNED NODE NUMBER" "):" item+

    node: NUMBER NUMBER NUMBER
    item: NUMBER NUMBER NUMBER NUMBER

    KNAPSACK: ("unknown" | "uncorrelated" | "bounded strongly corr" | "similar weights")
    knapsack_types: KNAPSACK ("," KNAPSACK)*
    
    STRING: ("-"|LETTER) ("_"|"-"|LETTER|DIGIT)*

    %import common.LETTER
    %import common.DIGIT
    %import common.NUMBER
    %import common.SIGNED_INT -> INT
    %import common.SIGNED_FLOAT -> FLOAT
    %import common.WS

    %ignore WS
"""

parser = Lark(grammar, parser='lalr', transformer=Transformer(), start='start')


# Define a transformer to convert the parsed data into a data structure
@v_args(inline=True)
class DatasetTransformer(Transformer):
    def start(self, *args):
        return Dataset(*args)

    def problem_name(self, name):
        return name[::]

    def knapsack_data_type(self, values):
        return list(map(str, values))

    def dimension(self, dimension):
        return int(dimension)

    def number_items(self, number_items):
        return int(number_items)

    def knapsack_capacity(self, knapsack_capacity):
        return int(knapsack_capacity)

    def min_speed(self, min_speed):
        return float(min_speed)

    def max_speed(self, max_speed):
        return float(max_speed)

    def renting_ratio(self, renting_ratio):
        return float(renting_ratio)

    def edge_weight_type(self, edge_type):
        return edge_type[::]

    def node_coord_section(self, *nodes):
        return np.array(nodes)

    def items_section(self, *items):
        return np.array(items)

    def node(self, *data):
        return Node(int(data[0]), int(data[1]), int(data[2]))

    def item(self, *attributes):
        return Item(int(attributes[0]), int(attributes[1]), int(attributes[2]), int(attributes[3]))

    def knapsack_types(self, *types):
        return list(types)


class Node:
    def __init__(self, index, x_coord, y_coord):
        self.index = index
        self.x = x_coord
        self.y = y_coord

    def __repr__(self):
        return f"<index:{self.index},  x:{self.x}, y:{self.y}>"


class Item:
    def __init__(self, index, profit, weight, node_number):
        self.index = index
        self.profit = profit
        self.weight = weight
        self.node_number = node_number

    def __repr__(self):
        return f"<index:{self.index}, profit:{self.profit}, weight:{self.weight}, node_number:{self.node_number}>"


class Dataset:
    def __init__(self, name, knapsack_type, dimension, number_items, knapsack_capacity, min_speed, max_speed,
                 renting_ratio, edge_type, nodes, items):
        self.name = name
        self.knapsack_type = knapsack_type
        self.dimension = dimension
        self.number_items = number_items
        self.knapsack_capacity = knapsack_capacity
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.renting_ratio = renting_ratio
        self.edge_type = edge_type
        self.nodes = nodes
        self.items = items

    def __repr__(self):
        return (f"<name:{self.name}\n knapsack_type:{self.knapsack_type}\n dimension:{self.dimension}\n "
                f"number_items:{self.number_items}\n knapsack_capacity:{self.knapsack_capacity}\n "
                f"min_speed:{self.min_speed}\n max_speed:{self.max_speed}\n renting_ratio:{self.renting_ratio}\n "
                f"edge_type:{self.edge_type}\n nodes:{self.nodes}\n items:{self.items}>")

    def new(file_content):
        """
        Function to return a Dataset for a given file

        For example:
        
        NAME_OF_DATASET = Dataset.new(open("data/a280-n279.txt", 'r').read())

        To access the underlying information, use the format NAME_OF_DATASET.FIELD
        where FIELD is one of:
        (name, knapsack_type, dimension, number_items, knapsack_capacity, 
        min_speed, max_speed, renting_ratio, edge_type, nodes, items)
        """
        return DatasetTransformer().transform(parser.parse(file_content))