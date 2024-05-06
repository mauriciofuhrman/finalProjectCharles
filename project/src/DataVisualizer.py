import matplotlib.pyplot as plt
import pandas as pd
from QOLAnalysis import QOLAnalysis
from typing import Tuple, List


class DataVisualizer:
    """
    Class to handle visualization of Quality of Life and unemployment data.
    """

    def __init__(self, data_processor: QOLAnalysis, fig_size: Tuple[int, int] = (20, 10)) -> None:
        """
        Initializes the DataVisualizer with a QOLAnalysis instance.

        Parameters:
            data_processor (QOLAnalysis): The data processing instance that loads and computes data.
            fig_size (Tuple[int, int], optional): A tuple representing the width and height of the figure. Defaults to (20, 10).
        """
        self.data_processor = data_processor
        self.fig_size = fig_size

    def plot_unemployment_rates(self, fig_size: Tuple[int, int] = None) -> None:
        """
        Plots weighted unemployment rates as a bar chart for each state.

        Parameters:
            fig_size (Optional[Tuple[int, int]]): Size of the figure to override the default size.
        """
        unemployment_rate_per_state = pd.DataFrame([
            {'State': self.data_processor.state_abbrev_mapping[abbr], 'Rate': self.data_processor.calculate_weighted_unemployment_rate(abbr)}
            for abbr in self.data_processor.state_abbrev_mapping
        ])
        unemployment_rate_per_state.dropna(inplace=True)  # Remove states with missing data
        unemployment_rate_per_state.sort_values('Rate', ascending=False, inplace=True)

        print("Unemployment Rates per State:")
        print(unemployment_rate_per_state)

        if fig_size is not None:
            plt.figure(figsize=fig_size)
        else:
            plt.figure(figsize=self.fig_size)
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

    def plot_quality_of_life_comparison(self, states : List[str], fig_size : Tuple[int, int] = None) -> None:
        """
        Plots a grouped bar chart comparison of different Quality of Life metrics for specific states.

        Parameters:
            states (List[str]): List of state names to be compared.
            fig_size (Optional[Tuple[int, int]]): Size of the figure to override the default size.
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

        if fig_size is not None:
            _, ax = plt.subplots(figsize=fig_size)
        else:
           _, ax = plt.subplots(figsize=self.fig_size)


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
        ax.legend(title='Metrics', bbox_to_anchor=(1, 1), loc='upper left', fontsize='small')

        plt.tight_layout(rect=[0, 0, 0.85, 1])  

        plt.show()

    def plot_happiness_colorcoded_bars(self, fig_size: Tuple[int, int] = None) -> None:
        """
        Plots color-coded bar charts for happiness scores across states. The colors of the bars
        represent the relative happiness scores normalized to the highest score.

        Parameters:
            fig_size (Optional[Tuple[int, int]]): Size of the figure to override the default size.
        """
        happiness_scores = self.data_processor.get_all_happiness_scores()
        sorted_happiness_scores = happiness_scores.sort_values('HappiestStatesTotalHappinessScore', ascending=False)

        if fig_size is not None:
            plt.figure(figsize=fig_size)
        else:
            plt.figure(figsize=self.fig_size)
        normalized_scores = sorted_happiness_scores['HappiestStatesTotalHappinessScore'] / sorted_happiness_scores['HappiestStatesTotalHappinessScore'].max()
        colors = plt.cm.viridis(normalized_scores)
        plt.bar(sorted_happiness_scores['state'], sorted_happiness_scores['HappiestStatesTotalHappinessScore'], color=colors)
        plt.xlabel('State')
        plt.ylabel('Happiness Score')
        plt.title('Happiness Scores by State')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()


    def plot_happiness_correlation(self) -> None:
        """
        Plots a scatter plot to illustrate the correlation between happiness scores and unemployment rates
        across states. This can help visualize any relationship between overall happiness and economic factors.

        Returns:
            None: This method only generates a plot and does not return any data.
        """
        happiness_scores = self.data_processor.get_all_happiness_scores()
        merged_data = pd.merge(happiness_scores, self.data_processor.get_all_weighted_unemployment_data(), on='state')

        plt.scatter(merged_data['HappiestStatesTotalHappinessScore'], merged_data['UnemploymentRate'])
        plt.xlabel('Happiness Score')
        plt.ylabel('Unemployment Rate')
        plt.title('Happiness vs Unemployment Rate')
        plt.grid(True)
        plt.show()

    def plot_economy_averages(self, fig_size=None):
        """
        Plots the weighted averages of economy-related metrics, such as cost of living and median income,
        for each state. This visualization helps compare economic conditions across different states.

        Parameters:
            fig_size (Optional[Tuple[int, int]]): Size of the figure to override the default size.
        """
        df = self.data_processor.compute_economy_averages()
        if fig_size is not None:
            _, ax = plt.subplots(figsize=fig_size)
        else:
           _, ax = plt.subplots(figsize=self.fig_size)
        df.plot(x='state', y=['Cost of Living', '2022 Median Income'], kind='bar', ax=ax)
        ax.set_title('Economy-Related Metrics by State ($)')
        ax.set_xlabel('State')
        ax.set_ylabel('Weighted Average ($)')
        ax.grid(True)
        plt.xticks(rotation=90, ha='center')  
        ax.tick_params(axis='x', labelsize=8)  
        plt.tight_layout()
        plt.show()
    
    def plot_health_averages(self, fig_size: Tuple[int, int] = None) -> None:
        """
        Plots the weighted averages of health-related metrics for each state. The plot focuses on metrics
        such as water quality, visualizing health standards across states.

        Parameters:
            fig_size (Optional[Tuple[int, int]]): Size of the figure to override the default size.
        """
        if fig_size is not None:
            _, ax = plt.subplots(figsize=fig_size)
        else:
           _, ax = plt.subplots(figsize=self.fig_size)
        # Removed %CvgCityPark from the plot as there is little data available (only very few states have this metric)
        self.data_processor.compute_health_averages().plot(x='state', y='WaterQualityVPV', kind='bar', ax=ax, color='blue')
        ax.set_title('Health-Related Metrics by State (Lower = Better)')
        ax.set_xlabel('State')
        ax.set_ylabel('Weighted VPV Average')
        plt.xticks(rotation=90, ha='center')  
        ax.tick_params(axis='x', labelsize=8)  
        plt.tight_layout()
        plt.show()

    def plot_safety_averages(self, fig_size : Tuple[int, int] = None) -> None:
        """
        Plots the weighted averages of safety-related metrics for each state. Metrics such as crime rates
        are visualized to provide insights into the safety conditions of different states.

        Parameters:
            fig_size (Optional[Tuple[int, int]]): Size of the figure to override the default size.
        """
        if fig_size is not None:
            _, ax = plt.subplots(figsize=fig_size)
        else:
           _, ax = plt.subplots(figsize=self.fig_size)
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