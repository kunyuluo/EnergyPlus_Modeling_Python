fan_pressure_rise_default = 500  # Pa
autosize = 'Autosize'
schedule_always_on = 'Always On Discrete'
schedule_always_on_hvac = 'Always On Discrete hvac_library'

func_by_type = {
    'ApartmentHighRise': 'sort_zone_by_floor_1',
    'ApartmentMidRise': 'sort_zone_by_floor_1',
    'Hospital': 'sort_zone_by_floor_2',
    'HotelLarge': 'sort_zone_by_floor_2',
    'HotelSmall': 'sort_zone_by_floor_5',
    'OfficeLarge': 'sort_zone_by_floor_3',
    'OfficeMedium': 'sort_zone_by_floor_3',
    'OfficeSmall': 'sort_zone_by_floor_6',
    'OutPatientHealthCare': 'sort_zone_by_floor_4',
    'RestaurantFastFood': 'sort_zone_by_floor_6',
    'RestaurantSitDown': 'sort_zone_by_floor_6',
    'RetailStandalone': 'sort_zone_by_floor_6',
    'RetailStripmall': 'sort_zone_by_floor_6',
    'SchoolPrimary': 'sort_zone_by_floor_2',
    'SchoolSecondary': 'sort_zone_by_floor_2',
    'Warehouse': 'sort_zone_by_floor_6',
}
