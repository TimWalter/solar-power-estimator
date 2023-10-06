import requests
from PIL import Image
import numpy as np

from global_mercator import GlobalMercator
from sec.keys import MAPTILER_API_KEY


class ElevationProvider:
    def __init__(self, api_key):
        self.api_key = api_key
        self.gm = GlobalMercator(512)
        self.tiles = {}

    def get_elevation(self, lat, lon):
        tile_index = self.get_tile_index(lat, lon, 12)
        tile_data = self.get_or_fetch_tile(tile_index)
        return self.decode_elevation(lat, lon, tile_index, tile_data)

    def get_or_fetch_tile(self, tile_index):
        key = self.create_tile_key(tile_index)
        if key in self.tiles:
            tile = self.tiles[key]
        else:
            tile = self.fetch_tile(tile_index)
            self.tiles[key] = tile
        return tile

    def fetch_tile(self, tile_index):
        url = f"https://api.maptiler.com/tiles/terrain-rgb/{tile_index['zoom']}/{tile_index['x']}/{tile_index['y']}.png?key={self.api_key}"
        image = self.load_image(url)
        return self.get_image_data(image)

    def load_image(self, url):
        response = requests.get(url, stream=True)
        image = Image.open(response.raw)
        return image

    def get_image_data(self, image):
        image_data = np.array(image)
        return image_data

    def create_tile_key(self, tile_index):
        return f"{tile_index['zoom']}_{tile_index['y']}_{tile_index['x']}"

    def get_tile_index(self, lat, lon, zoom):
        tms = self.gm.LatLonToTile(lat, lon, zoom)
        google = self.gm.GoogleTile(tms["tx"], tms["ty"], zoom)
        return {"x": google["tx"], "y": google["ty"], "zoom": zoom}

    def get_tile_extent_geographic(self, x, y, zoom):
        tms = self.gm.TMSTile(x, y, zoom)
        tile_bounds = self.gm.TileBounds(tms["tx"], tms["ty"], zoom)
        return {
            "lowerLeft": self.gm.MetersToLatLon(
                tile_bounds["minx"], tile_bounds["miny"]
            ),
            "upperRight": self.gm.MetersToLatLon(
                tile_bounds["maxx"], tile_bounds["maxy"]
            ),
        }

    def get_tile_extent_pixels(self, x, y, zoom):
        tms = self.gm.TMSTile(x, y, zoom)
        tile_bounds = self.gm.TileBounds(tms["tx"], tms["ty"], zoom)
        return {
            "lowerLeft": self.gm.MetersToPixels(
                tile_bounds["minx"], tile_bounds["miny"], zoom
            ),
            "upperRight": self.gm.MetersToPixels(
                tile_bounds["maxx"], tile_bounds["maxy"], zoom
            ),
        }

    def decode_elevation(self, lat, lon, tile_index, tile_data):
        meters = self.gm.LatLonToMeters(lat, lon)
        pixels = self.gm.MetersToPixels(meters["mx"], meters["my"], tile_index["zoom"])
        tile_pixel_extent = self.get_tile_extent_pixels(
            tile_index["x"], tile_index["y"], tile_index["zoom"]
        )

        x_offset = int(pixels["px"] - tile_pixel_extent["lowerLeft"]["px"])
        x_offset = max(0, min(tile_data.shape[1] - 1, x_offset))
        y_offset = tile_data.shape[0] - int(
            pixels["py"] - tile_pixel_extent["lowerLeft"]["py"]
        )
        y_offset = max(0, min(tile_data.shape[0] - 1, y_offset))

        image_data_index = y_offset * (tile_data.shape[1] * 4) + x_offset * 4
        red = tile_data[y_offset, x_offset, 0]
        green = tile_data[y_offset, x_offset, 1]
        blue = tile_data[y_offset, x_offset, 2]

        return -10000 + ((red * 256 * 256 + green * 256 + blue) * 0.1)


elevation_provider = ElevationProvider(MAPTILER_API_KEY)
