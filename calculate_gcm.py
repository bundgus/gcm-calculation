import pandas as pd
import math
import csv


def haversine(p1, p2):
    # https://gist.github.com/internaut/5a653317688b14fd0fc67214c1352831
    """
    Calculate distance between two points on earth in km
    See: http://www.movable-type.co.uk/scripts/latlong.html
    :param p1 point 1 tuple (latitude, longitude)
    :param p2 point 2 tuple (latitude, longitude)
    :return distance between points p1 and p2 on earth in km
    """
    R = 3958.7613  # earth radius in miles
    p1 = [math.radians(v) for v in p1]
    p2 = [math.radians(v) for v in p2]

    d_lat = p2[0] - p1[0]
    d_lng = p2[1] - p1[1]
    a = math.pow(math.sin(d_lat / 2), 2) + math.cos(p1[0]) * math.cos(p2[0]) * math.pow(math.sin(d_lng / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return int(R * c)


df = pd.read_csv('EC Air Service Location Pairs.csv', header=0, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

df['Distance_Miles'] = df.apply(lambda row: haversine((row['Latitude Decimal Degree Measurement_orig'],
                                                       row['Longitude Decimal Degree Measurement_orig']),
                                                      (row['Latitude Decimal Degree Measurement_dest'],
                                                       row['Longitude Decimal Degree Measurement_dest'])),
                                axis=1)
df = df.drop(['Latitude Decimal Degree Measurement_orig', 'Longitude Decimal Degree Measurement_orig',
              'Latitude Decimal Degree Measurement_dest', 'Longitude Decimal Degree Measurement_dest'], axis=1)

df = df.loc[df['Distance_Miles'] < 10000]

df.to_csv('EC Air Service Location Pairs With Distance.csv', index=False)
