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
        unemployment_rate_per_state = pd.DataFrame([
            {'State': abbr, 'Rate': self.data_processor.calculate_weighted_unemployment_rate(abbr)}
            for abbr in self.data_processor.state_abbrev_mapping
        ])

        unemployment_rate_per_state.sort_values('Rate', ascending=False, inplace=True)

        plt.figure(figsize=(12, 8))
        colors = plt.cm.viridis(unemployment_rate_per_state['Rate'] / unemployment_rate_per_state['Rate'].max())
        bars = plt.bar(unemployment_rate_per_state['State'], unemployment_rate_per_state['Rate'], color=colors)
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

    def plot_quality_of_life_comparison(self, states):
        """
        Plot a grouped bar chart comparison of different Quality of Life metrics for specific states.
        """
        states = [state.strip() for state in states]

        quality_data = self.data_processor.state_data[self.data_processor.state_data['state'].isin(states)].copy()

        metrics_columns = ['QualityOfLifeTotalScore', 'QualityOfLifeAffordability', 'QualityOfLifeEconomy', 
                        'QualityOfLifeEducationAndHealth', 'QualityOfLifeSafety']
        
        quality_data[metrics_columns] = quality_data[metrics_columns].apply(pd.to_numeric, errors='coerce')

        # Normalize the data
        normalized_data = quality_data[metrics_columns].copy()
        for metric in metrics_columns:
            min_val = self.data_processor.state_data[metric].min()
            max_val = self.data_processor.state_data[metric].max()
            normalized_data.loc[:, metric] = (quality_data.loc[:, metric] - min_val) / (max_val - min_val)

        plot_data = normalized_data.copy()
        plot_data['state'] = quality_data['state'].values

        positions = list(range(len(plot_data)))
        bar_width = 0.15

        _, ax = plt.subplots(figsize=(10, 6))

        for i, metric in enumerate(metrics_columns):
            ax.bar([p + bar_width * i for p in positions],
                plot_data[metric],
                bar_width,
                label=metric)

        ax.set_xticks([p + bar_width * (len(metrics_columns) - 1) / 2 for p in positions])
        ax.set_xticklabels(plot_data['state'], rotation=45)

        ax.set_xlabel('State')
        ax.set_ylabel('Normalized Quality of Life Scores')
        ax.set_title('Comparative Quality of Life Scores by State')
        ax.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()






