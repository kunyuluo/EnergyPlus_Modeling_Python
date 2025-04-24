import os
import numpy as np


def format_date(date: str):
    try:
        items = date.split("/")
        if len(items) == 2:
            month = items[0]
            day = items[1]
            new_date = month + "/ " + day if len(day) == 1 else month + "/" + day
            return new_date
        elif len(items) == 3:
            month = items[1]
            day = items[2]
            new_date = month + "/ " + day if len(day) == 1 else month + "/" + day
            return new_date
        else:
            raise ValueError("Invalid input value of date.")
    except ValueError:
        raise ValueError("Invalid input value of date.")


class Location:
    def __init__(
            self,
            city: str = "Shanghai",
            province: str = "-",
            country: str = "CHN",
            latitude: float = 31.17,
            longitude: float = 121.43,
            timezone: float = 8,
            elevation: float = 7.0,
            source: str = "IWEC",
            wmo: str = "583620"):

        self._city = city
        self._province = province
        self._country = country
        self._source = source
        self._wmo = wmo
        self._latitude = latitude
        self._longitude = longitude
        self._timezone = timezone
        self._elevation = elevation

    @property
    def city(self):
        return self._city

    @property
    def province(self):
        return self._province

    @property
    def country(self):
        return self._country

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def timezone(self):
        return self._timezone

    @property
    def elevation(self):
        return self._elevation

    @classmethod
    def from_dict(cls, location):
        keys = ['city', 'state', 'country', 'latitude', 'longitude', 'time_zone', 'elevation']

        if isinstance(location, dict):
            for key in keys:
                if key not in keys:
                    location[key] = None

            return cls(location['city'], location['state'], location['country'], location['latitude'],
                       location['longitude'], location['time_zone'], location['elevation'])
        else:
            raise TypeError("Invalid input type if location dictionary.")

    @classmethod
    def from_string(cls, location_string: str):
        items = location_string.split("LOCATION,")[1].split(",")

        return cls(items[0], items[1], items[2], float(items[5]), float(items[6]), float(items[7]), float(items[8]),
                   items[3], items[4])

    def to_dict(self):
        return {
            "city": self._city,
            "province": self._province,
            "country": self._country,
            "latitude": self._latitude,
            "longitude": self._longitude,
            "time_zone": self._timezone,
            "elevation": self._elevation,
            "source": self._source,
            "wmo": self._wmo
        }

    def to_string(self):
        string = "LOCATION" + "," + self._city.upper() + "," + self._province.upper() + "," + \
                 self._country.upper() + "," + self._source + "," + self._wmo + "," + \
                 str(self._latitude) + "," + str(self._longitude) + "," + \
                 str(self._timezone) + "," + str(self._elevation)
        return string


class HeatingDesignCondition:
    def __init__(
            self,
            coldest_month: int = 1,
            dry_bulb_temp_996: float = -2,
            dry_bulb_temp_990: float = -0.6,
            dew_point_temp_996: float = -12.9,
            humidity_ratio_996: float = 1.2,
            mean_coincident_dry_bulb_temp_996: float = 1.2,
            dew_point_temp_990: float = -10.3,
            humidity_ratio_990: float = 1.6,
            mean_coincident_dry_bulb_temp_990: float = 2.1,
            wind_speed_04: float = 7.9,
            mean_coincident_dry_bulb_temp_04: float = 4.8,
            wind_speed_1: float = 7.3,
            mean_coincident_dry_bulb_temp_1: float = 4.6,
            mean_wind_speed_996: float = 2.9,
            wind_direction_996: float = 270):
        """
        :param coldest_month: Coldest month (i.e., month with lowest average dry-bulb temperature;
        1 = January, 12 = December).
        :param dry_bulb_temp_996: Dry-bulb temperature corresponding to 99.6% annual cumulative frequency of occurrence
         (cold conditions), °C.
        :param dry_bulb_temp_990: Dry-bulb temperature corresponding to 99.0% annual cumulative frequency of occurrence
         (cold conditions), °C.
        :param dew_point_temp_996: Dew-point temperature corresponding to 99.6%, °C
        :param humidity_ratio_996: humidity ratio corresponding to 99.6% (g/kg)
        :param mean_coincident_dry_bulb_temp_996: mean coincident dry bulb temperature corresponding to 99.6% (g/kg)
        :param dew_point_temp_990: Dew-point temperature corresponding to 99.0%, °C
        :param humidity_ratio_990: humidity ratio corresponding to 99.0% (g/kg)
        :param mean_coincident_dry_bulb_temp_990: mean coincident dry bulb temperature corresponding to 99.0% (g/kg)
        :param wind_speed_04: Wind speed corresponding to 0.4% cumulative frequency of occurrence for coldest month, m/s
        :param wind_speed_1: Wind speed corresponding to 1.0% cumulative frequency of occurrence for coldest month, m/s
        :param mean_coincident_dry_bulb_temp_04: mean coincident dry-bulb temperature corresponding to 0.4%
        :param mean_coincident_dry_bulb_temp_1: mean coincident dry-bulb temperature corresponding to 1.0%
        :param mean_wind_speed_996: Mean wind speed coincident with 99.6% dry-bulb temperature, m/s.
        :param wind_direction_996: corresponding most frequent wind direction, degrees from north (east = 90°).
        """

        self._coldest_month = coldest_month
        self._dry_bulb_temp_996 = dry_bulb_temp_996
        self._dry_bulb_temp_990 = dry_bulb_temp_990
        self._dew_point_temp_996 = dew_point_temp_996
        self._humidity_ratio_996 = humidity_ratio_996
        self._mean_coincident_dry_bulb_temp_996 = mean_coincident_dry_bulb_temp_996
        self._dew_point_temp_990 = dew_point_temp_990
        self._humidity_ratio_990 = humidity_ratio_990
        self._mean_coincident_dry_bulb_temp_990 = mean_coincident_dry_bulb_temp_990
        self._wind_speed_04 = wind_speed_04
        self._mean_coincident_dry_bulb_temp_04 = mean_coincident_dry_bulb_temp_04
        self._wind_speed_1 = wind_speed_1
        self._mean_coincident_dry_bulb_temp_1 = mean_coincident_dry_bulb_temp_1
        self._mean_wind_speed_996 = mean_wind_speed_996
        self._wind_direction_996 = wind_direction_996

    @property
    def coldest_month(self):
        return self._coldest_month

    @property
    def dry_bulb_temp_996(self):
        return self._dry_bulb_temp_996

    @property
    def dry_bulb_temp_990(self):
        return self._dry_bulb_temp_990

    @property
    def dew_point_temp_996(self):
        return self._dew_point_temp_996

    @property
    def humidity_ratio_996(self):
        return self._humidity_ratio_996

    @property
    def mean_coincident_dry_bulb_temp_996(self):
        return self._mean_coincident_dry_bulb_temp_996

    @property
    def dew_point_temp_990(self):
        return self._dew_point_temp_990

    @property
    def humidity_ratio_990(self):
        return self._humidity_ratio_990

    @property
    def mean_coincident_dry_bulb_temp_990(self):
        return self._mean_coincident_dry_bulb_temp_990

    @property
    def wind_speed_04(self):
        return self._wind_speed_04

    @property
    def mean_coincident_dry_bulb_temp_04(self):
        return self._mean_coincident_dry_bulb_temp_04

    @property
    def wind_speed_1(self):
        return self._wind_speed_1

    @property
    def mean_coincident_dry_bulb_temp_1(self):
        return self._mean_coincident_dry_bulb_temp_1

    @property
    def mean_wind_speed_996(self):
        return self._mean_wind_speed_996

    @property
    def wind_direction_996(self):
        return self._wind_direction_996

    @classmethod
    def from_string(cls, design_condition: str):
        items = design_condition.split("Heating,")[1].split(",Cooling")[0].split(",")
        items = list(map(float, items))

        return cls(int(items[0]), items[1], items[2], items[3], items[4], items[5], items[6], items[7], items[8],
                   items[9], items[10], items[11], items[12], items[13], items[14])

    def to_string(self):
        string = "Heating" + "," + str(self._coldest_month) + "," + \
                 str(self._dry_bulb_temp_996) + "," + str(self._dry_bulb_temp_990) + "," + \
                 str(self._dew_point_temp_996) + "," + str(self._humidity_ratio_996) + "," + \
                 str(self._mean_coincident_dry_bulb_temp_996) + "," + str(self._dew_point_temp_990) + "," + \
                 str(self._humidity_ratio_990) + "," + str(self._mean_coincident_dry_bulb_temp_990) + "," + \
                 str(self._wind_speed_04) + "," + str(self._mean_coincident_dry_bulb_temp_04) + "," + \
                 str(self._wind_speed_1) + "," + str(self._mean_coincident_dry_bulb_temp_1) + "," + \
                 str(self._mean_wind_speed_996) + "," + str(self._wind_direction_996)
        return string


class CoolingDesignCondition:
    def __init__(
            self,
            hottest_month: int = 7,
            hottest_month_dry_bulb_temp_range: float = 5.6,
            dry_bulb_temp_04: float = 35.1,
            mean_coincident_wet_bulb_temp_04: float = 26.9,
            dry_bulb_temp_1: float = 33.8,
            mean_coincident_wet_bulb_temp_1: float = 26.6,
            dry_bulb_temp_2: float = 32.6,
            mean_coincident_wet_bulb_temp_2: float = 26.3,
            wet_bulb_temp_04: float = 27.9,
            mean_coincident_dry_bulb_temp_04_evap: float = 32.5,
            wet_bulb_temp_1: float = 27.4,
            mean_coincident_dry_bulb_temp_1_evap: float = 31.7,
            wet_bulb_temp_2: float = 27,
            mean_coincident_dry_bulb_temp_2_evap: float = 31.1,
            mean_wind_speed_04: float = 3.6,
            wind_direction_04: float = 220,
            dew_point_temp_04: float = 26.7,
            humidity_ratio_04: float = 22.3,
            mean_coincident_dry_bulb_temp_04_dehum: float = 30.4,
            dew_point_temp_1: float = 26.2,
            humidity_ratio_1: float = 21.7,
            mean_coincident_dry_bulb_temp_1_dehum: float = 29.9,
            dew_point_temp_2: float = 25.8,
            humidity_ratio_2: float = 21.2,
            mean_coincident_dry_bulb_temp_2_dehum: float = 29.6,
            enthalpy_04: float = 89.4,
            mean_coincident_dry_bulb_temp_04_enth: float = 32.7,
            enthalpy_1: float = 87.1,
            mean_coincident_dry_bulb_temp_1_enth: float = 32,
            enthalpy_2: float = 85.2,
            mean_coincident_dry_bulb_temp_2_enth: float = 31.2,
            hours_8_to_4_db_12_to_20: int = 724):

        self._hottest_month = hottest_month
        self._hottest_month_dry_bulb_temp_range = hottest_month_dry_bulb_temp_range
        self._dry_bulb_temp_04 = dry_bulb_temp_04
        self._mean_coincident_wet_bulb_temp_04 = mean_coincident_wet_bulb_temp_04
        self._dry_bulb_temp_1 = dry_bulb_temp_1
        self._mean_coincident_wet_bulb_temp_1 = mean_coincident_wet_bulb_temp_1
        self._dry_bulb_temp_2 = dry_bulb_temp_2
        self._mean_coincident_wet_bulb_temp_2 = mean_coincident_wet_bulb_temp_2
        self._wet_bulb_temp_04 = wet_bulb_temp_04
        self._mean_coincident_dry_bulb_temp_04_evap = mean_coincident_dry_bulb_temp_04_evap
        self._wet_bulb_temp_1 = wet_bulb_temp_1
        self._mean_coincident_dry_bulb_temp_1_evap = mean_coincident_dry_bulb_temp_1_evap
        self._wet_bulb_temp_2 = wet_bulb_temp_2
        self._mean_coincident_dry_bulb_temp_2_evap = mean_coincident_dry_bulb_temp_2_evap
        self._mean_wind_speed_04 = mean_wind_speed_04
        self._wind_direction_04 = wind_direction_04
        self._dew_point_temp_04 = dew_point_temp_04
        self._humidity_ratio_04 = humidity_ratio_04
        self._mean_coincident_dry_bulb_temp_04_dehum = mean_coincident_dry_bulb_temp_04_dehum
        self._dew_point_temp_1 = dew_point_temp_1
        self._humidity_ratio_1 = humidity_ratio_1
        self._mean_coincident_dry_bulb_temp_1_dehum = mean_coincident_dry_bulb_temp_1_dehum
        self._dew_point_temp_2 = dew_point_temp_2
        self._humidity_ratio_2 = humidity_ratio_2
        self._mean_coincident_dry_bulb_temp_2_dehum = mean_coincident_dry_bulb_temp_2_dehum
        self._enthalpy_04 = enthalpy_04
        self._mean_coincident_dry_bulb_temp_04_enth = mean_coincident_dry_bulb_temp_04_enth
        self._enthalpy_1 = enthalpy_1
        self._mean_coincident_dry_bulb_temp_1_enth = mean_coincident_dry_bulb_temp_1_enth
        self._enthalpy_2 = enthalpy_2
        self._mean_coincident_dry_bulb_temp_2_enth = mean_coincident_dry_bulb_temp_2_enth
        self._hours_8_to_4_db_12_to_20 = hours_8_to_4_db_12_to_20

    @property
    def hottest_month(self):
        return self._hottest_month

    @property
    def hottest_month_dry_bulb_temp_range(self):
        return self._hottest_month_dry_bulb_temp_range

    @property
    def dry_bulb_temp_04(self):
        return self._dry_bulb_temp_04

    @property
    def mean_coincident_wet_bulb_temp_04(self):
        return self._mean_coincident_wet_bulb_temp_04

    @property
    def dry_bulb_temp_1(self):
        return self._dry_bulb_temp_1

    @property
    def mean_coincident_wet_bulb_temp_1(self):
        return self._mean_coincident_wet_bulb_temp_1

    @property
    def dry_bulb_temp_2(self):
        return self._dry_bulb_temp_2

    @property
    def mean_coincident_wet_bulb_temp_2(self):
        return self._mean_coincident_wet_bulb_temp_2

    @property
    def wet_bulb_temp_04(self):
        return self._wet_bulb_temp_04

    @property
    def mean_coincident_dry_bulb_temp_04_evap(self):
        return self._mean_coincident_dry_bulb_temp_04_evap

    @property
    def wet_bulb_temp_1(self):
        return self._wet_bulb_temp_1

    @property
    def mean_coincident_dry_bulb_temp_1_evap(self):
        return self._mean_coincident_dry_bulb_temp_1_evap

    @property
    def wet_bulb_temp_2(self):
        return self._wet_bulb_temp_2

    @property
    def mean_coincident_dry_bulb_temp_2_evap(self):
        return self._mean_coincident_dry_bulb_temp_2_evap

    @property
    def mean_wind_speed_04(self):
        return self._mean_wind_speed_04

    @property
    def wind_direction_04(self):
        return self._wind_direction_04

    @property
    def dew_point_temp_04(self):
        return self._dew_point_temp_04

    @property
    def humidity_ratio_04(self):
        return self._humidity_ratio_04

    @property
    def mean_coincident_dry_bulb_temp_04_dehum(self):
        return self._mean_coincident_dry_bulb_temp_04_dehum

    @property
    def dew_point_temp_1(self):
        return self._dew_point_temp_1

    @property
    def humidity_ratio_1(self):
        return self._humidity_ratio_1

    @property
    def mean_coincident_dry_bulb_temp_1_dehum(self):
        return self._mean_coincident_dry_bulb_temp_1_dehum

    @property
    def dew_point_temp_2(self):
        return self._dew_point_temp_2

    @property
    def humidity_ratio_2(self):
        return self._humidity_ratio_2

    @property
    def mean_coincident_dry_bulb_temp_2_dehum(self):
        return self._mean_coincident_dry_bulb_temp_2_dehum

    @property
    def enthalpy_04(self):
        return self._enthalpy_04

    @property
    def mean_coincident_dry_bulb_temp_04_enth(self):
        return self._mean_coincident_dry_bulb_temp_04_enth

    @property
    def enthalpy_1(self):
        return self._enthalpy_1

    @property
    def mean_coincident_dry_bulb_temp_1_enth(self):
        return self._mean_coincident_dry_bulb_temp_1_enth

    @property
    def enthalpy_2(self):
        return self._enthalpy_2

    @property
    def mean_coincident_dry_bulb_temp_2_enth(self):
        return self._mean_coincident_dry_bulb_temp_2_enth

    @property
    def hours_8_to_4_db_12_to_20(self):
        return self._hours_8_to_4_db_12_to_20

    @classmethod
    def from_string(cls, design_condition: str):
        items = design_condition.split("Cooling,")[1].split(",Extremes")[0].split(",")
        items = list(map(float, items))

        return cls(int(items[0]), items[1], items[2], items[3], items[4], items[5], items[6], items[7], items[8],
                   items[9], items[10], items[11], items[12], items[13], items[14], items[15], items[16], items[17],
                   items[18], items[19], items[20], items[21], items[22], items[23], items[24], items[25], items[26],
                   items[27], items[28], items[29], items[30], int(items[31]))

    def to_string(self):
        string = "Cooling" + "," + str(self._hottest_month) + "," + \
                 str(self._hottest_month_dry_bulb_temp_range) + "," + \
                 str(self._dry_bulb_temp_04) + "," + str(self._mean_coincident_wet_bulb_temp_04) + "," + \
                 str(self._dry_bulb_temp_1) + "," + str(self._mean_coincident_wet_bulb_temp_1) + "," + \
                 str(self._dry_bulb_temp_2) + "," + str(self._mean_coincident_wet_bulb_temp_2) + "," + \
                 str(self._wet_bulb_temp_04) + "," + str(self._mean_coincident_dry_bulb_temp_04_evap) + "," + \
                 str(self._wet_bulb_temp_1) + "," + str(self._mean_coincident_dry_bulb_temp_1_evap) + "," + \
                 str(self._wet_bulb_temp_2) + "," + str(self._mean_coincident_dry_bulb_temp_2_evap) + "," + \
                 str(self._mean_wind_speed_04) + "," + str(self._wind_direction_04) + "," + \
                 str(self._dew_point_temp_04) + "," + str(self._humidity_ratio_04) + "," + \
                 str(self._mean_coincident_dry_bulb_temp_04_dehum) + "," + \
                 str(self._dew_point_temp_1) + "," + str(self._humidity_ratio_1) + "," + \
                 str(self._mean_coincident_dry_bulb_temp_1_dehum) + "," + \
                 str(self._dew_point_temp_2) + "," + str(self._humidity_ratio_2) + "," + \
                 str(self._mean_coincident_dry_bulb_temp_2_dehum) + "," + \
                 str(self._enthalpy_04) + "," + str(self._mean_coincident_dry_bulb_temp_04_enth) + "," + \
                 str(self._enthalpy_1) + "," + str(self._mean_coincident_dry_bulb_temp_1_enth) + "," + \
                 str(self._enthalpy_2) + "," + str(self._mean_coincident_dry_bulb_temp_2_enth) + "," + \
                 str(self._hours_8_to_4_db_12_to_20)
        return string


class ExtremeDesignCondition:
    def __init__(
            self,
            wind_speed_1: float = 7.6,
            wind_speed_2: float = 6.8,
            wind_speed_5: float = 6.1,
            max_wet_bulb_temp: float = 30.1,
            mean_min_dry_bulb_temp: float = -3.9,
            mean_max_dry_bulb_temp: float = 37,
            deviation_min_dry_bulb_temp: float = 1.3,
            deviation_max_dry_bulb_temp: float = 1.1,
            min_extreme_dry_bulb_temp_5_year: float = -4.8,
            max_extreme_dry_bulb_temp_5_year: float = 37.8,
            min_extreme_dry_bulb_temp_10_year: float = -5.6,
            max_extreme_dry_bulb_temp_10_year: float = 38.5,
            min_extreme_dry_bulb_temp_20_year: float = -6.3,
            max_extreme_dry_bulb_temp_20_year: float = 39.1,
            min_extreme_dry_bulb_temp_50_year: float = -7.3,
            max_extreme_dry_bulb_temp_50_year: float = 39.9):
        self._wind_speed_1 = wind_speed_1
        self._wind_speed_2 = wind_speed_2
        self._wind_speed_5 = wind_speed_5
        self._max_wet_bulb_temp = max_wet_bulb_temp
        self._mean_min_dry_bulb_temp = mean_min_dry_bulb_temp
        self._mean_max_dry_bulb_temp = mean_max_dry_bulb_temp
        self._deviation_min_dry_bulb_temp = deviation_min_dry_bulb_temp
        self._deviation_max_dry_bulb_temp = deviation_max_dry_bulb_temp
        self._min_extreme_dry_bulb_temp_5_year = min_extreme_dry_bulb_temp_5_year
        self._max_extreme_dry_bulb_temp_5_year = max_extreme_dry_bulb_temp_5_year
        self._min_extreme_dry_bulb_temp_10_year = min_extreme_dry_bulb_temp_10_year
        self._max_extreme_dry_bulb_temp_10_year = max_extreme_dry_bulb_temp_10_year
        self._min_extreme_dry_bulb_temp_20_year = min_extreme_dry_bulb_temp_20_year
        self._max_extreme_dry_bulb_temp_20_year = max_extreme_dry_bulb_temp_20_year
        self._min_extreme_dry_bulb_temp_50_year = min_extreme_dry_bulb_temp_50_year
        self._max_extreme_dry_bulb_temp_50_year = max_extreme_dry_bulb_temp_50_year

    @classmethod
    def from_string(cls, design_condition: str):
        items = design_condition.split("Extremes,")[1].split(",")
        items = list(map(float, items))

        return cls(items[0], items[1], items[2], items[3], items[4], items[5], items[6], items[7], items[8],
                   items[9], items[10], items[11], items[12], items[13], items[14], items[15])

    def to_string(self):
        string = "Extremes" + "," + str(self._wind_speed_1) + "," + str(self._wind_speed_2) + "," + \
                 str(self._wind_speed_5) + "," + str(self._max_wet_bulb_temp) + "," + \
                 str(self._mean_min_dry_bulb_temp) + "," + str(self._mean_max_dry_bulb_temp) + "," + \
                 str(self._deviation_min_dry_bulb_temp) + "," + str(self._deviation_max_dry_bulb_temp) + "," + \
                 str(self._min_extreme_dry_bulb_temp_5_year) + "," + \
                 str(self._max_extreme_dry_bulb_temp_5_year) + "," + \
                 str(self._min_extreme_dry_bulb_temp_10_year) + "," + \
                 str(self._max_extreme_dry_bulb_temp_10_year) + "," + \
                 str(self._min_extreme_dry_bulb_temp_20_year) + "," + \
                 str(self._max_extreme_dry_bulb_temp_20_year) + "," + \
                 str(self._min_extreme_dry_bulb_temp_50_year) + "," + \
                 str(self._max_extreme_dry_bulb_temp_50_year)
        return string


class DesignConditions:
    def __init__(
            self,
            number_of_design_conditions: int = 1,
            design_condition_source: str = "Climate Design Data 2009 ASHRAE Handbook",
            heating_design_condition: HeatingDesignCondition = HeatingDesignCondition(),
            cooling_design_condition: CoolingDesignCondition = CoolingDesignCondition(),
            extreme_design_condition: ExtremeDesignCondition = ExtremeDesignCondition()):

        self._number_of_design_conditions = number_of_design_conditions
        self._design_condition_source = design_condition_source
        self._heating_design_condition = heating_design_condition
        self._cooling_design_condition = cooling_design_condition
        self._extreme_design_condition = extreme_design_condition

    @property
    def heating_design_condition(self):
        return self._heating_design_condition

    @property
    def cooling_design_condition(self):
        return self._cooling_design_condition

    @property
    def extreme_design_condition(self):
        return self._extreme_design_condition

    @classmethod
    def from_string(cls, design_condition: str):
        items = design_condition.split(",")

        return cls(int(items[1]), items[2],
                   HeatingDesignCondition.from_string(design_condition),
                   CoolingDesignCondition.from_string(design_condition),
                   ExtremeDesignCondition.from_string(design_condition))

    def to_string(self):
        string = "DESIGN CONDITIONS" + "," + str(self._number_of_design_conditions) + "," + \
                 self._design_condition_source + "," + "" + "," + \
                 self._heating_design_condition.to_string() + "," + \
                 self._cooling_design_condition.to_string() + "," + \
                 self._extreme_design_condition.to_string()
        return string


class ExtremePeriod:
    def __init__(self, name: str = None, period_type: int = 1, start_day: str = None, end_day: str = None):
        """
        Period_type: 1.Extreme 2.Typical \n
        Start/End Day: use format "M/D", eg. 7/13
        """

        self._name = name
        self._period_type = period_type
        self._start_day = format_date(start_day)
        self._end_day = format_date(end_day)

    @classmethod
    def from_string(cls, items: list):
        # items = extreme_period.split(",")

        return cls(items[0], items[1], items[2], items[3])

    def to_string(self):
        period_type = "Extreme" if self._period_type == 1 else "Typical"
        string = self._name + "," + period_type + "," + self._start_day + "," + self._end_day
        return string


class ExtremePeriods:
    def __init__(self, periods: list = None):
        if periods is None:
            periods = [ExtremePeriod("Summer - Week Nearest Max Temperature For Period", 1, "7/13", "7/19"),
                       ExtremePeriod("Summer - Week Nearest Average Temperature For Period", 2, "8/17", "7/23"),
                       ExtremePeriod("Winter - Week Nearest Min Temperature For Period", 1, "1/20", "1/26"),
                       ExtremePeriod("Winter - Week Nearest Average Temperature For Period", 2, "12/22", "12/28"),
                       ExtremePeriod("Autumn - Week Nearest Average Temperature For Period", 2, "11/3", "11/9"),
                       ExtremePeriod("Spring - Week Nearest Average Temperature For Period", 2, "4/12", "4/18")]

        self._periods = periods

    @classmethod
    def from_string(cls, extreme_period: str):
        step = 4
        items = extreme_period.split(",")[2:]
        batch = int(len(items) / step)
        periods = []
        for i in range(batch):
            start_index = i * step
            end_index = start_index + step
            period = ExtremePeriod.from_string(items[start_index:end_index])
            periods.append(period)

        return cls(periods)

    def to_string(self):
        string = ""
        if len(self._periods) > 0:
            number_of_periods = len(self._periods)
            for i, period in enumerate(self._periods):
                if isinstance(period, ExtremePeriod):
                    if i == len(self._periods) - 1:
                        string = string + period.to_string()
                    else:
                        string = string + period.to_string() + ","
        else:
            number_of_periods = 0

        string = "TYPICAL/EXTREME PERIODS" + "," + str(number_of_periods) + "," + string
        return string


class GroundTemperature:
    def __init__(
            self,
            depth: float = 0.5,
            jan_temp: float = 15,
            feb_temp: float = 15,
            mar_temp: float = 15,
            apr_temp: float = 15,
            may_temp: float = 15,
            jun_temp: float = 15,
            jul_temp: float = 15,
            aug_temp: float = 15,
            sep_temp: float = 15,
            oct_temp: float = 15,
            nov_temp: float = 15,
            dec_temp: float = 15,
            soil_conductivity: float = "",
            soil_density: float = "",
            soil_specific_heat: float = "", ):
        self._depth = depth
        self._soil_conductivity = soil_conductivity
        self._soil_density = soil_density
        self._soil_specific_heat = soil_specific_heat
        self._jan_temp = jan_temp
        self._feb_temp = feb_temp
        self._mar_temp = mar_temp
        self._apr_temp = apr_temp
        self._may_temp = may_temp
        self._jun_temp = jun_temp
        self._jul_temp = jul_temp
        self._aug_temp = aug_temp
        self._sep_temp = sep_temp
        self._oct_temp = oct_temp
        self._nov_temp = nov_temp
        self._dec_temp = dec_temp

    @classmethod
    def from_string(cls, items: list):
        return cls(items[0], items[4], items[5], items[6], items[7], items[8], items[9], items[10], items[11],
                   items[12], items[13], items[14], items[15], items[1], items[2], items[3])

    def to_string(self):
        string = str(self._depth) + "," + str(self._soil_conductivity) + "," + \
                 str(self._soil_density) + "," + str(self._soil_specific_heat) + "," + \
                 str(self._jan_temp) + "," + str(self._feb_temp) + "," + str(self._mar_temp) + "," + \
                 str(self._apr_temp) + "," + str(self._may_temp) + "," + str(self._jun_temp) + "," + \
                 str(self._jul_temp) + "," + str(self._aug_temp) + "," + str(self._sep_temp) + "," + \
                 str(self._oct_temp) + "," + str(self._nov_temp) + "," + str(self._dec_temp)
        return string


class GroundTemperatures:
    def __init__(self, ground_temps: list = None):

        if ground_temps is None:
            ground_temps = [
                GroundTemperature(0.5, 5.45, 7.48, 11.43, 15.17, 22.25, 25.97, 27.00, 25.11, 20.75, 15.31, 9.95, 6.42),
                GroundTemperature(2, 8.25, 8.74, 10.99, 13.50, 18.94, 22.42, 24.15, 23.76, 21.27, 17.52, 13.29, 9.97),
                GroundTemperature(4, 11.14, 10.79, 11.77, 13.20, 16.80, 19.49, 21.23, 21.66, 20.57, 18.36, 15.49, 12.9)]

        self._ground_temps = ground_temps

    @classmethod
    def from_string(cls, ground_temp: str):
        step = 16
        items = ground_temp.split(",")[2:]
        batch = int(len(items) / step)
        ground_temps = []
        for i in range(batch):
            start_index = i * step
            end_index = start_index + step
            ground_temp = GroundTemperature.from_string(items[start_index:end_index])
            ground_temps.append(ground_temp)

        return cls(ground_temps)

    def to_string(self):
        string = ""
        if len(self._ground_temps) > 0:
            number_of_depths = len(self._ground_temps)
            for i, temps in enumerate(self._ground_temps):
                if isinstance(temps, GroundTemperature):
                    if i == len(self._ground_temps) - 1:
                        string = string + temps.to_string()
                    else:
                        string = string + temps.to_string() + ","
        else:
            number_of_depths = 0
        string = "GROUND TEMPERATURES" + "," + str(number_of_depths) + "," + string
        return string


class Holiday:
    def __init__(self, name: str = "", day: str = ""):
        """
        Day: use format "M/D", eg. 7/13
        """
        self._name = name
        self._day = format_date(day) if day != "" else day

    @classmethod
    def from_string(cls, items: list):
        return cls(items[0], items[1])

    def to_string(self):
        string = self._name + "," + self._day
        return string


class Holidays:
    def __init__(
            self,
            leap_year: bool = False,
            daylight_saving_start_day: str = "0",
            daylight_saving_end_day: str = "0",
            holidays=None):

        if holidays is None:
            holidays = []

        self._leap_year = leap_year
        self._daylight_saving_start_day = daylight_saving_start_day
        self._daylight_saving_end_day = daylight_saving_end_day
        self._holidays = holidays

    @classmethod
    def from_string(cls, holiday: str):
        number_of_holidays = holiday[4]
        holidays = []
        if number_of_holidays != 0:
            step = 2
            items = holiday.split(",")[5:]
            batch = int(len(items) / step)
            for i in range(batch):
                start_index = i * step
                end_index = start_index + step
                day = Holiday.from_string(items[start_index:end_index])
                holidays.append(day)

        leap = True if holiday[1] == "Yes" else False

        return cls(leap, holiday.split(",")[2], holiday.split(",")[3], holidays)

    def to_string(self):
        leap_year = "Yes" if self._leap_year else "No"
        holiday_string = ""
        if len(self._holidays) > 0:
            number_of_holiday = str(len(self._holidays))
            for i, holiday in enumerate(self._holidays):
                if isinstance(holiday, Holiday):
                    if i == len(self._holidays) - 1:
                        holiday_string = holiday_string + holiday.to_string()
                    else:
                        holiday_string = holiday_string + holiday.to_string() + ","
        else:
            number_of_holiday = "0"
            holiday_string = ""

        if holiday_string == "":
            string = "HOLIDAYS/DAYLIGHT SAVINGS" + "," + leap_year + "," + \
                     self._daylight_saving_start_day + "," + self._daylight_saving_end_day + "," + \
                     number_of_holiday
        else:
            string = "HOLIDAYS/DAYLIGHT SAVINGS" + "," + leap_year + "," + \
                     self._daylight_saving_start_day + "," + self._daylight_saving_end_day + "," + \
                     number_of_holiday + "," + holiday_string
        return string


class DataPeriod:
    def __init__(
            self,
            name: str = "Data",
            start_day_of_week: int = 7,
            start_day: str = "1/1",
            end_day: str = "12/31"):
        """
        Start_day_of_week: 1.Monday 2.Tuesday 3.Wednesday 4.Thursday 5.Friday 6.Saturday 7.Sunday \n
        Start/End day: use format "M/D", eg. 7/13
        """
        self._name = name
        self._start_day_of_week = start_day_of_week
        self._start_day = format_date(start_day)
        self._end_day = format_date(end_day)

    @classmethod
    def from_string(cls, items: list):
        week = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
        return cls(items[0], week[items[1]], items[2], items[3])

    def to_string(self):
        week = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
        string = self._name + "," + week[self._start_day_of_week] + "," + self._start_day + "," + self._end_day
        return string


class DataPeriods:
    def __init__(self, data_period: list = None, number_of_records_per_hour: int = 1):

        if data_period is None:
            data_period = [DataPeriod()]

        self._data_period = data_period
        self._number_of_records_per_hour = number_of_records_per_hour

    @classmethod
    def from_string(cls, data_period: str):
        step = 4
        items = data_period.split(",")[3:]
        batch = int(len(items) / step)
        periods = []
        for i in range(batch):
            start_index = i * step
            end_index = start_index + step
            period = DataPeriod.from_string(items[start_index:end_index])
            periods.append(period)

        return cls(periods)

    def to_string(self):
        period_string = ""
        if len(self._data_period) > 0:
            number_of_periods = len(self._data_period)
            for i, period in enumerate(self._data_period):
                if isinstance(period, DataPeriod):
                    if i == len(self._data_period) - 1:
                        period_string = period_string + period.to_string()
                    else:
                        period_string = period_string + period.to_string() + ","
        else:
            number_of_periods = 0

        string = "DATA PERIODS" + "," + str(number_of_periods) + "," + \
                 str(self._number_of_records_per_hour) + "," + period_string
        return string


class EPW:
    year = 2023
    minute = 0
    data_source = "C9C9C9C9*0?9?9?9?9?9?9?9*0B8B8B8B8*0*0E8*0*0"

    def __init__(
            self,
            location: Location = Location(),
            design_conditions: DesignConditions = DesignConditions(),
            extreme_periods: ExtremePeriods = ExtremePeriods(),
            ground_temps: GroundTemperatures = GroundTemperatures(),
            holidays: Holidays = Holidays(),
            comments_1: str = "",
            comments_2: str = "",
            data_periods: DataPeriods = DataPeriods(),
            dry_bulb_temps=None,
            dew_point_temps=None,
            relative_humidity=None,
            atmosphere_station_pressure=None,
            extraterrestrial_horizontal_radiation=None,
            extraterrestrial_direct_normal_radiation=None,
            horizontal_infrared_radiation_intensity=None,
            global_horizontal_radiation=None,
            direct_normal_radiation=None,
            diffuse_horizontal_radiation=None,
            global_horizontal_illuminance=None,
            direct_normal_illuminance=None,
            diffuse_horizontal_illuminance=None,
            zenith_luminance=None,
            wind_direction=None,
            wind_speed=None,
            total_sky_cover=None,
            opaque_sky_cover=None,
            visibility=None,
            ceiling_height=None,
            present_weather_observation=None,
            present_weather_codes=None,
            precipitable_water=None,
            aerosol_optical_depth=None,
            snow_depth=None,
            days_since_last_snowfall=None,
            albedo=None,
            liquid_precipitation_depth=None,
            liquid_precipitation_quantity=None,
            existing_file_path: str = None):

        # Assign default value for missing inputs:
        if dry_bulb_temps is None:
            dry_bulb_temps = [99.9] * 8760

        if dew_point_temps is None:
            dew_point_temps = [99.9] * 8760

        if relative_humidity is None:
            relative_humidity = [999] * 8760

        if atmosphere_station_pressure is None:
            atmosphere_station_pressure = [999999] * 8760

        if extraterrestrial_horizontal_radiation is None:
            extraterrestrial_horizontal_radiation = [9999] * 8760

        if extraterrestrial_direct_normal_radiation is None:
            extraterrestrial_direct_normal_radiation = [9999] * 8760

        if horizontal_infrared_radiation_intensity is None:
            horizontal_infrared_radiation_intensity = [9999] * 8760

        if global_horizontal_radiation is None:
            global_horizontal_radiation = [9999] * 8760

        if direct_normal_radiation is None:
            direct_normal_radiation = [0] * 8760

        if diffuse_horizontal_radiation is None:
            diffuse_horizontal_radiation = [0] * 8760

        if global_horizontal_illuminance is None:
            global_horizontal_illuminance = [999999] * 8760

        if direct_normal_illuminance is None:
            direct_normal_illuminance = [999999] * 8760

        if diffuse_horizontal_illuminance is None:
            diffuse_horizontal_illuminance = [999999] * 8760

        if zenith_luminance is None:
            zenith_luminance = [9999] * 8760

        if wind_direction is None:
            wind_direction = [999] * 8760

        if wind_speed is None:
            wind_speed = [999] * 8760

        if total_sky_cover is None:
            total_sky_cover = [99] * 8760

        if opaque_sky_cover is None:
            opaque_sky_cover = [99] * 8760

        if visibility is None:
            visibility = [9999] * 8760

        if ceiling_height is None:
            ceiling_height = [99999] * 8760

        if present_weather_observation is None:
            present_weather_observation = [9] * 8760

        if present_weather_codes is None:
            present_weather_codes = [999999999] * 8760

        if precipitable_water is None:
            precipitable_water = [999] * 8760

        if aerosol_optical_depth is None:
            aerosol_optical_depth = [0.999] * 8760

        if snow_depth is None:
            snow_depth = [999] * 8760

        if days_since_last_snowfall is None:
            days_since_last_snowfall = [99] * 8760

        if albedo is None:
            albedo = [0.0] * 8760

        if liquid_precipitation_depth is None:
            liquid_precipitation_depth = [0.0] * 8760

        if liquid_precipitation_quantity is None:
            liquid_precipitation_quantity = [0.0] * 8760

        # Pre-process: Convert number to string
        dry_bulb_temps = list(map(str, dry_bulb_temps))
        dew_point_temps = list(map(str, dew_point_temps))
        relative_humidity = list(map(str, relative_humidity))
        atmosphere_station_pressure = list(map(str, atmosphere_station_pressure))
        extraterrestrial_horizontal_radiation = list(map(str, extraterrestrial_horizontal_radiation))
        extraterrestrial_direct_normal_radiation = list(map(str, extraterrestrial_direct_normal_radiation))
        horizontal_infrared_radiation_intensity = list(map(str, horizontal_infrared_radiation_intensity))
        global_horizontal_radiation = list(map(str, global_horizontal_radiation))
        direct_normal_radiation = list(map(str, direct_normal_radiation))
        diffuse_horizontal_radiation = list(map(str, diffuse_horizontal_radiation))
        global_horizontal_illuminance = list(map(str, global_horizontal_illuminance))
        direct_normal_illuminance = list(map(str, direct_normal_illuminance))
        diffuse_horizontal_illuminance = list(map(str, diffuse_horizontal_illuminance))
        zenith_luminance = list(map(str, zenith_luminance))
        wind_direction = list(map(str, wind_direction))
        wind_speed = list(map(str, wind_speed))
        total_sky_cover = list(map(str, total_sky_cover))
        opaque_sky_cover = list(map(str, opaque_sky_cover))
        visibility = list(map(str, visibility))
        ceiling_height = list(map(str, ceiling_height))
        present_weather_observation = list(map(str, present_weather_observation))
        present_weather_codes = list(map(str, present_weather_codes))
        precipitable_water = list(map(str, precipitable_water))
        aerosol_optical_depth = list(map(str, aerosol_optical_depth))
        snow_depth = list(map(str, snow_depth))
        days_since_last_snowfall = list(map(str, days_since_last_snowfall))
        albedo = list(map(str, albedo))
        liquid_precipitation_depth = list(map(str, liquid_precipitation_depth))
        liquid_precipitation_quantity = list(map(str, liquid_precipitation_quantity))

        self._location = location
        self._design_conditions = design_conditions
        self._extreme_periods = extreme_periods
        self._ground_temps = ground_temps
        self._holidays = holidays
        self._comments_1 = comments_1 if comments_1 != "" else "Oh Yeah! Oh la la!"
        self._comments_2 = comments_2 if comments_2 != "" else " -- Ground temps produced with a standard soil " \
                                                               "diffusivity of 2.3225760E-03 {m**2/day}"
        self._data_periods = data_periods

        self._dry_bulb_temps = dry_bulb_temps
        self._dew_point_temps = dew_point_temps
        self._relative_humidity = relative_humidity
        self._atmosphere_station_pressure = atmosphere_station_pressure
        self._extraterrestrial_horizontal_radiation = extraterrestrial_horizontal_radiation
        self._extraterrestrial_direct_normal_radiation = extraterrestrial_direct_normal_radiation
        self._horizontal_infrared_radiation_intensity = horizontal_infrared_radiation_intensity
        self._global_horizontal_radiation = global_horizontal_radiation
        self._direct_normal_radiation = direct_normal_radiation
        self._diffuse_horizontal_radiation = diffuse_horizontal_radiation
        self._global_horizontal_illuminance = global_horizontal_illuminance
        self._direct_normal_illuminance = direct_normal_illuminance
        self._diffuse_horizontal_illuminance = diffuse_horizontal_illuminance
        self._zenith_luminance = zenith_luminance
        self._wind_direction = wind_direction
        self._wind_speed = wind_speed
        self._total_sky_cover = total_sky_cover
        self._opaque_sky_cover = opaque_sky_cover
        self._visibility = visibility
        self._ceiling_height = ceiling_height
        self._present_weather_observation = present_weather_observation
        self._present_weather_codes = present_weather_codes
        self._precipitable_water = precipitable_water
        self._aerosol_optical_depth = aerosol_optical_depth
        self._snow_depth = snow_depth
        self._days_since_last_snowfall = days_since_last_snowfall
        self._albedo = albedo
        self._liquid_precipitation_depth = liquid_precipitation_depth
        self._liquid_precipitation_quantity = liquid_precipitation_quantity
        self._existing_file_path = existing_file_path

    @property
    def location(self):
        return self._location

    @property
    def design_conditions(self):
        return self._design_conditions

    @property
    def extreme_periods(self):
        return self._extreme_periods

    @property
    def ground_temps(self):
        return self._ground_temps

    @property
    def holidays(self):
        return self._holidays

    @property
    def data_periods(self):
        return self._data_periods

    @property
    def dry_bulb_temps(self):
        return list(map(float, self._dry_bulb_temps))

    @property
    def dew_point_temps(self):
        return list(map(float, self._dew_point_temps))

    @property
    def relative_humidity(self):
        return list(map(float, self._relative_humidity))

    @property
    def atmosphere_station_pressure(self):
        return list(map(float, self._atmosphere_station_pressure))

    @property
    def extraterrestrial_horizontal_radiation(self):
        return list(map(float, self._extraterrestrial_horizontal_radiation))

    @property
    def extraterrestrial_direct_normal_radiation(self):
        return list(map(float, self._extraterrestrial_direct_normal_radiation))

    @property
    def horizontal_infrared_radiation_intensity(self):
        return list(map(float, self._horizontal_infrared_radiation_intensity))

    @property
    def global_horizontal_radiation(self):
        return list(map(float, self._global_horizontal_radiation))

    @property
    def direct_normal_radiation(self):
        return list(map(float, self._direct_normal_radiation))

    @property
    def diffuse_horizontal_radiation(self):
        return list(map(float, self._diffuse_horizontal_radiation))

    @property
    def global_horizontal_illuminance(self):
        return list(map(float, self._global_horizontal_illuminance))

    @property
    def direct_normal_illuminance(self):
        return list(map(float, self._direct_normal_illuminance))

    @property
    def diffuse_horizontal_illuminance(self):
        return list(map(float, self._diffuse_horizontal_illuminance))

    @property
    def zenith_luminance(self):
        return list(map(float, self._zenith_luminance))

    @property
    def wind_direction(self):
        return list(map(float, self._wind_direction))

    @property
    def wind_speed(self):
        return list(map(float, self._wind_speed))

    @property
    def total_sky_cover(self):
        return list(map(float, self._total_sky_cover))

    @property
    def opaque_sky_cover(self):
        return list(map(float, self._opaque_sky_cover))

    @property
    def visibility(self):
        return list(map(float, self._visibility))

    @property
    def ceiling_height(self):
        return list(map(float, self._ceiling_height))

    @property
    def present_weather_observation(self):
        return self._present_weather_observation

    @property
    def present_weather_codes(self):
        return self._present_weather_codes

    @property
    def precipitable_water(self):
        return list(map(float, self._precipitable_water))

    @property
    def aerosol_optical_depth(self):
        return list(map(float, self._aerosol_optical_depth))

    @property
    def snow_depth(self):
        return list(map(float, self._snow_depth))

    @property
    def days_since_last_snowfall(self):
        return list(map(float, self._days_since_last_snowfall))

    @property
    def albedo(self):
        return list(map(float, self._albedo))

    @property
    def liquid_precipitation_depth(self):
        return list(map(float, self._liquid_precipitation_depth))

    @property
    def liquid_precipitation_quantity(self):
        return list(map(float, self._liquid_precipitation_quantity))

    @staticmethod
    def import_from_existing(file_path):

        """
        :param file_path: file path of an existing epw weather file.
        :return: a dictionary contains all data from the file

        Index reference for output dictionary: \n
        Header: \n
        0.Location 1.Design Conditions 2.Extreme Periods 3.Ground Temperatures 4.Holidays \n
        5.Comments-1 6.Comments-2 7.Data Periods \n
        Data: \n
        0.Dry Bulb Temperature (℃) \n
        1.Dew Point Temperature (℃) \n
        2.Relative Humidity (%) \n
        3.Atmospheric Station Pressure (Pa) \n
        4.Extraterrestrial Horizontal Radiation (Wh/m2) \n
        5.Extraterrestrial Direct Normal Radiation (Wh/m2) \n
        6.Horizontal Infrared Radiation Intensity (Wh/m2) \n
        7.Global Horizontal Radiation (Wh/m2) \n
        8.Direct Normal Radiation (Wh/m2) \n
        9.Diffuse Horizontal Radiation (Wh/m2) \n
        10.Global Horizontal Illuminance (lux) \n
        11.Direct Normal Illuminance (lux) \n
        12.Diffuse Horizontal Illuminance (lux) \n
        13.Zenith Luminance (lux) \n
        14.Wind Direction (degrees) \n
        15.Wind Speed (m/s) \n
        16.Total Sky Cover (tenths of coverage) \n
        17.Opaque Sky Cover (tenths of coverage) \n
        18.Visibility (km) \n
        19.Ceiling Height (m) \n
        20.Present Weather Observation (0 or 9) \n
        21.Present Weather Codes (mm) \n
        22.Precipitable Water (mm) \n
        23.Aerosol Optical Depth (thousandths) \n
        24.Snow Depth (cm) \n
        25.Days Since Last Snowfall \n
        26.Albedo \n
        27.Liquid Precipitation Depth (mm) \n
        28.Liquid Precipitation Quantity (hr) \n
        """

        assert os.path.isfile(file_path), 'Cannot find an epw file at {}'.format(file_path)
        assert file_path.lower().endswith('epw'), '{} is not an .epw file. \n' \
                                                  'It does not possess the .epw file extension.'.format(file_path)

        try:
            data_dict = {"header": {}, "data": {}}

            with open(file_path, 'r') as epwin:
                lines = epwin.readlines()

            data_dict["header"][0] = Location.from_string(lines[0])
            data_dict["header"][1] = DesignConditions.from_string(lines[1])
            data_dict["header"][2] = ExtremePeriods.from_string(lines[2])
            data_dict["header"][3] = GroundTemperatures.from_string(lines[3])
            data_dict["header"][4] = Holidays.from_string(lines[4])
            data_dict["header"][5] = lines[5]
            data_dict["header"][6] = lines[6]
            data_dict["header"][7] = DataPeriods.from_string(lines[7])

            matrix = []
            for i in range(8, len(lines)):
                data = lines[i].split(",")
                matrix.append(data)

            weather_data = np.column_stack(matrix)
            weather_data = np.delete(weather_data, [0, 1, 2, 3, 4, 5], 0)
            # print(weather_data.shape)

            for i in range(29):
                data_dict["data"][i] = list(weather_data[i])

            return data_dict

        except ValueError:
            pass

    @classmethod
    def from_string(cls, file_path: str):
        assert os.path.isfile(file_path), 'Cannot find an epw file at {}'.format(file_path)
        assert file_path.lower().endswith('epw'), '{} is not an .epw file. \n' \
                                                  'It does not possess the .epw file extension.'.format(file_path)

        try:
            with open(file_path, 'r') as epwin:
                line = epwin.readlines()

            return line[8]
        except ValueError:
            pass

    def to_string(self):
        epw_string = self._location.to_string() + os.linesep + \
                     self._design_conditions.to_string() + os.linesep + \
                     self._extreme_periods.to_string() + os.linesep + \
                     self._ground_temps.to_string() + os.linesep + \
                     self._holidays.to_string() + os.linesep + \
                     "COMMENTS 1" + "," + self._comments_1 + os.linesep + \
                     "COMMENTS 2" + "," + self._comments_2 + os.linesep + \
                     self._data_periods.to_string() + os.linesep
        return epw_string

    def write_to_file(self, file_path: str):
        # Open the file from the given file path:
        file = open(file_path, "w+")

        # Write content line by line:
        # Header:
        # *************************************************************************
        file.writelines(self._location.to_string() + os.linesep)
        file.writelines(self._design_conditions.to_string() + os.linesep)
        file.writelines(self._extreme_periods.to_string() + os.linesep)
        file.writelines(self._ground_temps.to_string() + os.linesep)
        file.writelines(self._holidays.to_string() + os.linesep)
        file.writelines("COMMENTS 1" + "," + self._comments_1 + os.linesep)
        file.writelines("COMMENTS 2" + "," + self._comments_2 + os.linesep)
        file.writelines(self._data_periods.to_string() + os.linesep)

        # Weather Data:
        # *************************************************************************
        years = [str(self.year)] * 8760
        months = []
        days = []
        hours = []
        minutes = [str(self.minute)] * 8760
        sources = [self.data_source] * 8760

        days_of_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        for i, number in enumerate(days_of_month, 1):
            month = [str(i)] * number * 24
            months.extend(month)

            for d in range(number):
                day = [d + 1] * 24
                hour = range(1, 25)
                days.extend(day)
                hours.extend(hour)

        weather_data = np.column_stack([
            years,
            months,
            days,
            hours,
            minutes,
            sources,
            self._dry_bulb_temps,
            self._dew_point_temps,
            self._relative_humidity,
            self._atmosphere_station_pressure,
            self._extraterrestrial_horizontal_radiation,
            self._extraterrestrial_direct_normal_radiation,
            self._horizontal_infrared_radiation_intensity,
            self._global_horizontal_radiation,
            self._direct_normal_radiation,
            self._diffuse_horizontal_radiation,
            self._global_horizontal_illuminance,
            self._direct_normal_illuminance,
            self._diffuse_horizontal_illuminance,
            self._zenith_luminance,
            self._wind_direction,
            self._wind_speed,
            self._total_sky_cover,
            self._opaque_sky_cover,
            self._visibility,
            self._ceiling_height,
            self._present_weather_observation,
            self._present_weather_codes,
            self._precipitable_water,
            self._aerosol_optical_depth,
            self._snow_depth,
            self._days_since_last_snowfall,
            self._albedo,
            self._liquid_precipitation_depth,
            self._liquid_precipitation_quantity])

        for row in weather_data:
            content = ""
            for i, item in enumerate(row):
                if i == len(row) - 1:
                    content = content + item
                else:
                    content = content + item + ","
            file.write(content + os.linesep)

        # Close the file after done
        file.close()
        print("Done!")


# epw_path_str = "C:\\Users\\DELL\\Downloads\\USA_CA_Los.Angeles.Intl.AP.722950_TMY3.epw"
#
# la_epw = EPW.import_from_existing(epw_path_str)
# new_epw = EPW(dry_bulb_temps=la_epw["data"][0], dew_point_temps=la_epw["data"][1], relative_humidity=la_epw["data"][2])
#
# new_epw.write_to_file("D:\\Projects\\OpenStudioDev\\shanghai_weather.epw")
# print(epw.to_string())
