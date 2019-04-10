from shapely.geometry import Polygon, Point
import random

class grid():

    def __init__(self, log_data, unobserved_points = 50):
        self.log_data = log_data
        self.unobserved_points = unobserved_points

    def polygon_creation(self,k):    ## give the intial dataframe here
        coordinates_list = []
        for i in range(len(k)):
            coordinates = (k[i]['lat'][0], k[i]['long'][0])
            coordinates_list.append(coordinates)
        poly = Polygon(coordinates_list)
        return poly

    def random_points_within(self,poly, num_points):
        min_x, min_y, max_x, max_y = poly.bounds
        points = []

        while len(points) < num_points:
            random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
            if (random_point.within(poly)):
                points.append(random_point)
        return points

    def grid_main(self):
        poly = self.polygon_creation(self.log_data)
        return self.random_points_within(poly, self.unobserved_points)