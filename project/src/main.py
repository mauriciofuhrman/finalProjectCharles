from QOLAnalysis import QOLAnalysis
from DataVisualizer import DataVisualizer

def main():
    input("Hi, my name is Mauricio Fuhrman, and I am using Python to analyze and interpret the United States' Quality of Life and Unemployment. Press Enter to continue.")

    data_processor = QOLAnalysis('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')
    visualizer = DataVisualizer(data_processor)

    if input("Would you like to find out which state has the highest unemployment rate? (y/n): ").strip().lower().startswith('y'):
        guess = input("First guess which state has the highest unemployment rate. Write your guess and press Enter: ")
        state_with_highest_unemployment = data_processor.find_state_with_highest_unemployment()
        if guess.lower() == state_with_highest_unemployment['state'].lower():
            print("You guessed correctly! They have an unemployment rate of", state_with_highest_unemployment['rate'], "%")
        else:
            print("Incorrect. The state with the highest unemployment rate is", state_with_highest_unemployment['state'], "with a rate of", state_with_highest_unemployment['rate'], "%")
        
    
    if input("Would you like to find out which state has the lowest unemployment rate? (y/n): ").strip().lower().startswith('y'):
        guess = input("First guess which state has the lowest unemployment rate. Write your guess and press Enter: ")
        state_with_lowest_unemployment = data_processor.find_state_with_lowest_unemployment()
        if guess.lower() == state_with_lowest_unemployment['state'].lower():
            print("You guessed correctly! They have an unemployment rate of", state_with_lowest_unemployment['rate'], "%")
        else:
            print("Incorrect. The state with the lowest unemployment rate is", state_with_lowest_unemployment['state'], "with a rate of", state_with_lowest_unemployment['rate'], "%")
    
    if input("Would you like to view the Unemployment Rates by State graph? (y/n): ").strip().lower().startswith('y'):
        visualizer.plot_unemployment_rates()


    if input("Would you like to view the Quality of Life Comparison graph? (y/n): ").strip().lower().startswith('y'):
        while True:
            states = input("Please enter the states you want to compare separated by commas (such as: 'California, Texas, New York'): ").strip().split(',')
            states = [state.strip().title() for state in states]
            all_possible_states = [state for state in data_processor.state_abbrev_mapping.values()]
            all_are_states = all(state in all_possible_states for state in states)
            if all_are_states:
                print("Comparing states:", states)
                visualizer.plot_quality_of_life_comparison(states)
                break  
            else:
                print("One or more of the states you entered is not a valid state. Please try again.")

if __name__ == '__main__':
    main()
