from QOLAnalysis import QOLAnalysis
from DataVisualizer import DataVisualizer

def main():
    data_processor = QOLAnalysis('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')
    
    visualizer = DataVisualizer(data_processor)
    
    visualizer.plot_unemployment_rates()

    print("State with Highest Unemployment Rate:")
    print(data_processor.find_state_with_highest_unemployment())

    print("State with Lowest Unemployment Rate:")
    print(data_processor.find_state_with_lowest_unemployment())

if __name__ == '__main__':
    main()