import csv


# I used OOP to make code user-friendly and some additional algorithms because
# I can't be sure in correctness of all data in your csv files: in general, in data order

# user class
class User:
    def __init__(self, user_id, user_latitude, user_longitude):
        self.__id = user_id  # user id
        self.__lat = user_latitude  # user latitude
        self.__lon = user_longitude  # user longitude
        self.__zoneCount = 0  # count of available zones for user

    # getters
    def getId(self):
        return f'{self.__id}'

    def getLat(self):
        return self.__lat

    def getLon(self):
        return self.__lon

    def getZoneCount(self):
        return f'{self.__zoneCount}'

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
                #   checking wrong data
                if len(row) == 3:
                    users.append(User(int(row[0]), float(row[1]), float(row[2])))
                else:
                    print(f"Wrong user data at line {line_count + 1}")
                line_count += 1
    return users


def readZoneData():
    zones = []  # for all zones after grouping by id
    # I use dict in dict to make all vertexes in correct order
    d = dict()  # for all zones
    with open('place_zone_coordinates.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:  # for naming line
                line_count += 1
            else:
                #  checking wrong data
                if len(row) == 4:
                    if row[0] in d:  # add another vertex to zone
                        d[row[0]][int(row[3])] = [float(row[1]), float(row[2])]
                    else:   # add new zone by id
                        d[row[0]] = dict()
                        d[row[0]][int(row[3])] = [float(row[1]), float(row[2])]
                else:
                    print(f"Wrong zone data at line {line_count + 1}")
                line_count += 1

    for _d in d.keys():  # zones to list of classes
        #  checking wrong zones (lines, for example)
        if len(d.get(_d).keys()) > 2:
            lat = []
            lon = []
            for coord in d.get(_d).keys():
                lat.append(d[_d][coord][0])
                lon.append(d[_d][coord][1])
            zones.append(Zone(int(_d), lat, lon))
        else:
            print(f"Incorrect zone with {len(d.get(_d)[0])} vertexes with id: {_d}")
    return zones


# I suppose, i should use border of zone as an available area
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


def writeUserData(users):
    print("id,number_of_places_available")
    with open('result.csv', 'w') as csvfile:
        fieldnames = ['id', 'number_of_places_available']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            print(user.getId() + ',' + user.getZoneCount())
            writer.writerow(({'id': user.getId(), 'number_of_places_available': user.getZoneCount()}))


def main():
    users = readUserData()
    zones = readZoneData()

    for user in users:
        userLat = user.getLat()
        userLon = user.getLon()
        for zone in zones:
            zoneLat = zone.getLat()
            zoneLon = zone.getLon()
            if isUserInZone(userLat, userLon, zoneLat, zoneLon):
                user.addZone()

    writeUserData(users)


if __name__ == '__main__':
    main()
