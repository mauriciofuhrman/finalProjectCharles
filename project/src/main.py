from QOLAnalysis import QOLAnalysis
from DataVisualizer import DataVisualizer



def get_valid_y_or_n_answer(prompt):
    """
    Asks the user a yes or no question and returns the answer.

    This function will repeatedly prompt the user until they
    enter an exact 'y' for yes or 'n' for no.

    Parameters:
        prompt (str): The question to prompt the user with.

    Returns:
        str: 'y' if the user enters 'y', 'n' if the user enters 'n'.
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer == 'y':
            return 'y'
        elif answer == 'n':
            return 'n'
        print("Please enter 'y' for yes or 'n' for no.")

def get_valid_state_guess(prompt, states):
        """
        Asks the user for a state.

        This function will repeatedly prompt the user until they
        enter an actual value for a state.

        Parameters:
            prompt (str): The question to prompt the user with.
            states (str[]): The values of states. Will pass in the state_abbrev_mapping values.

        Returns:
            str: the state selected.
        """
        valid_states = set(states)  
        while True:
            guess = input(prompt).strip().title()  
            if guess in valid_states:
                return guess
            print("Please enter the full name of a valid state, not an abbreviation.")

def main():

    input("Hi, my name is Mauricio Fuhrman, and I am using Python to analyze and interpret the United States' Quality of Life and Unemployment. Press Enter to continue.")

    data_processor = QOLAnalysis('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')
    visualizer = DataVisualizer(data_processor)

    answer = get_valid_y_or_n_answer("Would you like to find out which state has the highest unemployment rate? (y/n): ")
    if answer == 'y':
        guess = get_valid_state_guess("First guess which state has the highest unemployment rate. Write your guess and press Enter: ", data_processor.state_abbrev_mapping.values())
        state_with_highest_unemployment = data_processor.find_state_with_highest_unemployment()
        if guess.lower() == state_with_highest_unemployment['state'].lower():
            print("You guessed correctly! They have an unemployment rate of", state_with_highest_unemployment['rate'], "%")
        else:
            print("Incorrect. The state with the highest unemployment rate is", state_with_highest_unemployment['state'], "with a rate of", round(state_with_highest_unemployment['rate']*100,2), "%")

    answer = get_valid_y_or_n_answer("Would you like to find out which state has the lowest unemployment rate? (y/n): ")
    if answer == 'y':
        guess = get_valid_state_guess("First guess which state has the lowest unemployment rate. Write your guess and press Enter: ", data_processor.state_abbrev_mapping.values())
        state_with_lowest_unemployment = data_processor.find_state_with_lowest_unemployment()
        if guess.lower() == state_with_lowest_unemployment['state'].lower():
            print("You guessed correctly! They have an unemployment rate of", state_with_lowest_unemployment['rate'], "%")
        else:
            print("Incorrect. The state with the lowest unemployment rate is", state_with_lowest_unemployment['state'], "with a rate of", round(state_with_lowest_unemployment['rate']*100,2), "%")
    
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
    if input("Would you like to see the happiest states? (y/n): ").strip().lower().startswith('y'):
        visualizer.plot_happiness_colorcoded_bars()
    if input("Would you like to see the correlation between unemployment and happiness? (y/n): ").strip().lower().startswith('y'):
        visualizer.plot_happiness_correlation()

if __name__ == '__main__':
    main()
