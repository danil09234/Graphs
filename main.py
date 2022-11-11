from copy import copy
from dataclasses import dataclass


@dataclass
class Edge:
    first_point: int
    second_point: int
    weight: int


def parse_input_string(string: str) -> Edge:
    return Edge(*map(int, string.split(" ")))


def parse_input_file(filename: str) -> list[Edge]:
    edges_list = []
    with open(filename, "r", encoding="utf-8") as read_file:
        file_text = read_file.read()
        file_strings = file_text.split("\n")

        for string in file_strings:
            if string != '':
                edges_list.append(parse_input_string(string))

    return edges_list


def get_all_points(edges: list[Edge]) -> list[int]:
    all_points = []
    for edge in edges:
        if edge.first_point not in all_points:
            all_points.append(edge.first_point)
        if edge.second_point not in all_points:
            all_points.append(edge.second_point)

    return all_points


def get_nearest_point(point, edges: list[Edge]) -> int | None:
    edge_with_nearest_point = None
    for edge in edges:
        if edge.first_point == point or edge.second_point == point:
            if edge_with_nearest_point is None:
                edge_with_nearest_point = edge
            elif edge.weight < edge_with_nearest_point.weight:
                edge_with_nearest_point = edge

    result_point = edge_with_nearest_point.first_point
    if result_point == point:
        result_point = edge_with_nearest_point.second_point

    return result_point


def find_edge_by_points(first_point: int, second_point: int, edges: list[Edge]) -> Edge:
    for edge in edges:
        if edge.first_point == first_point and edge.second_point == second_point:
            return edge
        elif edge.second_point == first_point and edge.first_point == second_point:
            return Edge(
                first_point=edge.second_point,
                second_point=edge.first_point,
                weight=edge.weight
            )


def get_edges_by_sequence(edges: list[Edge], sequence: list[int]) -> list[Edge]:
    edges_sequence = []

    for point_number, current_point in enumerate(sequence):
        try:
            next_point = sequence[point_number + 1]
        except IndexError:
            break

        for edge in edges:
            if edge.first_point == current_point and edge.second_point == next_point:
                edges_sequence.append(edge)
                break
            elif edge.second_point == current_point and edge.first_point == next_point:
                edges_sequence.append(Edge(edge.second_point, edge.first_point, edge.weight))
                break

    return edges_sequence


def get_edges_sequence_weight(sequence: list[Edge]) -> int:
    weight = 0

    for edge in sequence:
        weight += edge.weight

    return weight


def minimalize(edges: list[Edge], subgraph: list[int], new_point: int) -> list[int] | None:
    result = None
    result_weight = None

    if subgraph == [1, 1]:
        return [1, new_point, 1]

    for point_index in range(len(subgraph) - 1):
        current_subgraph = copy(subgraph)
        current_subgraph.insert(point_index + 1, new_point)

        current_weight = find_edge_by_points(
            current_subgraph[point_index],
            current_subgraph[point_index + 1],
            edges
        ).weight
        current_weight += find_edge_by_points(
            current_subgraph[point_index + 1],
            current_subgraph[point_index + 2],
            edges
        ).weight
        current_weight -= find_edge_by_points(
            current_subgraph[point_index],
            current_subgraph[point_index + 2],
            edges
        ).weight

        if result is None:
            result = current_subgraph
            result_weight = current_weight
        elif result_weight > current_weight:
            result = current_subgraph
            result_weight = current_weight

    return result


def initialize(edges: list[Edge], points: list[int]) -> list[int]:
    result_graph = [points[0], get_nearest_point(points[0], edges), points[0]]
    return result_graph


def find_nearest_insertion(edges: list[Edge]) -> list[int]:
    all_points = sorted(get_all_points(edges))

    result_graph = initialize(edges, all_points)

    points_left = [point for point in all_points if point not in result_graph]

    for point in points_left:
        result_graph = minimalize(edges, result_graph, point)

    return result_graph


def write_result_to_file(filename: str, nearest_insertion_sequence: list[int], edges: list[Edge]):
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
