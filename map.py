import random
import geopy.distance
import numpy as np
import folium

from sklearn.cluster import KMeans
from twitter_request import twitter_embed_request


class Map:
    """
    A class that models the map representation of the tweets

    Attributes
    ----------
    color_theme: list
        a list that contains the possible color for the markers as hex
    tweets_data: list
        a list of tweets dictionaries that contain "id", "text", "coordinates"
    coordinates_list: list
        a lost of extracted coordinates as [latitude, longitude] from tweets_data
    centroids: list
        a list of clusters centroids as [latitude, longitude]
    centre_location: float
        the center point of the map representation
    zoom: float
        the initial zoom of the map representation
    map: a folium.Map object
        used to generate a html map visualisation of the tweets

    Methods
    -------
    get_coordinates_list()
        return a list of coordinates as [latitude, longitude] extracted from self.tweets_data
    get_coordinates_centroids()
        return a list of clusters centroids of coordinates_list as [latitude, longitude]
    get_center_location()
        returns the center point of self.centroids
    calculate_zoom()
        return the initial zoom of the map, a float between 1 and 5 based on self.clusters and self.centroids
    add_circles()
        adds each tweet on the map as a folium.CircleMarker
    save_map(save_location)
        saves the html representation of the map at the location specified by save_location
    get_html_string_representation()
        returns the html representation of the map as  string
    """

    def __init__(self, tweets_data):
        """

        :param tweets_data: a list of dictionaries that contain "id", "text" and "coordinates" of the tweets
        """
        self.color_theme = ['#00FFFF', '#00EFFF', '#00DEFF', '#00CBFF', '#00B8FF', '#00A3FF', '#008CFF']
        self.tweets_data = tweets_data
        self.coordinates_list = self.get_coordinates_list()
        self.centroids = self.get_coordinates_centroids()
        self.centre_location = self.get_center_location()
        self.zoom = self.calculate_zoom()
        self.map = folium.Map(location=self.centre_location, tiles='Stamen Toner', zoom_start=self.zoom)
        self.add_circles()

    def get_coordinates_list(self):
        """
        A function that extracts the coordinates from self.tweets_data
        :return: list of coordinates represented as [latitude, longitude]
        """
        return [tweet['coordinates'][::-1] for tweet in self.tweets_data]

    def get_coordinates_centroids(self):
        """
        A function that uses the K means algorithm to compute the coordinates clusters and their centroids
        :return: list of clusters centroids coordinates represented as [latitude, longitude]
        """
        points = np.array(self.coordinates_list)
        k_means = KMeans(n_clusters=10 if len(self.tweets_data) > 30 else len(self.tweets_data) // 3 + 1,
                         init='k-means++',
                         random_state=0).fit(points)
        centroids = k_means.cluster_centers_
        return centroids

    def calculate_zoom(self):
        """
        A function that computes the initial zoom on the map based on the centroids and the center point
        :return: a float number between 1 and 5 that represents the initial map zoom
        """
        distances = [geopy.distance.geodesic(self.centre_location, centroid).km for centroid in self.centroids]
        a = 4 / 20000
        distances = [1 + 4 - a * distance for distance in distances]
        print(min(distances))
        return min(distances)

    def get_center_location(self):
        """
        A function that computes the center point of self.centroids
        :return: a location as [latitude, longitude]
        """
        latitude = 0
        longitude = 0
        for centroid in self.centroids:
            latitude += centroid[0]
            longitude += centroid[1]
        return [latitude / len(self.centroids), longitude / len(self.centroids)]

    def add_circles(self):
        """
        A function that requests the Twitter embed json for every tweet and adds the tweet on the map as a Circle Marker
        based on their coordinates with the embedded tweet as a Popup of the Circle Marker
        """
        for tweet in self.tweets_data:
            embed_json = twitter_embed_request(tweet["id"])
            html = embed_json["html"]

            iframe = folium.IFrame(html=html, width=500, height=400)
            popup = folium.Popup(iframe, max_width=2650)

            color = random.choice(self.color_theme)
            folium.CircleMarker(radius=50, location=tweet["coordinates"][::-1], popup=popup, color=color,
                                fill=True, fill_color=color).add_to(self.map)

    def save_map(self, save_location):
        """
        A function that saves the html representation of the map at the location specified by save_location
        :param save_location: a string that represents the file name where the map will be saved
        """
        self.map.save(save_location)

    def get_html_string_representation(self):
        """
        A function that provides the html representation as a string
        :return: a string that represents the html of the map
        """
        return self.map.get_root().render()
