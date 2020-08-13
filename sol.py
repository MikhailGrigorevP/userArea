import csv


# user class
class User:
    def __init__(self, user_id, user_latitude, user_longitude):
        self.__id = user_id  # user id
        self.__lat = user_latitude  # user latitude
        self.__lon = user_longitude  # user longitude
        self.__zoneCount = 0  # count of available zones for user

    # getters
    def getLat(self):
        return self.__lat

    def getLon(self):
        return self.__lon

    # setters
    def addZone(self):
        self.__zoneCount += 1

    def __repr__(self):
        return f'User ID\t{self.__id}, location: ({self.__lat}; {self.__lon}) \n\t ' \
               f'Count of available zones: {self.__zoneCount}'


class Zone:
    def __init__(self, zone_id, zone_latitude, zone_longitude):
        self.__id = zone_id  # zone id
        self.__lat = zone_latitude  # zone latitude
        self.__lon = zone_longitude  # zone longitude

    # getters
    def getLat(self):
        return self.__lat

    def getLon(self):
        return self.__lon

    def __repr__(self):
        location = ', location \n\t'
        for lat, lon in zip(self.__lat, self.__lon):
            location += f'({lat}; {lon})\n\t'
        return f'Zone ID\t{self.__id}' + location


def readUserData():
    users = []  # for all users
    with open('user_coordinates.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:  # for naming line
                line_count += 1
            else:
                users.append(User(int(row[0]), float(row[1]), float(row[2])))
                line_count += 1
    return users


def readZoneData():
    zones = []  # for all zones after grouping by id
    d = dict()  # for all zones
    with open('place_zone_coordinates.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:  # for naming line
                line_count += 1
            else:
                if row[0] in d:  # add another vertex to zone
                    d[row[0]][0].append(float(row[1]))
                    d[row[0]][1].append(float(row[2]))
                else:   # add new zone by id
                    d[row[0]] = [[float(row[1])], [float(row[2])]]
                line_count += 1

    for _d in d.keys():  # zones to list of classes
        zones.append(Zone(int(_d), d.get(_d)[0], d.get(_d)[1]))
    return zones


def isUserInZone(userLat, userLon, zoneLat, zoneLon):
    isIn = 0
    for i in range(len(zoneLat)):
        if ((zoneLon[i] <= userLon < zoneLon[i - 1])
            or (zoneLon[i - 1] <= userLon < zoneLon[i])) \
                and (userLat > (zoneLat[i - 1] - zoneLat[i])
                     * (userLon - zoneLon[i]) /
                     (zoneLon[i - 1] - zoneLon[i])
                     + zoneLat[i]): isIn = 1 - isIn
    return isIn


def main():
    users = readUserData()
    for user in users:
        print(user)
    print("\n")
    zones = readZoneData()
    #   for zone in zones:
    #       print(zone)
    print("\n == analyzing zones ==\n")

    for user in users:
        userLat = user.getLat()
        userLon = user.getLon()
        for zone in zones:
            zoneLat = zone.getLat()
            zoneLon = zone.getLon()
            if isUserInZone(userLat, userLon, zoneLat, zoneLon):
                user.addZone()
    for user in users:
        print(user)
    print("\n")


if __name__ == '__main__':
    main()
