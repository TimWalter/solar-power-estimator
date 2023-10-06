import math


class GlobalMercator:
    def __init__(self, tileSize):
        self.tileSize = tileSize or 256
        self.initialResolution = math.pi * 2 * 6378137 / self.tileSize
        self.originShift = math.pi * 2 * 6378137 / 2.0

    def LatLonToMeters(self, lat, lon):
        mx = lon * self.originShift / 180.0
        my = math.log(math.tan((90 + lat) * (math.pi / 360.0))) / (math.pi / 180.0)
        my = my * self.originShift / 180.0
        return {'mx': mx, 'my': my}

    def MetersToLatLon(self, mx, my):
        lon = mx / self.originShift * 180.0
        lat = my / self.originShift * 180.0
        lat = 180.0 / math.pi * (2 * math.atan(math.exp(lat * (math.pi / 180.0))) - math.pi / 2.0)
        return {'lat': lat, 'lon': lon}

    def MetersToPixels(self, mx, my, zoom):
        res = self.Resolution(zoom)
        px = (mx + self.originShift) / res
        py = (my + self.originShift) / res
        return {'px': px, 'py': py}

    def Resolution(self, zoom):
        return self.initialResolution / 2.0 ** zoom

    def TileBounds(self, tx, ty, zoom):
        minx = self.PixelsToMeters(tx * self.tileSize, ty * self.tileSize, zoom)['mx']
        miny = self.PixelsToMeters(tx * self.tileSize, ty * self.tileSize, zoom)['my']
        maxx = self.PixelsToMeters((tx + 1) * self.tileSize, (ty + 1) * self.tileSize, zoom)['mx']
        maxy = self.PixelsToMeters((tx + 1) * self.tileSize, (ty + 1) * self.tileSize, zoom)['my']
        return {'minx': minx, 'miny': miny, 'maxx': maxx, 'maxy': maxy}

    def PixelsToMeters(self, px, py, zoom):
        res = self.Resolution(zoom)
        mx = px * res - self.originShift
        my = py * res - self.originShift
        return {'mx': mx, 'my': my}

    def PixelsToTile(self, px, py):
        tx = int(math.ceil(px / self.tileSize) - 1)
        ty = int(math.ceil(py / self.tileSize) - 1)
        return {'tx': tx, 'ty': ty}

    def PixelsToRaster(self, px, py, zoom):
        mapSize = self.tileSize << zoom
        return {'x': px, 'y': mapSize - py}

    def LatLonToTile(self, lat, lon, zoom):
        meters = self.LatLonToMeters(lat, lon)
        pixels = self.MetersToPixels(meters['mx'], meters['my'], zoom)
        return self.PixelsToTile(pixels['px'], pixels['py'])

    def MetersToTile(self, mx, my, zoom):
        pixels = self.MetersToPixels(mx, my, zoom)
        return self.PixelsToTile(pixels['px'], pixels['py'])

    def GoogleTile(self, tx, ty, zoom):
        return {'tx': tx, 'ty': 2 ** zoom - 1 - ty}

    def TMSTile(self, tx, ty, zoom):
        return {'tx': tx, 'ty': 2 ** zoom - 1 - ty}

    def QuadKey(self, tx, ty, zoom):
        quadKey = ""
        ty = 2 ** zoom - 1 - ty
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i - 1)
            if (tx & mask) != 0:
                digit += 1
            if (ty & mask) != 0:
                digit += 2
            quadKey += str(digit)
        return quadKey

    def QuadKeyToTile(self, quadKey):
        tx = 0
        ty = 0
        zoom = len(quadKey)
        for i in range(zoom):
            bit = zoom - i
            mask = 1 << (bit - 1)
            if quadKey[zoom - bit] == '1':
                tx |= mask
            if quadKey[zoom - bit] == '2':
                ty |= mask
            if quadKey[zoom - bit] == '3':
                tx |= mask
                ty |= mask
        ty = 2 ** zoom - 1 - ty
        return {'tx': tx, 'ty': ty, 'zoom': zoom}
