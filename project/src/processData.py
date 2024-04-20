import pandas as pd

class QualityOfLifeData:
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

    def calculate_weighted_unemployment_rate(self, state_abbreviation):
        """
        Calculates the weighted average unemployment rate for a specified state.
        
        Parameters:
            state_abbreviation (str): The state abbreviation for which to calculate the rate.
        
        Returns:
            float: The weighted average unemployment rate for the state.
        """
        assert state_abbreviation in self.state_abbrev_mapping.keys(), 'Invalid state abbreviation'
        state_counties = self.county_data[self.county_data['LSTATE'] == state_abbreviation].copy()
        if state_counties.empty:
            return None
        
        state_counties.loc[:, 'Population'] = state_counties['2022 Population'].replace(',', '', regex=True).astype(int)
        state_counties.loc[:, 'Unemployment'] = state_counties['Unemployment'].str.rstrip('%').astype(float)
        
        total_population = state_counties['Population'].sum()
        weighted_sum = (state_counties['Population'] * state_counties['Unemployment']).sum()
        
        weighted_average = weighted_sum / total_population
        return weighted_average

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

data_processor = QualityOfLifeData('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')
print(data_processor.calculate_weighted_unemployment_rate('CA'))
print(data_processor.find_state_with_highest_unemployment())
print(data_processor.find_state_with_lowest_unemployment())
