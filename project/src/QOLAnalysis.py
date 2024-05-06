import pandas as pd
from pydantic import BaseModel
from typing import Union, Optional
import logging



class UnemploymentRateInfo(BaseModel):
    state: str
    rate: float


class QOLAnalysis:
    """
    Class to analyze and process QOL and unemployment data by state and county.
    """
    
    def __init__(self, state_data_path : str, county_data_path : str) -> None:
        """
        Initializes the QOL data with the correct paths.
        
        Parameters:
            state_data_path (str): Path to the state quality of life CSV file.
            county_data_path (str): Path to the county quality of life CSV file.
        """
        self.state_data_path = state_data_path
        self.county_data_path = county_data_path
        # Added DC because data includes it as a State
        self.state_abbrev_mapping = {
            'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
            'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'Washington D.C.','DE': 'Delaware',
            'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
            'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
            'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
            'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
            'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
            'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
            'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
            'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
            'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
            'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
            'WI': 'Wisconsin', 'WY': 'Wyoming'
        }
        self.state_data = None
        self.county_data = None
        self.logger = logging.getLogger(__name__)
        self.logger.info(f'Initializing QOLAnalysis with paths: State data path - {state_data_path}, County data path - {county_data_path}')
        self.load_data()
        
    def load_data(self) -> None:
        """
        Loads state and county data from CSV files into pandas DataFrames.
        """
        self.logger.info('Starting to load state and county data...')
        self.state_data = pd.read_csv(self.state_data_path)
        self.county_data = pd.read_csv(self.county_data_path)
        self.logger.info('Data loaded successfully. Processing data...')
        if self.county_data['Unemployment'].isnull().any():
            self.county_data['Unemployment'].fillna(self.county_data['Unemployment'].mean(), inplace=True)
            self.logger.info('Filled missing unemployment data with mean values.')
        if '2022 Population' in self.county_data.columns:
            self.county_data['2022 Population'].replace(',', '', regex=True, inplace=True)
            self.county_data['2022 Population'] = pd.to_numeric(self.county_data['2022 Population'], errors='coerce')
            self.county_data.dropna(subset=['2022 Population'], inplace=True)
            self.logger.info('Processed 2022 Population data for numeric consistency.')
        self.logger.info('State and county data fully loaded and processed.') 


    def calculate_weighted_unemployment_rate(self, state_abbreviation : str) -> float:
        """
        Calculates the weighted average unemployment rate for a specified state.
        
        Parameters:
            state_abbreviation (str): The state abbreviation for which to calculate the rate.
        
        Returns:
            float: The weighted average unemployment rate for the state.
        """
        self.logger.info(f'Calculating weighted unemployment rate for {state_abbreviation}')
        rate = self.compute_weighted_average(state_abbreviation, 'Unemployment')
        self.logger.info(f'Weighted unemployment rate for {state_abbreviation} is {rate}')
        return rate

    def get_all_weighted_unemployment_data(self) -> pd.DataFrame:
        """
        Retrieves weighted unemployment data for all states.

        Returns:
            DataFrame: A DataFrame containing each state with its weighted average unemployment rate.
        """
        self.logger.info('Retrieving weighted unemployment data for all states...')
        weighted_unemployment_rates = []
        for abbr in self.state_abbrev_mapping.keys():
            weighted_rate = self.calculate_weighted_unemployment_rate(abbr)
            if weighted_rate is not None:
                weighted_unemployment_rates.append({'state': self.state_abbrev_mapping[abbr], 'UnemploymentRate': weighted_rate})
        df = pd.DataFrame(weighted_unemployment_rates)
        self.logger.info('Successfully retrieved weighted unemployment data for all states.')
        return df
    
    
    def get_state_happiness_score_based_on_state(self, state_abbreviation : str) -> float:
        """
        Calculates the happiness score for a specified state.
        
        Parameters:
            state_abbreviation (str): The state abbreviation for which to calculate the score.
        
        Returns:
            float: The happiness score for the state.
        """
        assert state_abbreviation in self.state_abbrev_mapping.keys(), 'Invalid state abbreviation'
        # print(state_abbreviation)
        self.logger.info(f'Calculating happiness score for {state_abbreviation}')
        state_data = self.state_data[self.state_data['state'] == self.state_abbrev_mapping[state_abbreviation]].copy()
        if state_data.empty:
            self.logger.warning(f'No data available for state abbreviation: {state_abbreviation}')
            return None
        happiness_score = state_data['HappiestStatesTotalHappinessScore'].values[0]
        self.logger.info(f'Happiness score for {state_abbreviation} is {happiness_score}')
        return happiness_score

    def get_all_happiness_scores(self) -> pd.DataFrame:
        """Retrieve happiness scores for all states."""
        self.logger.info("Retrieving all happiness scores from state data.")
        try:
            scores = self.state_data[['state', 'HappiestStatesTotalHappinessScore']]
            self.logger.info("Successfully retrieved happiness scores for all states.")
            return scores
        except KeyError as e:
            self.logger.error(f"Failed to retrieve happiness scores: {e}")
            raise



    def find_state_with_highest_unemployment(self) -> UnemploymentRateInfo:
        """
        Identifies the state with the highest weighted unemployment rate.
        
        Returns:
            map: {"state" : [state_name], "rate" : [highest_unemployment_rate]}
        """
        self.logger.info("Searching for the state with the highest unemployment rate.")
        max_rate = 0
        max_state = None
        
        for state_abbr in self.county_data['LSTATE'].unique():
            rate = self.calculate_weighted_unemployment_rate(state_abbr)
            if rate and rate > max_rate:
                max_rate = rate
                max_state = state_abbr
        
        self.logger.info(f"State with the highest unemployment: {max_state} at {max_rate}%")
        return {
            "state": self.state_abbrev_mapping[max_state],
            "rate": max_rate
        }

    
    def find_state_with_lowest_unemployment(self) -> UnemploymentRateInfo:
        """
        Identifies the state with the lowest weighted unemployment rate.
        
        Returns:
            map: {"state" : [state_name], "rate" : [lowest_unemployment_rate]}
        """
        self.logger.info("Searching for the state with the lowest unemployment rate.")
        min_rate = 100
        min_state = None
        
        for state_abbr in self.county_data['LSTATE'].unique():
            rate = self.calculate_weighted_unemployment_rate(state_abbr)
            if rate and rate < min_rate:
                min_rate = rate
                min_state = state_abbr
        
        self.logger.info(f"State with the lowest unemployment: {min_state} at {min_rate}%")
        return {
            "state": self.state_abbrev_mapping[min_state],
            "rate": min_rate
        }

    
    def _convert_to_decimal(self, value : Union[str, float]) -> Optional[float]:
        """
        Converts a given string or float to a decimal representation. The function returns None if
        the input value is '-1' or if the conversion results in -1, indicating missing or invalid data.
        """
        self.logger.debug(f"Converting value: {value}")
        try:
            if isinstance(value, str):
                if '%' in value:
                    new_val = float(value.replace('%', '')) / 100
                    if new_val != -1:
                        self.logger.debug(f"Converted value: {new_val}")
                        return new_val
                    else:
                        return None
                elif '/' in value:
                    numerator, denominator = value.split('/')
                    new_val = float(numerator) / float(denominator)
                    if new_val != -1:
                        self.logger.debug(f"Converted value: {new_val}")
                        return new_val
            if float(value) == -1:
                return None
            return float(value)
        except Exception as e:
            self.logger.error(f"Error converting value {value}: {e}")
            return None

    
    def compute_weighted_average(self, state_abbreviation : str, metric : str, is_dollar : bool = False) -> float:
        """
        Computes the weighted average of a specific metric for a given state.
        
        Parameters:
            state_abbreviation (str): The state abbreviation for which to calculate the weighted average.
            metric (str): The metric to calculate the weighted average for.
        
        Returns:
            float: The weighted average of the specified metric for the state.
        """
        self.logger.info(f"Computing weighted average for {state_abbreviation} based on {metric}.")
        assert state_abbreviation in self.state_abbrev_mapping.keys(), 'Invalid state abbreviation'
        state_counties = self.county_data[self.county_data['LSTATE'] == state_abbreviation].copy()
        if state_counties.empty:
            self.logger.warning(f"No county data available for {state_abbreviation}. Returning None.")
            return None

        state_counties.loc[:, 'Population'] = state_counties['2022 Population'].replace(',', '', regex=True).astype(int)
        if is_dollar:
            state_counties.loc[:, metric] = pd.to_numeric(state_counties[metric].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float), errors='coerce')
        else:
            state_counties.loc[:, metric] = pd.to_numeric(state_counties[metric].apply(self._convert_to_decimal), errors='coerce')

        total_population = state_counties['Population'].sum()
        weighted_sum = (state_counties['Population'] * state_counties[metric]).sum()
        weighted_average = weighted_sum / total_population
        self.logger.info(f"Weighted average for {metric} in {state_abbreviation} is {weighted_average}.")
        return weighted_average

    def compute_economy_averages(self) -> pd.DataFrame:
        """
        Computes the weighted averages of economy-related metrics for each state.
        
        Returns:
            DataFrame: A DataFrame containing each state with its weighted averages for economy-related metrics.
        """
        self.logger.info("Computing economy averages for all states.")
        economy_metrics = ['Cost of Living', '2022 Median Income']
        economy_averages = []

        for abbr in self.state_abbrev_mapping.keys():
            state_averages = {'state': self.state_abbrev_mapping[abbr]}
            for metric in economy_metrics:
                weighted_average = self.compute_weighted_average(abbr, metric, True)
                if weighted_average is not None:
                    state_averages[metric] = weighted_average
            economy_averages.append(state_averages)

        self.logger.info("Successfully computed economy averages for all states.")
        return pd.DataFrame(economy_averages)

    def compute_health_averages(self) -> pd.DataFrame:
        """
        Computes the weighted averages of health-related metrics for each state.
        
        Returns:
            DataFrame: A DataFrame containing each state with its weighted averages for health-related metrics.
        """
        self.logger.info("Computing health averages for all states.")
        health_metrics = ['WaterQualityVPV', '%CvgCityPark']
        health_averages = []

        for abbr in self.state_abbrev_mapping.keys():
            state_averages = {'state': self.state_abbrev_mapping[abbr]}
            for metric in health_metrics:
                weighted_average = self.compute_weighted_average(abbr, metric)
                if weighted_average is not None:
                    state_averages[metric] = weighted_average
            health_averages.append(state_averages)

        self.logger.info("Successfully computed health averages for all states.")
        return pd.DataFrame(health_averages)

    def compute_safety_averages(self) -> pd.DataFrame:
        """
        Computes the weighted averages of safety-related metrics for each state.
        
        Returns:
            DataFrame: A DataFrame containing each state with its weighted averages for safety-related metrics.
        """
        self.logger.info("Computing safety averages for all states.")
        safety_metric = '2016 Crime Rate'
        safety_averages = []

        for abbr in self.state_abbrev_mapping.keys():
            weighted_average = self.compute_weighted_average(abbr, safety_metric)
            if weighted_average is not None:
                safety_averages.append({
                    'state': self.state_abbrev_mapping[abbr],
                    safety_metric: weighted_average
                })

        self.logger.info("Successfully computed safety averages for all states.")
        return pd.DataFrame(safety_averages)

# qol = QOLAnalysis('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')
# print(qol.compute_weighted_average('FL', 'Unemployment'))
# print(qol.compute_economy_averages())
# print(qol.compute_weighted_average('FL', 'WaterQualityVPV'))
# print(qol.compute_health_averages())
# print(qol.compute_safety_averages())
