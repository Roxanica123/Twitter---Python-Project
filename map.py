import folium


class Map:
    def __init__(self, tweets_data):
        self.tweets_data = tweets_data
        self.centre_location = self.get_center_location()
        self.map = folium.Map(location=self.centre_location, tiles='Stamen Toner', zoom_start=1)
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
            folium.CircleMarker(radius=50, location=tweet["coordinates"][::-1], popup=popup, color='#3186cc',
                                fill=True, fill_color='#3186cc').add_to(self.map)

    def save_map(self, save_location):
        self.map.save(save_location)
