"""
DataProcessor inherits sklearn BaseEstimator and TransformerMixin to provide a data preprocessing pipeline which can be
used as a first step in a sklearn.pipeline in order to serialize data preprocessing and model in one pickle.

By now, data transformation are as follows and can be extended as needed

- Drop alternative_id, user_id, route_id and date features
- Get dummies
- Group several destination and origin type columns
- Shuffled data

"""

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class DataProcessor(BaseEstimator, TransformerMixin):
    """
    Takes in dataframe, extracts the same dataframe with transformations as:
        - Drop alternative_id, user_id, route_id and date features
        - Get dummies
        - Group several destination and origin type columns
    """

    def __init__(self):
        pass


    def group_places_by_matcher(self, df_data, matcher, matcher_items):
        cols_origin_with_pt = [col for col in df_data.columns if 'pt_origin' in col]
        cols_destination_with_pt = [col for col in df_data.columns if 'pt_destination' in col]

        cols_origin_matching = [s for s in cols_origin_with_pt if any(xs in s for xs in matcher_items)]
        cols_destination_matching = [s for s in cols_destination_with_pt if any(xs in s for xs in matcher_items)]

        origin_matcher = 'pt_origin_' + matcher
        destination_matcher = 'pt_destination_' + matcher

        df_data[origin_matcher] = df_data[cols_origin_matching].sum(axis=1)
        df_data = df_data.drop(np.asarray(cols_origin_matching), axis=1)
        df_data[destination_matcher] = df_data[cols_destination_matching].sum(axis=1)
        df_data = df_data.drop(np.asarray(cols_destination_matching), axis=1)
        return df_data


    def process_data(self, df_data):
        print("estoy en process_data.py")
        df_data = df_data.drop(['alternative_id', 'route_id', 'user_id', 'fecha'], axis=1)
        print(list(df_data.index))

        food_places_items = ['food', 'bar', 'cafe', 'night_club', 'restaurant']
        shopping_places_items = ['bicycle_store', 'book_store', 'clothing_store', 'convenience_store',
                                 'department_store',
                                 'electronics_store', 'furniture_store', 'hardware_store', 'home_goods_store',
                                 'jewelry_store',
                                 'liquor_store', 'pet_store', 'shoe_store', 'shopping_mall', 'supermarket']

        health_places_items = ['health', 'dentist', 'doctor', 'hospital', 'veterinary_care', 'physiotherapist']
        vehicle_related_places_items = ['gas_station', 'parking']

        df_data_grouped = self.group_places_by_matcher(df_data, 'food_places', food_places_items)
        df_data_grouped = self.group_places_by_matcher(df_data_grouped, 'shopping_places', shopping_places_items)
        df_data_grouped = self.group_places_by_matcher(df_data_grouped, 'health_places', health_places_items)
        df_data_grouped = self.group_places_by_matcher(df_data_grouped, 'vehicle_places', vehicle_related_places_items)

        columns_dummies = ['day_of_week', 'day_of_week_type', 'profileName', 'traffic', 'weather', 'arrivalTimeSlot',
                           'departureTimeSlot']
        df_data_dummies = pd.get_dummies(df_data_grouped, columns=columns_dummies)

        predict_cols = ['agenda', 'bike_sharing_distance_km', 'bike_sharing_time_min', 'bus_distance_km', 'bus_time_min',
                       'car_distance_km', 'car_time_min', 'first_walking_distance_km', 'first_walking_time_min', 'has_car',
                       'has_moto', 'lat_destination', 'lat_origin', 'lng_destination', 'lng_origin', 'moto_distance_km',
                       'moto_sharing_distance_km', 'moto_sharing_time_min', 'moto_time_min', 'stops', 'subway_distance_km',
                       'subway_time_min', 'taxi_distance_km', 'taxi_time_min', 'total_distance_km', 'total_time_min',
                       'train_distance_km', 'train_time_min', 'tram_distance_km', 'tram_time_min', 'transfers',
                       'walking_distance_km', 'walking_time_min', 'pt_origin_gym', 'pt_origin_point_of_interest',
                       'pt_origin_street_address', 'pt_origin_establishment', 'pt_origin_locality', 'pt_origin_sublocality',
                       'pt_destination_gym', 'pt_destination_point_of_interest', 'pt_destination_street_address',
                       'pt_destination_establishment', 'pt_destination_locality', 'pt_destination_sublocality',
                       'day_of_week_thursday', 'pt_origin_food_places', 'pt_destination_food_places',
                       'pt_origin_shopping_places', 'pt_destination_shopping_places', 'pt_origin_health_places',
                        'pt_destination_health_places', 'pt_origin_vehicle_places', 'pt_destination_vehicle_places',
                        'day_of_week_friday', 'day_of_week_monday', 'day_of_week_saturday', 'day_of_week_sunday',
                        'day_of_week_tuesday', 'day_of_week_wednesday', 'day_of_week_type_weekend',
                        'day_of_week_type_work', 'profileName_green', 'profileName_innovate', 'profileName_pragmatic',
                        'profileName_technological', 'profileName_traditional', 'profileName_utilitarian',
                       'traffic_fluid', 'traffic_medium', 'traffic_heavy', 'weather_clear', 'weather_rain',
                       'weather_snow', 'arrivalTimeSlot_afternoon', 'arrivalTimeSlot_evening', 'arrivalTimeSlot_morning',
                        'arrivalTimeSlot_night','departureTimeSlot_afternoon', 'departureTimeSlot_morning', 'departureTimeSlot_night']


        # df_ref = pd.DataFrame(columns=predict_cols, index=df_data_dummies.index)
        #
        # df_data_dummies = df_data_dummies.merge(df_ref, how='left')[predict_cols].fillna(0)
        #
        df_columns = list(df_data_dummies.columns)
        dif_columns = list(set(predict_cols) - set(df_columns))
        print(">>", dif_columns)
        zero_dataframe = np.zeros(shape=(len(df_data_dummies), len(dif_columns)))
        df_ceros = pd.DataFrame(zero_dataframe, columns=dif_columns, index=df_data_dummies.index)
        df_final = pd.concat([df_data_dummies, df_ceros], axis=1).reindex(df_data.index)
        df_final = df_final.loc[:, predict_cols]
        #df_final = df_final.reindex(sorted(df_final.columns), axis=1)

        return df_final

    def transform(self, df_data, y=None):
        """The workhorse of this feature extractor"""
        return self.process_data(df_data)

    def fit(self, df_data, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self

