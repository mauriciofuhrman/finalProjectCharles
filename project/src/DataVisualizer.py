import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

class DataVisualizer:
    """
    Class to handle visualization of Quality of Life and unemployment data.
    """
    def __init__(self, data_processor):
        """
        Initializes the DataVisualizer with a QualityOfLifeData instance.

        Parameters:
            data_processor (QualityOfLifeData): The data processing instance that loads and computes data.
        """
        self.data_processor = data_processor

    def plot_unemployment_rates(self):
        """
        Plots the unemployment rates using matplotlib.
        """
        state_data = pd.DataFrame([
            {'State': abbr, 'Rate': self.data_processor.calculate_weighted_unemployment_rate(abbr)}
            for abbr in self.data_processor.state_abbrev_mapping
        ])
        state_data.sort_values('Rate', ascending=False, inplace=True)

       
        plt.figure(figsize=(12, 8))
        colors = plt.cm.viridis(state_data['Rate'] / state_data['Rate'].max())
        bars = plt.bar(state_data['State'], state_data['Rate'], color=colors)
        plt.xlabel('State')
        plt.ylabel('Unemployment Rate (%)')
        plt.title('Unemployment Rates by State')
        plt.xticks(rotation=45)
        plt.tight_layout()

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval - 0.26, round(yval, 2),
                    va='bottom', ha='center', color='black', rotation=90)

        plt.show()


