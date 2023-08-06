import random
import numpy

from PIL import Image


def most_frequent_colour(image):

    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    return most_frequent_pixel


def average_colour(image):
    colour_tuple = [None, None, None]
    for channel in range(3):

        # Get data for one channel at a time
        pixels = image.getdata(band=channel)

        values = []
        for pixel in pixels:
            values.append(pixel)

        colour_tuple[channel] = sum(values) / len(values)

    return tuple(colour_tuple)


class Cluster(object):
    def __init__(self):
        self.pixels = []
        self.centroid = None

    def add_point(self, pixel):
        self.pixels.append(pixel)

    def set_new_centroid(self):

        r = [colour[0] for colour in self.pixels]
        g = [colour[1] for colour in self.pixels]
        b = [colour[2] for colour in self.pixels]

        r = sum(r) / len(r)
        g = sum(g) / len(g)
        b = sum(b) / len(b)

        self.centroid = (r, g, b)
        self.pixels = []

        return self.centroid


class Kmeans(object):
    def __init__(self, k=3, max_iterations=5, min_distance=5.0, size=200):
        self.k = k
        self.max_iterations = max_iterations
        self.min_distance = min_distance
        self.size = (size, size)

    def run(self, image):
        self.image = image
        self.image.thumbnail(self.size)
        self.pixels = numpy.array(image.getdata(), dtype=numpy.uint8)

        self.clusters = [None for i in range(self.k)]
        self.old_clusters = None

        random_pixels = random.sample(self.pixels, self.k)

        for idx in range(self.k):
            self.clusters[idx] = Cluster()
            self.clusters[idx].centroid = random_pixels[idx]

        iterations = 0

        while self.should_exit(iterations) is False:

            self.old_clusters = [cluster.centroid for cluster in self.clusters]

            print(iterations)

            for pixel in self.pixels:
                self.assign_clusters(pixel)

            for cluster in self.clusters:
                cluster.set_new_centroid()

            iterations += 1

        return [cluster.centroid for cluster in self.clusters]

    def assign_clusters(self, pixel):
        shortest = float("Inf")
        for cluster in self.clusters:
            distance = self.calc_distance(cluster.centroid, pixel)
            if distance < shortest:
                shortest = distance
                nearest = cluster

        nearest.addPoint(pixel)

    def calc_distance(self, a, b):

        result = numpy.sqrt(sum((a - b) ** 2))
        return result

    def should_exit(self, iterations):

        if self.old_clusters is None:
            return False

        for idx in range(self.k):
            dist = self.calc_distance(numpy.array(self.clusters[idx].centroid), numpy.array(self.old_clusters[idx]))
            if dist < self.min_distance:
                return True

        if iterations <= self.max_iterations:
            return False

        return True

    # ############################################
    # The remaining methods are used for debugging
    def show_image(self):
        self.image.show()

    def show_centroid_colours(self):

        for cluster in self.clusters:
            image = Image.new("RGB", (200, 200), cluster.centroid)
            image.show()

    def show_clustering(self):

        local_pixels = [None] * len(self.image.getdata())

        for idx, pixel in enumerate(self.pixels):
            shortest = float("Inf")
            for cluster in self.clusters:
                distance = self.calc_distance(cluster.centroid, pixel)
                if distance < shortest:
                    shortest = distance
                    nearest = cluster

            local_pixels[idx] = nearest.centroid

        w, h = self.image.size
        local_pixels = numpy.asarray(local_pixels).astype("uint8").reshape((h, w, 3))

        colour_map = Image.fromarray(local_pixels)
        colour_map.show()
