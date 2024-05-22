import random
import math
import matplotlib.pyplot as plt
from util import (
    City,
    read_cities,
    path_cost,
)


class Particle:
    def __init__(self, route, cost=None):
        self.route = route
        self.pbest = route
        self.current_cost = cost if cost else self.path_cost()
        self.pbest_cost = cost if cost else self.path_cost()
        self.velocity = [random.random() for _ in range(len(route))]

    def clear_velocity(self):
        self.velocity = [0 for _ in range(len(self.route))]

    def update_costs_and_pbest(self):
        self.current_cost = self.path_cost()
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route
            self.pbest_cost = self.current_cost

    def path_cost(self):
        return path_cost(self.route)


class PSO:

    def __init__(
        self,
        iterations,
        population_size,
        w,
        c1,
        c2,
        cities=None,
    ):
        self.cities = cities
        self.gbest = None
        self.gcost_iter = []
        self.iterations = iterations
        self.population_size = population_size
        self.particles = []
        self.w = w
        self.c1 = c1
        self.c2 = c2

        solutions = self.initial_population()
        self.particles = [Particle(route=solution) for solution in solutions]

    def random_route(self):
        return random.sample(self.cities, len(self.cities))

    def initial_population(self):
        random_population = [
            self.random_route() for _ in range(self.population_size - 1)
        ]
        greedy_population = [self.greedy_route(0)]
        return [*random_population]
        # return [*random_population]

    # tạo đầu vào tốt hơn
    def greedy_route(self, start_index):
        unvisited = self.cities[:]
        del unvisited[start_index]
        route = [self.cities[start_index]]
        while len(unvisited):
            index, nearest_city = min(
                enumerate(unvisited), key=lambda item: item[1].distance(route[-1])
            )
            route.append(nearest_city)
            del unvisited[index]
        return route

    def run(self):
        self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
        print(f"initial cost is {self.gbest.pbest_cost}")
        plt.ion()
        plt.draw()
        for t in range(self.iterations):
            if t % 20 == 0:
                plt.figure(0)
                plt.plot(pso.gcost_iter, "g")
                plt.ylabel("Distance")
                plt.xlabel("Generation")
                fig = plt.figure(0)
                fig.suptitle("pso iter")
                x_list, y_list = [], []
                for city in self.gbest.pbest:
                    x_list.append(city.x)
                    y_list.append(city.y)
                x_list.append(pso.gbest.pbest[0].x)
                y_list.append(pso.gbest.pbest[0].y)
                fig = plt.figure(1)
                fig.clear()
                fig.suptitle(f"pso TSP iter thứ {t}")

                plt.plot(x_list, y_list, "ro")
                plt.plot(x_list, y_list, "g--")
                plt.draw()
                plt.pause(0.01)
            self.gcost_iter.append(self.gbest.pbest_cost)
            for particle in self.particles:
                for i in range(len(self.cities)):
                    r1 = random.random()
                    r2 = random.random()
                    new_velocity = (
                        self.w * particle.velocity[i]
                        + self.c1 * r1 * (particle.pbest[i].distance(particle.route[i]))
                        + self.c2
                        * r2
                        * (self.gbest.pbest[i].distance(particle.route[i]))
                    )
                particle.velocity[i] = new_velocity
                # Update position
                new_x = particle.route[i].x + new_velocity
                new_y = particle.route[i].y + new_velocity
                particle.route[i] = City(new_x, new_y)
                particle.update_costs_and_pbest()
                if particle.pbest_cost < self.gbest.pbest_cost:
                    self.gbest = particle


if __name__ == "__main__":
    cities = read_cities(16)
    pso = PSO(
        iterations=200,
        population_size=300,
        w=0.5,  # Hệ số trọng số quán tính
        c1=1.3,  # Hệ số học
        c2=1.5,  # Hệ số học
        cities=cities,
    )
    pso.run()
    print(f"cost: {pso.gbest.pbest_cost}\t| gbest: {pso.gbest.pbest}")
    x_list, y_list = [], []
    for city in pso.gbest.pbest:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(pso.gbest.pbest[0].x)
    y_list.append(pso.gbest.pbest[0].y)
    fig = plt.figure(1)
    fig.suptitle("pso TSP")

    plt.plot(x_list, y_list, "ro")
    plt.plot(x_list, y_list)
    plt.show(block=True)
