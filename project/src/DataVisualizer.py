import matplotlib.pyplot as plt
import pandas as pd

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
        Plot unemployment rate as bar chart for each state.
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

    def plot_quality_of_life_comparison(self):
        """
        Plot a comparison of different Quality of Life metrics for each state.
        """
        quality_data = self.data_processor.state_data[['state', 'QualityOfLifeTotalScore', 'QualityOfLifeAffordability', 'QualityOfLifeEconomy', 'QualityOfLifeEducationAndHealth', 'QualityOfLifeSafety']].copy()
        quality_data.set_index('state', inplace=True)
        quality_data.sort_values('QualityOfLifeTotalScore', ascending=False, inplace=True)
        
        # Normalizing the data for comparison
        quality_normalized = (quality_data - quality_data.min()) / (quality_data.max() - quality_data.min())

        quality_normalized.plot(kind='bar', stacked=True, figsize=(15, 8))
        plt.xlabel('State')
        plt.ylabel('Normalized Quality of Life Scores')
        plt.title('Comparative Quality of Life Scores by State')
        plt.legend(title='Metrics')
        plt.tight_layout()
        plt.show()

    def plot_correlation_unemployment_quality(self):
        """
        Plot the correlation between unemployment rates and Quality of Life scores.
        """
        unemployment_rates = [self.data_processor.calculate_weighted_unemployment_rate(abbr) for abbr in self.data_processor.state_abbrev_mapping]
        quality_of_life_scores = self.data_processor.state_data['QualityOfLifeTotalScore'].tolist()
        
        paired_data = [(rate, score) for rate, score in zip(unemployment_rates, quality_of_life_scores) if rate is not None]
        
        unemployment_rates, quality_of_life_scores = zip(*paired_data)
        
        correlation_data = pd.DataFrame({
            'UnemploymentRate': unemployment_rates,
            'QualityOfLifeScore': quality_of_life_scores
        })
        
        plt.figure(figsize=(10, 6))
        plt.scatter(correlation_data['UnemploymentRate'], correlation_data['QualityOfLifeScore'])
        plt.xlabel('Weighted Unemployment Rate (%)')
        plt.ylabel('Quality of Life Total Score')
        plt.title('Correlation between Unemployment Rate and Quality of Life Score')
        plt.tight_layout()
        plt.show()





