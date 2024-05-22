import random
import math
import matplotlib.pyplot as plt
from util import City, read_cities, path_cost


class Particle:
    def __init__(self, route, cost=None):
        self.route = route
        self.pbest = route[:]
        self.current_cost = cost if cost else self.path_cost()
        self.pbest_cost = cost if cost else self.path_cost()
        self.velocity = [0] * len(route)

    def update_costs_and_pbest(self):
        self.current_cost = self.path_cost()
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route[:]
            self.pbest_cost = self.current_cost

    def path_cost(self):
        return path_cost(self.route)


class PSO:
    def __init__(
        self,
        iterations,
        population_size,
        c1=1.5,
        c2=1.5,
        cities=None,
    ):
        self.cities = cities
        self.gbest = None
        self.gcost_iter = []
        self.iterations = iterations
        self.population_size = population_size
        self.particles = []
        self.cognitive_constant = c1
        self.social_constant = c2

        solutions = self.initial_population()
        self.particles = [Particle(route=solution) for solution in solutions]

    def random_route(self):
        return random.sample(self.cities, len(self.cities))

    def swap_positions(self, route, pos1, pos2):
        route[pos1], route[pos2] = route[pos2], route[pos1]

    def initial_population(self):
        random_population = [self.random_route() for _ in range(self.population_size)]
        return random_population

    def run(self):
        self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
        print(f"Initial cost is {self.gbest.pbest_cost}")
        plt.ion()
        plt.draw()
        for t in range(self.iterations):
            if t % 100 == 0:
                plt.figure(0)
                plt.plot(self.gcost_iter, "orange")
                plt.ylabel("Distance")
                plt.xlabel("Iterations")
                fig = plt.figure(0)
                plt.legend(["Distance"])
                x_list, y_list = [], []
                for city in self.gbest.pbest:
                    x_list.append(city.x)
                    y_list.append(city.y)
                x_list.append(self.gbest.pbest[0].x)
                y_list.append(self.gbest.pbest[0].y)
                fig = plt.figure(1)
                fig.clear()
                fig.suptitle(f"PSO TSP Iteration {t}")
                plt.xlabel("x")
                plt.ylabel("y")
                plt.plot(x_list, y_list, "ro")
                plt.plot(x_list, y_list, "g--")
                plt.draw()
                plt.pause(0.001)
            self.gcost_iter.append(self.gbest.pbest_cost)
            for particle in self.particles:
                new_velocity = []
                for i in range(len(particle.route)):
                    r1, r2 = random.random(), random.random()
                    cognitive_velocity = (
                        self.cognitive_constant
                        * r1
                        * (particle.pbest[i].x - particle.route[i].x)
                    )
                    social_velocity = (
                        self.social_constant
                        * r2
                        * (self.gbest.pbest[i].x - particle.route[i].x)
                    )
                    new_velocity.append(cognitive_velocity + social_velocity)
                particle.velocity = new_velocity

                new_route = particle.route[:]
                for i in range(len(new_route)):
                    swap_index = int(particle.velocity[i]) % len(new_route)
                    new_route[i], new_route[swap_index] = (
                        new_route[swap_index],
                        new_route[i],
                    )

                particle.route = new_route
                particle.update_costs_and_pbest()

                # Cập nhật gbest nếu cần
                if particle.pbest_cost < self.gbest.pbest_cost:
                    self.gbest = particle


if __name__ == "__main__":
    cities = read_cities(18)
    pso = PSO(
        iterations=10000,
        population_size=500,
        c1=1.4,
        c2=1.4,
        cities=cities,
    )
    pso.run()
    print(f"Cost: {pso.gbest.pbest_cost}\nGbest: {pso.gbest.pbest}")
    x_list, y_list = [], []
    for city in pso.gbest.pbest:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(pso.gbest.pbest[0].x)
    y_list.append(pso.gbest.pbest[0].y)
    fig = plt.figure(1)
    fig.suptitle("PSO TSP")

    plt.plot(x_list, y_list, "ro")
    plt.plot(x_list, y_list)
    plt.show(block=True)
