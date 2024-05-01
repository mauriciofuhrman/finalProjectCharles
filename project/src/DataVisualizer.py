import matplotlib.pyplot as plt
import pandas as pd
from QOLAnalysis import QOLAnalysis


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
        Plot weighted unemployment rate as a bar chart for each state.
        """
        unemployment_rate_per_state = pd.DataFrame([
            {'State': self.data_processor.state_abbrev_mapping[abbr], 'Rate': self.data_processor.calculate_weighted_unemployment_rate(abbr)}
            for abbr in self.data_processor.state_abbrev_mapping
        ])
        unemployment_rate_per_state.dropna(inplace=True)  # Remove states with missing data
        unemployment_rate_per_state.sort_values('Rate', ascending=False, inplace=True)

        print("Unemployment Rates per State:")
        print(unemployment_rate_per_state)

        plt.figure(figsize=(20, 10))
        colors = plt.cm.viridis(unemployment_rate_per_state['Rate'] / unemployment_rate_per_state['Rate'].max())
        bars = plt.bar(unemployment_rate_per_state['State'], unemployment_rate_per_state['Rate'], color=colors)
        plt.xlabel('State')
        plt.ylabel('Weighted Unemployment Rate (%)')
        plt.title('Weighted Unemployment Rates by State')
        plt.xticks(rotation=90)
        plt.tight_layout()

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval:.2f}', va='bottom', ha='center', color='black', rotation=90)

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

    def plot_happiness_colorcoded_bars(self):
        """Plot color-coded bar charts for happiness scores across states."""
        happiness_scores = self.data_processor.get_all_happiness_scores()
        sorted_happiness_scores = happiness_scores.sort_values('HappiestStatesTotalHappinessScore', ascending=False)

        plt.figure(figsize=(12, 8))
        normalized_scores = sorted_happiness_scores['HappiestStatesTotalHappinessScore'] / sorted_happiness_scores['HappiestStatesTotalHappinessScore'].max()
        colors = plt.cm.viridis(normalized_scores)
        plt.bar(sorted_happiness_scores['state'], sorted_happiness_scores['HappiestStatesTotalHappinessScore'], color=colors)
        plt.xlabel('State')
        plt.ylabel('Happiness Score')
        plt.title('Happiness Scores by State')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()


    def plot_happiness_correlation(self):
        """Plot correlation between happiness and unemployment."""
        happiness_scores = self.data_processor.get_all_happiness_scores()
        merged_data = pd.merge(happiness_scores, self.data_processor.get_all_weighted_unemployment_data(), on='state')

        plt.scatter(merged_data['HappiestStatesTotalHappinessScore'], merged_data['UnemploymentRate'])
        plt.xlabel('Happiness Score')
        plt.ylabel('Unemployment Rate')
        plt.title('Happiness vs Unemployment Rate')
        plt.grid(True)
        plt.show()

    def plot_economy_averages(self):
        """
        Plots the weighted averages of economy-related metrics for each state from a DataFrame.
        """
        df = self.data_processor.compute_economy_averages()
        _, ax = plt.subplots(figsize=(18, 7))  
        df.plot(x='state', y=['Cost of Living', '2022 Median Income'], kind='bar', ax=ax)
        ax.set_title('Economy-Related Metrics by State ($)')
        ax.set_xlabel('State')
        ax.set_ylabel('Weighted Average ($)')
        ax.grid(True)
        plt.xticks(rotation=90, ha='center')  
        ax.tick_params(axis='x', labelsize=8)  
        plt.tight_layout()
        plt.show()
    
    def plot_health_averages(self):
        """
        Plots the weighted averages of health-related metrics for each state from a DataFrame.
        """
        _, ax = plt.subplots(figsize=(14, 7))
        # Removed %CvgCityPark from the plot as there is little data available (only very few states have this metric)
        self.data_processor.compute_health_averages().plot(x='state', y='WaterQualityVPV', kind='bar', ax=ax, color='blue')
        ax.set_title('Health-Related Metrics by State (Lower = Better)')
        ax.set_xlabel('State')
        ax.set_ylabel('Weighted VPV Average')
        plt.xticks(rotation=90, ha='center')  
        ax.tick_params(axis='x', labelsize=8)  
        plt.tight_layout()
        plt.show()

    def plot_safety_averages(self):
        """
        Plots the weighted averages of safety-related metrics for each state from a DataFrame.
        
        Parameters:
            df (DataFrame): DataFrame containing each state with its weighted averages for safety-related metrics.
        """
        _, ax = plt.subplots(figsize=(14, 7))
        self.data_processor.compute_safety_averages().plot(x='state', y=['2016 Crime Rate'], kind='bar', ax=ax, color='red')
        ax.set_title('Safety-Related Metrics by State')
        ax.set_xlabel('State')
        ax.set_ylabel('Weighted Average')
        plt.xticks(rotation=90, ha='center')  
        ax.tick_params(axis='x', labelsize=8)  
        plt.tight_layout()
        plt.show()               


# qol = QOLAnalysis('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')
# dv = DataVisualizer(qol)
# dv.plot_happiness_colorcoded_bars()
# dv.plot_happiness_correlation(qol.get_all_weighted_unemployment_data())
# dv.plot_economy_averages()
# dv.plot_health_averages()
# dv.plot_safety_averages()