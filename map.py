import random

import folium


class Map:
    def __init__(self, tweets_data):
        self.color_theme = ['#00FFFF', '#00EFFF', '#00DEFF', '#00CBFF', '#00B8FF', '#00A3FF', '#008CFF']
        self.tweets_data = tweets_data
        self.centre_location = self.get_center_location()
        self.map = folium.Map(location=self.centre_location, tiles='Stamen Toner', zoom_start=2)
        self.add_circles()

    def get_center_location(self):
        latitude = 0
        longitude = 0
        for tweet in self.tweets_data:
            latitude += tweet["coordinates"][1]
            longitude += tweet["coordinates"][0]
        return [latitude / len(self.tweets_data), longitude / len(self.tweets_data)]

    def add_circles(self):
        for tweet in self.tweets_data:
            popup = tweet["text"]
            color = random.choice(self.color_theme)
            folium.CircleMarker(radius=50, location=tweet["coordinates"][::-1], popup=popup, color=color,
                                fill=True, fill_color=color).add_to(self.map)

    def save_map(self, save_location):
        self.map.save(save_location)

    def get_html_string_representation(self):
        return self.map.get_root().render()
