# Author: James Chen
# Date: 2025-05-25
# Description: Graph traversal game that employs Dijkstra, player finds optimal path through graph

import math
import matplotlib.pyplot as plt
import random
import time


def tsp_game():
    coordinates, graph = generate_map(6)
    min_path, min_time = tsp(graph)
    # print(min_path)
    n = len(graph)
    cities = {0: "PrisonTown",
              1: "Bootsville",
              2: "Seamsland",
              3: "WidgetTown",
              4: "Cornland",
              5: "DustSwamp"}
    visited = set()
    visited.add(0)
    hours_left = min_time
    game_state = 1

    print(f"Thank the heavens you escaped, punished ranger.")
    time.sleep(1)
    print("The imperial army is coming, and we must stand together!")
    time.sleep(1)
    print(f"Find the shortest path you can between all {n} towns, only united can we prevail against the enemy.")
    time.sleep(1)
    print("Rules: We only have time to visit each city once, there's no time to waste!")
    time.sleep(1)
    print(f"Mission: Communications are down, and we'll need to visit all {n-1} towns by horseback in the next {round(min_time,1)} hours.\n")
    time.sleep(1)

    draw_map(coordinates, cities)
    prev = 0
    inp = None

    while inp != "quit":
        print(f"We are currently at: #{prev} {cities[prev]}.")
        print(f"Only {round(hours_left, 1)} hours before the enemy arrives.")
        print("Where to next? Enter a number OR enter 'quit' to surrender.\n")

        # Display player's options
        for _ in range(1, len(cities)):
            if _ not in visited:
                print(f"{_}. {cities[_]} | {round(graph[prev][_],1)} hours away")

        inp = input("\nYour Selection: ")

        # Quit game
        if inp == "quit":
            game_state = 0
            break

        # Read player input
        try:
            inp = int(inp)
        except TypeError:
            if int(inp) not in cities.keys():
                print("Invalid city key entered, try again.")
                continue

        # Already visited
        if inp in visited:
            print("We already went there, remember? It's a ghost town now!")
            continue

        # Valid choice, add to visited set, deduct time left
        visited.add(inp)
        time_spent = graph[prev][inp]
        hours_left -= time_spent
        prev = inp

        # Ran out of time
        if hours_left < 0:
            game_state = 2
            break

        # Success
        if len(visited) == n and round(hours_left,0) >= 0:
            game_state = 3
            break

        print(f"\nNext stop, {cities[inp]}!")
        time.sleep(2)
        print("...\n...\nRiding\n...\n...\n")
        time.sleep(2)

    # End States
    print(hours_left)
    if game_state == 0:
        print("Guess you weren't the hero the prophecy foretold after all.")
    if game_state == 1:
        print("ERROR")
    if game_state == 2:
        print("We tried our best, ranger. At least we were able to save the souls in:")
        for _ in range(len(visited)):
            print(cities[_])
    if game_state == 3:
        print("We saved them all! History will remember our great deeds today.")


def draw_map(cities: list, labels: dict):
    n = len(cities)

    # Set up plot vertices
    plt.figure(figsize=(20, 20))
    for _ in range(n):
        xi, yi = cities[_]
        plt.plot(xi, yi, 'bo', markersize=12)
        plt.text(xi + 0.1, yi + 0.1, f"{_}. {labels[_]}", fontsize=20)

    # Draw edges
    for i in range(n):
        for j in range(i+1, n):
            # Plot lines
            x_values = [cities[i][0], cities[j][0]]
            y_values = [cities[i][1], cities[j][1]]
            plt.plot(x_values, y_values, 'gray', linestyle="--", linewidth=3)

            # Add labels at midpoint
            mid_x = (cities[i][0] + cities[j][0]) / 2
            mid_y = (cities[i][1] + cities[j][1]) / 2
            dist = euclidean(cities[i], cities[j])
            plt.text(mid_x, mid_y, f"{round(dist, 1)}", fontsize=20, color='red')

    plt.show()


def generate_map(num_cities: int):
    points = []
    while len(points) < num_cities:
        coordinates = [random.randint(0, 10), random.randint(0, 10)]
        if coordinates not in points:
            points.append(coordinates)

    matrix = []
    for i in range(num_cities):
        row = []
        for j in range(num_cities):
            dist = euclidean(points[i], points[j])
            row.append(dist)
        matrix.append(row)

    return points, matrix


def euclidean(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])


def tsp(graph: list):
    n = len(graph)
    queue = []
    memo = dict()
    min_path = None
    min_dist = math.inf

    current_path = [0,]
    distance = 0

    memo[(tuple(current_path))] = distance
    queue.append(tuple(current_path))

    while queue:
        current_path = queue.pop(0)
        current_point = current_path[-1]

        options = []
        for _ in range(n):
            if _ not in current_path:
                options.append(_)

        for choice in options:
            new_path = list(current_path)
            new_path.append(choice)
            distance = memo[current_path] + graph[current_point][choice]
            memo[(tuple(new_path))] = distance
            queue.append((tuple(new_path)))

        if len(new_path) == n:
            if distance < min_dist:
                min_path = new_path
                min_dist = distance

    # print(queue)
    # print(memo)

    return min_path, min_dist


if __name__ == "__main__":
    # test_graph = [
    #     [0, 1, 2, 3],
    #     [1, 0, 2, 3],
    #     [2, 1, 0, 3],
    #     [3, 2, 1, 0],
    # ]
    #
    # print(tsp(test_graph))
    #
    # test_graph2 = [
    #     [0, 1, 2, 3],
    #     [4, 0, 5, 6],
    #     [7, 8, 0, 9],
    #     [10, 11, 12, 0],
    # ]
    #
    # print(tsp(test_graph2))

    tsp_game()