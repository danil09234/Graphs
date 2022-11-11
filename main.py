from copy import copy
from dataclasses import dataclass


@dataclass
class Edge:
    """
    Dataclass representing a graph edge
    """
    first_vertex: int  # First vertex of a graph edge
    second_vertex: int  # Second vertex of a graph edge
    weight: int  # Weight of a graph edge


def parse_input_string(string: str) -> Edge:
    """
    Function to parse a string of an input file into an Edge object

    Input string example:
    "1 2 5"
    where 1 is a first vertex of an edge,
    2 is a second vertex of an edge
    5 is a weight of an edge
    :param string: string to parse
    :return: Edge object of parsed string
    """
    return Edge(*map(int, string.split(" ")))


def parse_input_file(filename: str) -> list[Edge]:
    """
    Function to parse an input file into a list of edges
    :param filename: name of a file to parse
    :return: list of all edges taken from a file
    """
    edges_list = []
    with open(filename, "r", encoding="utf-8") as read_file:
        file_text = read_file.read()
        file_strings = file_text.split("\n")

        for string in file_strings:
            if string != '':
                edges_list.append(parse_input_string(string))

    return edges_list


def get_all_vertices(edges: list[Edge]) -> list[int]:
    """
    Function to get a list of all vertices of a graph by a list of all edges
    :param edges: list of all graph edges
    :return: list of all graph vertices
    """
    all_vertices = []
    for edge in edges:
        if edge.first_vertex not in all_vertices:
            all_vertices.append(edge.first_vertex)
        if edge.second_vertex not in all_vertices:
            all_vertices.append(edge.second_vertex)

    return all_vertices


def get_nearest_vertex(vertex: int, edges: list[Edge]) -> int | None:
    """
    Function to get a vertex nearest to a given
    :param vertex: given vertex
    :param edges: list of all graph edges
    :return: nearest vertex
    """
    edge_with_nearest_vertex = None
    for edge in edges:
        if edge.first_vertex == vertex or edge.second_vertex == vertex:
            if edge_with_nearest_vertex is None:
                edge_with_nearest_vertex = edge
            elif edge.weight < edge_with_nearest_vertex.weight:
                edge_with_nearest_vertex = edge

    result_vertex = edge_with_nearest_vertex.first_vertex
    if result_vertex == vertex:
        result_vertex = edge_with_nearest_vertex.second_vertex

    return result_vertex


def find_edge_by_vertices(first_vertex: int, second_vertex: int, edges: list[Edge]) -> Edge:
    """
    Function to find an edge between two vertices
    :param first_vertex: first vertex of an Edge
    :param second_vertex: second vertex of an Edge
    :param edges: list of all graph edges
    :return: Edge between two vertices
    """
    for edge in edges:
        if edge.first_vertex == first_vertex and edge.second_vertex == second_vertex:
            return edge
        elif edge.second_vertex == first_vertex and edge.first_vertex == second_vertex:
            return Edge(
                first_vertex=edge.second_vertex,
                second_vertex=edge.first_vertex,
                weight=edge.weight
            )


def get_edges_by_sequence(edges: list[Edge], sequence: list[int]) -> list[Edge]:
    """
    Function to convert a vertices sequence into a list of Edges objects
    :param edges: list of all graph edges
    :param sequence: list of vertices to convert
    :return: vertices sequence, converted into an Edges sequence
    """
    edges_sequence = []

    for vertex_number, current_vertex in enumerate(sequence):
        try:
            next_vertex = sequence[vertex_number + 1]
        except IndexError:
            break

        for edge in edges:
            if edge.first_vertex == current_vertex and edge.second_vertex == next_vertex:
                edges_sequence.append(edge)
                break
            elif edge.second_vertex == current_vertex and edge.first_vertex == next_vertex:
                edges_sequence.append(Edge(edge.second_vertex, edge.first_vertex, edge.weight))
                break

    return edges_sequence


def get_edges_sequence_weight(sequence: list[Edge]) -> int:
    """
    Function to get a weight of a given graph edges sequence
    :param sequence: sequence to handle
    :return: weight of a sequence
    """
    weight = 0

    for edge in sequence:
        weight += edge.weight

    return weight


def minimalize(edges: list[Edge], subgraph: list[int], new_vertex: int) -> list[int] | None:
    """
    Function to insert into a sequence a new vertex
    according to a step of "Nearest insertion of arbitrary city" algorithm
    :param edges: list of all graph edges
    :param subgraph: current subgraph sequence after initialization or this function use
    :param new_vertex: new vertex to insert into a graph
    :return: a sequence with inserted vertex by an algorithm
    """
    result = None
    result_weight = None

    if subgraph == [1, 1]:
        return [1, new_vertex, 1]

    for vertex_index in range(len(subgraph) - 1):
        current_subgraph = copy(subgraph)
        current_subgraph.insert(vertex_index + 1, new_vertex)

        current_weight = find_edge_by_vertices(
            current_subgraph[vertex_index],
            current_subgraph[vertex_index + 1],
            edges
        ).weight
        current_weight += find_edge_by_vertices(
            current_subgraph[vertex_index + 1],
            current_subgraph[vertex_index + 2],
            edges
        ).weight
        current_weight -= find_edge_by_vertices(
            current_subgraph[vertex_index],
            current_subgraph[vertex_index + 2],
            edges
        ).weight

        if result is None:
            result = current_subgraph
            result_weight = current_weight
        elif result_weight > current_weight:
            result = current_subgraph
            result_weight = current_weight

    return result


def initialize(edges: list[Edge], vertices: list[int]) -> list[int]:
    """
    Function to initialize a sequence according to a step of "Nearest insertion of arbitrary city" algorithm
    :param edges: list of all graph edges
    :param vertices: all vertex of a graph
    :return: sequence after initialization by an algorithm
    """
    result_graph = [vertices[0], get_nearest_vertex(vertices[0], edges), vertices[0]]
    return result_graph


def find_nearest_insertion(edges: list[Edge]) -> list[int]:
    """
    Function to find a sequence by "Nearest insertion of arbitrary city" algorithm within an all graph edges
    :param edges: list of all graph edges
    :return: sequence of vertex found within an algorithm
    """
    all_vertices = sorted(get_all_vertices(edges))

    result_graph = initialize(edges, all_vertices)

    vertices_left = [vertex for vertex in all_vertices if vertex not in result_graph]

    for vertex in vertices_left:
        result_graph = minimalize(edges, result_graph, vertex)

    return result_graph


def write_result_to_file(filename: str, nearest_insertion_sequence: list[int], edges: list[Edge]) -> None:
    """
    Function to write a list of a sequence vertices into a file with a weight of a sequence
    :param filename: filename of an output file
    :param nearest_insertion_sequence: list of a sequence vertices
    :param edges: list of all graph edges
    :return: None
    """
    sequence_weight = get_edges_sequence_weight(
        get_edges_by_sequence(
            edges, nearest_insertion_sequence
        )
    )
    with open(filename, "w", encoding="utf-8") as write_file:
        write_file.write(f"{sequence_weight}\n")
        for number_index in range(len(nearest_insertion_sequence) - 1):
            write_file.write(str(nearest_insertion_sequence[number_index]))
            if number_index < len(nearest_insertion_sequence) - 2:
                write_file.write(",")
        write_file.write("\n")


if __name__ == "__main__":
    all_input_edges = parse_input_file("example4.txt")
    nearest_insertion = find_nearest_insertion(all_input_edges)
    write_result_to_file("example4_nearest_insertion_of_arbitrary_city.txt", nearest_insertion, all_input_edges)
