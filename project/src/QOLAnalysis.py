import pandas as pd


class QOLAnalysis:
    """
    Class to analyze and process QOL and unemployment data by state and county.
    """
    
    def __init__(self, state_data_path, county_data_path):
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
        self.load_data()
        
    def load_data(self):
        """
        Loads state and county data from CSV files into pandas DataFrames.
        """
        self.state_data = pd.read_csv(self.state_data_path)
        self.county_data = pd.read_csv(self.county_data_path)
    
        if self.county_data['Unemployment'].isnull().any():
            self.county_data['Unemployment'].fillna(self.county_data['Unemployment'].mean(), inplace=True)  

        if '2022 Population' in self.county_data.columns:
            self.county_data['2022 Population'].replace(',', '', regex=True, inplace=True)
            self.county_data['2022 Population'] = pd.to_numeric(self.county_data['2022 Population'], errors='coerce')
            self.county_data.dropna(subset=['2022 Population'], inplace=True)  


    def calculate_weighted_unemployment_rate(self, state_abbreviation):
        """
        Calculates the weighted average unemployment rate for a specified state.
        
        Parameters:
            state_abbreviation (str): The state abbreviation for which to calculate the rate.
        
        Returns:
            float: The weighted average unemployment rate for the state.
        """
        return self.compute_weighted_average(state_abbreviation, 'Unemployment')

    def get_all_weighted_unemployment_data(self):
        """
        Retrieves weighted unemployment data for all states.

        Returns:
            DataFrame: A DataFrame containing each state with its weighted average unemployment rate.
        """
        weighted_unemployment_rates = []

        for abbr in self.state_abbrev_mapping.keys():
            weighted_rate = self.calculate_weighted_unemployment_rate(abbr)
            if weighted_rate is not None:  
                weighted_unemployment_rates.append({
                    'state': self.state_abbrev_mapping[abbr],
                    'UnemploymentRate': weighted_rate
                })

        return pd.DataFrame(weighted_unemployment_rates)
    
    
    def get_state_happiness_score_based_on_state(self, state_abbreviation):
        """
        Calculates the happiness score for a specified state.
        
        Parameters:
            state_abbreviation (str): The state abbreviation for which to calculate the score.
        
        Returns:
            float: The happiness score for the state.
        """
        assert state_abbreviation in self.state_abbrev_mapping.keys(), 'Invalid state abbreviation'
        # print(state_abbreviation)
        state_data = self.state_data[self.state_data['state'] == self.state_abbrev_mapping[state_abbreviation]].copy()
        if state_data.empty:
            print("No data available for:", state_abbreviation)
            return None


        happiness_score = state_data['HappiestStatesTotalHappinessScore'].values[0]
        # print("Happiness score for", self.state_abbrev_mapping[state_abbreviation], "is", happiness_score)
        return happiness_score

    def get_all_happiness_scores(self):
        """Retrieve happiness scores for all states."""
        return self.state_data[['state', 'HappiestStatesTotalHappinessScore']]


    def find_state_with_highest_unemployment(self):
        """
        Identifies the state with the highest weighted unemployment rate.
        
        Returns:
            map: {"state" : [state_name], "rate" : [highest_unemployment_rate]}
        """
        max_rate = 0
        max_state = None
        
        for state_abbr in self.county_data['LSTATE'].unique():
            rate = self.calculate_weighted_unemployment_rate(state_abbr)
            if rate and rate > max_rate:
                max_rate = rate
                max_state = state_abbr
        
        return {
            "state": self.state_abbrev_mapping[max_state],
            "rate": max_rate
        }
    
    def find_state_with_lowest_unemployment(self):
        """
        Identifies the state with the lowest weighted unemployment rate.
        
        Returns:
            map: {"state" : [state_name], "rate" : [lowest_unemployment_rate]}
        """
        min_rate = 100
        min_state = None
        
        for state_abbr in self.county_data['LSTATE'].unique():
            rate = self.calculate_weighted_unemployment_rate(state_abbr)
            if rate and rate < min_rate:
                min_rate = rate
                min_state = state_abbr
        
        return {
            "state": self.state_abbrev_mapping[min_state],
            "rate": min_rate
        }
    
    def _convert_to_decimal(self, value):
        if isinstance(value, str):
            if '%' in value:
                new_val = float(value.replace('%', '')) / 100
                if new_val != -1:
                    return new_val
                else:
                    return pd.NA
            elif '/' in value:
                numerator, denominator = value.split('/')
                new_val = float(numerator) / float(denominator)
                if new_val != -1:
                    return new_val
        if float(value) == -1:
            return pd.NA
        return float(value)
    
    def compute_weighted_average(self, state_abbreviation : str, metric, is_dollar=False):
        """
        Computes the weighted average of a specific metric for a given state.
        
        Parameters:
            state_abbreviation (str): The state abbreviation for which to calculate the weighted average.
            metric (str): The metric to calculate the weighted average for.
        
        Returns:
            float: The weighted average of the specified metric for the state.
        """
        assert state_abbreviation in self.state_abbrev_mapping.keys(), 'Invalid state abbreviation'
        state_counties = self.county_data[self.county_data['LSTATE'] == state_abbreviation].copy()
        if state_counties.empty:
            return None

        state_counties.loc[:, 'Population'] = state_counties['2022 Population'].replace(',', '', regex=True).astype(int)
        if is_dollar:
            state_counties.loc[:, metric] = pd.to_numeric(state_counties[metric].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float), errors='coerce')
        else:
            state_counties.loc[:, metric] = pd.to_numeric(state_counties[metric].apply(self._convert_to_decimal), errors='coerce')
            # print(state_counties[metric])

        
        total_population = state_counties['Population'].sum()
        weighted_sum = (state_counties['Population'] * state_counties[metric]).sum()
        
        weighted_average = weighted_sum / total_population
        return weighted_average

    def compute_economy_averages(self):
        """
        Computes the weighted averages of economy-related metrics for each state.
        
        Returns:
            DataFrame: A DataFrame containing each state with its weighted averages for economy-related metrics.
        """
        economy_metrics = ['Cost of Living', '2022 Median Income']
        economy_averages = []

        for abbr in self.state_abbrev_mapping.keys():
            state_averages = {'state': self.state_abbrev_mapping[abbr]}
            for metric in economy_metrics:
                weighted_average = self.compute_weighted_average(abbr, metric, True)
                if weighted_average is not None:
                    state_averages[metric] = weighted_average
            economy_averages.append(state_averages)

        return pd.DataFrame(economy_averages)

    def compute_health_averages(self):
        """
        Computes the weighted averages of health-related metrics for each state.
        
        Returns:
            DataFrame: A DataFrame containing each state with its weighted averages for health-related metrics.
        """
        health_metrics = ['WaterQualityVPV', '%CvgCityPark']
        health_averages = []

        for abbr in self.state_abbrev_mapping.keys():
            state_averages = {'state': self.state_abbrev_mapping[abbr]}
            for metric in health_metrics:
                weighted_average = self.compute_weighted_average(abbr, metric)
                if weighted_average is not None:
                    state_averages[metric] = weighted_average
            health_averages.append(state_averages)

        return pd.DataFrame(health_averages)

    def compute_safety_averages(self):
        """
        Computes the weighted averages of safety-related metrics for each state.
        
        Returns:
            DataFrame: A DataFrame containing each state with its weighted averages for safety-related metrics.
        """
        safety_metric = '2016 Crime Rate'
        safety_averages = []

        for abbr in self.state_abbrev_mapping.keys():
            weighted_average = self.compute_weighted_average(abbr, safety_metric)
            if weighted_average is not None:
                safety_averages.append({
                    'state': self.state_abbrev_mapping[abbr],
                    safety_metric: weighted_average
                })

        return pd.DataFrame(safety_averages)

# qol = QOLAnalysis('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')
# print(qol.compute_weighted_average('FL', 'Unemployment'))
# print(qol.compute_economy_averages())
# print(qol.compute_weighted_average('FL', 'WaterQualityVPV'))
# print(qol.compute_health_averages())
# print(qol.compute_safety_averages())
