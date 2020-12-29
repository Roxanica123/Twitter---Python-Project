import random
import geopy.distance
import numpy as np
import folium

from sklearn.cluster import KMeans
from twitter_request import twitter_embed_request


class Map:
    def __init__(self, tweets_data):
        self.color_theme = ['#00FFFF', '#00EFFF', '#00DEFF', '#00CBFF', '#00B8FF', '#00A3FF', '#008CFF']
        self.tweets_data = tweets_data
        self.coordinates_list = self.get_coordinates_list()
        self.centroids = self.get_coordinates_centroids()
        self.centre_location = self.get_center_location()
        self.zoom = self.calculate_zoom()
        self.map = folium.Map(location=self.centre_location, tiles='Stamen Toner', zoom_start=self.zoom)
        self.add_circles()

    def get_coordinates_list(self):
        return [tweet['coordinates'][::-1] for tweet in self.tweets_data]

    def get_coordinates_centroids(self):
        points = np.array(self.coordinates_list)
        k_means = KMeans(n_clusters=10 if len(self.tweets_data) > 30 else len(self.tweets_data) // 3 + 1,
                         init='k-means++',
                         random_state=0).fit(points)
        centroids = k_means.cluster_centers_
        return centroids

    def calculate_zoom(self):
        distances = [geopy.distance.geodesic(self.centre_location, centroid).km for centroid in self.centroids]
        a = 4 / 20000
        distances = [1 + 4 - a * distance for distance in distances]
        print(min(distances))
        return min(distances)

    def get_center_location(self):
        latitude = 0
        longitude = 0
        for centroid in self.centroids:
            latitude += centroid[0]
            longitude += centroid[1]
        return [latitude / len(self.centroids), longitude / len(self.centroids)]

    def add_circles(self):
        for tweet in self.tweets_data:
            embed_json = twitter_embed_request(tweet["id"])
            html = embed_json["html"]

            iframe = folium.IFrame(html=html, width=500, height=400)
            popup = folium.Popup(iframe, max_width=2650)

            color = random.choice(self.color_theme)
            folium.CircleMarker(radius=50, location=tweet["coordinates"][::-1], popup=popup, color=color,
                                fill=True, fill_color=color).add_to(self.map)

    def save_map(self, save_location):
        self.map.save(save_location)

    def get_html_string_representation(self):
        return self.map.get_root().render()
