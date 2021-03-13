# AIR Lab Challenge
# AIR Lab has developed the OPEN ATMS API.
# You can find it here https://open-atms.airlab.aero/public-api/

# Import necessary API for this challenge
import pycurl
from io import BytesIO
import json
import warnings
warnings.simplefilter("once")

# All Variables needed for JSON query
Airports = 'https://open-atms.airlab.aero/api/v1/airac/airports'
SIDs = 'https://open-atms.airlab.aero/api/v1/airac/sids/airport/'
STARs = 'https://open-atms.airlab.aero/api/v1/airac/stars/airport/'
key = ['api-key: lgBaEkJ1TLQrwFDhtwe2mqLWIgoiyxue9kmrNkvOKpdjfhyXHIcdw7MNLmTLopH6']
dict_key_icao = 'icao'
dict_key_waypoints = 'waypoints'
dic_key_name = 'name'

# Airports
# GET : Endpoints for retrieving airport records
def GET_ICAO_of_Airports():
    """
    Use OPEN ATMS API to get Aiports JSON object.
    It shall return a list of dictionary of airport
    records. Extract only Airport ICAO from this
    JSON object.
    :return: list of Airports ICAO
    """

    # Initiate the objects needed
    b_obj = BytesIO()
    crl = pycurl.Curl()
    icao = []

    # Retrieving airports records via JSON
    # At the end of this query, the API shall
    # return endpoints for retrieving airport
    # records
    crl.setopt(crl.URL, Airports)
    crl.setopt(crl.HTTPHEADER, key)
    crl.setopt(crl.WRITEFUNCTION, b_obj.write)
    crl.perform()
    crl.close()

    list_of_airports = json.loads(b_obj.getvalue())

    # Get the Airport by ICAO and append in
    # in a list
    for element in list_of_airports:
        icao.append(element[dict_key_icao])

    return icao

# SID
# Endpoints for retrieving SID (Standard Instrumentation Departure) records
def GET_SID(icao):
    """
    Use OPEN ATMS API to get Aiports SID JSON object.
    It shall return a list of dictionary of SIDs
    records.
    :param icao: Airport ICAO
    :return: SID JSON object based on specific Airport ICAO
    """

    # Initiate the objects needed
    b_obj = BytesIO()
    crl = pycurl.Curl()

    # Retrieving SID records via JSON
    # At the end of this query, the API shall
    # return endpoints for retrieving SID
    # (Standard Instrumentation Departure) records
    crl.setopt(crl.URL, SIDs + icao)
    crl.setopt(crl.HTTPHEADER, key)
    crl.setopt(crl.WRITEFUNCTION, b_obj.write)
    crl.perform()
    crl.close()

    return json.loads(b_obj.getvalue())

# STAR
# Endpoints for retrieving STAR (Standard Terminal Arrival Routes) records
def GET_STAR(icao):
    """
    Use OPEN ATMS API to get Aiports STAR JSON object.
    It shall return a list of dictionary of STARs
    records.
    :param icao: Airport ICAO
    :return: STAR JSON object based on specific Airport ICAO
    """
    # Initiate the objects needed
    b_obj = BytesIO()
    crl = pycurl.Curl()

    # Retrieving STAR records via JSON
    # At the end of this query, the API shall
    # return endpoints retrieving STAR
    # (Standard Terminal Arrival Routes) records
    crl.setopt(crl.URL, STARs + icao)
    crl.setopt(crl.HTTPHEADER, key)
    crl.setopt(crl.WRITEFUNCTION, b_obj.write)
    crl.perform()
    crl.close()

    return json.loads(b_obj.getvalue())

# Print Top or Bottom Waypoints
def PrintMostOrLeastWayPoints(waypoints_dictionary,
                              number,
                              WayPointType,
                              reverse=True):
    """
    Here will print the most or least waypoints either
    SID or STAR. The print will have name and total count
    :param waypoints_dictionary: Waypoints dictionary of specific ICAO
    :param number: Display to number of most or least waypoint counts
    :param WayPointType: 'SID' or 'STAR'
    :param reverse: True for most/top occurrence, False is otherwise
    :return: None
    """
    # Store Each WayPoints and count them
    WayPoints = {}
    for waypoints in waypoints_dictionary:
        for waypoint in waypoints[dict_key_waypoints]:
            if waypoint[dic_key_name] not in WayPoints:
                WayPoints[waypoint[dic_key_name]] = 1
            else:
                WayPoints[waypoint[dic_key_name]] += 1

    # Given no waypoints found
    if len(WayPoints) == 0:
        print(f'No {WayPointType} found!')
        return

    # Edge checks number is more than unique WayPoints
    if number > len(WayPoints):
        print("The number of WayPoints to print is more than available!")
        return

    # Sort based on reverse or non-reverse order
    sorted_tuple = sorted(WayPoints.items(),
                          key=lambda item: item[1],
                          reverse=reverse)

    # Print them based sorted value
    print(f'The Top {number} {WayPointType} WayPoints\n')
    for name, count in sorted_tuple[: number]:
        print(f'Name of the WayPoint: {name}')
        print(f'Total Count: {count}')


# Try call these functions and execute the challenge
# Declare variable
if __name__ == "__main__":
    sSID = 'SID'
    sSTAR = 'STAR'
    SID_Dictionary = {}
    STAR_Dictionary = {}

    Airports_ICAO = GET_ICAO_of_Airports()

    print('======================================================')
    print(f'-------------------------{sSID}--------------------------')
    print('----------Standard Instrumentation Departure----------')
    print('======================================================')

    # Get SID from Airport ICAO
    for ICAO in Airports_ICAO:
        SID_Dictionary[ICAO] = GET_SID(ICAO)

    # Print Statistics of SID
    for k, v in SID_Dictionary.items():
        print(f'Airport by ICAO: {k}')
        print('------------------------------------------------------')
        PrintMostOrLeastWayPoints(SID_Dictionary[k], 2, sSID, True)
        print('======================================================')

    print('\n')
    print('******************************************************')
    print('-------------------------END--------------------------')
    print('******************************************************')
    print('\n')

    print('======================================================')
    print(f'-------------------------{sSTAR}--------------------------')
    print('-----------Standard Terminal Arrival Routes-----------')
    print('======================================================')

    # Get STAR from Airport ICAO
    for ICAO in Airports_ICAO:
        STAR_Dictionary[ICAO] = GET_STAR(ICAO)

    # Print Statistics of STAR
    for k, v in STAR_Dictionary.items():
        print(f'Airport by ICAO: {k}')
        print('------------------------------------------------------')
        PrintMostOrLeastWayPoints(STAR_Dictionary[k], 2, sSTAR, True)
        print('======================================================')

    print('\n')
    print('******************************************************')
    print('-------------------------END--------------------------')
    print('******************************************************')
    print('\n')
