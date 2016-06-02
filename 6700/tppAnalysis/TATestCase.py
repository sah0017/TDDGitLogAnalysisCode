'''
Created on May 24, 2016

@author: susanha
'''


class TATestCase(object):
    '''
    classdocs
    '''
    TATestCase1 = "test200_010_ShouldGetSightingsFileWithOneElement"
    TATestCaseDict = {"test100_010_ShouldConstructFix":2,
                      "test200_010_ShouldGetSightingsFileWithOneElement":14, 
                      "test200_020_ShouldGetSightingsFileWithTwoElements":24, 
                      "test200_030_ShouldGetSightingsFileWithNoElements":4,
                      "test200_900_ShouldRaiseExceptionOnMissingFile":7,
                      "test200_910_ShouldRaiseExceptionBadSighting":6,
                      "test100_010_ShouldConstructSighting":12,
                      "test100_020_ShouldConstructSightingWithDefaultHeight":11,
                      "test100_030_ShouldConstructSightingWithDefaultTemperature":11,
                      "test100_040_ShouldConstructSightingWithDefaultPressure":11,
                      "test100_050_ShouldConstructSightingWithDefaultHorixon":11,
                      "test100_900_ShouldFailOnMissingBody":24,
                      "test100_901_ShouldFailOnNonStringBody":15,
                      "test100_902_ShouldFailOnEmptyBody":15,
                      "test100_911_ShouldFailOnMissingDateDate":14,
                      "test100_912_ShouldFailOnMissingNondateDate":15,
                      "test100_921_ShouldFailOnMissingMissingTime":14,
                      "test100_922_ShouldFailOnMissingNontimeTime":15,
                      "test100_931_ShouldFailOnMissingAltitude":14,
                      "test100_932_ShouldFailOnMalformedAltitude":15,
                      "test100_933_ShouldFailOnBelowBoundAltitudeDegrees":15,
                      "test100_934_ShouldFailOnAboveBoundAltitudeDegrees":15,
                      "test100_935_ShouldFailOnBadAltitudeDegrees":15,
                      "test100_936_ShouldFailOnBelowBoundAltitudeMinutes":15,
                      "test100_937_ShouldFailOnAboveBoundAltitudeMinutes":15,
                      "test100_938_ShouldFailOnAboveInvalidAltitudeMinutes":15,
                      "test100_942_ShouldFailOnBelowBoundHeight":15,
                      "test100_943_ShouldFailOnBelowInvalidHeight":15,
                      "test100_951_ShouldFailOnBelowBoundTemperature":15,
                      "test100_952_ShouldFailOnAboveBoundTemperature":15,
                      "test100_953_ShouldFailOnAboveInvalidTemperature":15,
                      "test100_961_ShouldFailOnBelowBoundPressure":15,
                      "test100_962_ShouldFailOnAboveBoundPressure":15,
                      "test100_963_ShouldFailOnAboveInvalidTemperature":15,
                      "test200_010_ShouldGetAllValues":19,
                      "test200_010_ShouldGetDefaultValues":11,
                      "test300_010_ShouldGetAltitudeCorrectionForArtificialHorizon":13,
                      "test300_020_ShouldGetAltitudeCorrectionForNaturalHorizon":14,
                      "test300_910_ShouldFailOnLowAltitude":15,
                      "test100_010_ShouldInstiantiateLatitude":2,
                      "test100_900_ShouldRaiseExceptionOnNonIntDegrees":6,
                      "test100_910_ShouldRaiseExceptionOnNonNumericalDegrees":6,
                      "test100_920_ShouldRaiseExceptionOnBelowBoundDegrees":6,
                      "test100_930_ShouldRaiseExceptionOnAboveBoundDegrees":6,
                      "test100_940_ShouldRaiseExceptionMissingDegrees":6,
                      "test100_950_ShouldRaiseExceptionOnNonNumericalDegrees":6,
                      "test100_952_ShouldRaiseExceptionOnBelowBoundDegrees":6,
                      "test100_954_ShouldRaiseExceptionOnAboveBoundDegrees":6,
                      "test100_956_ShouldRaiseExceptionMissingDegrees":6,
                      "test100_960_ShouldRaiseExceptionOnBadHemisphere":6,
                      "test100_962_ShouldRaiseExceptionOnEmptyHemisphere":6,
                      "test200_010_ShouldGetCorrectDegrees":5,
                      "test200_020_ShouldGetCorrectDegrees":5,
                      "test200_030_ShouldGetCorrectDegrees":5,
                      "test100_010_ShouldCalculateGhaForNominalCase":19,
                      "test100_020_ShouldCalculateGhaForOnHourCase":19,
                      "test100_030_ShouldCalculateGhaForOnPartialHourCase":19,
                      "test100_030_ShouldCalculateGhaForOnEndOfDayBoundary":19,
                      "test100_900_ShouldFailOnMissingAriesFile":16,
                      "test100_910_ShouldFailOnMissingAriesParm":16,
                      "test100_920_ShouldFailOnNoAriesTimeFound":16,
                      "test100_930_ShouldFailOnMissingStarFile":16,
                      "test100_940_ShouldFailOnMissingStarFileParm":16,
                      "test100_950_ShouldFailOnStarNotFound":16}

    def __init__(self):
        '''
        Constructor
        '''
        pass        