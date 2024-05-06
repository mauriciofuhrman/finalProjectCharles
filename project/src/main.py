from QOLAnalysis import QOLAnalysis
from DataVisualizer import DataVisualizer
import yaml

with open('../config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def get_valid_y_or_n_answer(prompt : str) -> str:
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

def get_valid_state_guess(prompt, states : str) -> str:
        """
        Asks the user for a state.

        This function will repeatedly prompt the user until they
        enter actual values for states.

        Parameters:
            prompt (str): The question to prompt the user with.
            states (str): The values of states. Will pass in the state_abbrev_mapping values.

        Returns:
            str: the state selected.
        """
        valid_states = set(states)  
        while True:
            guess = input(prompt).strip().title()  
            if guess in valid_states:
                return guess
            print("Please enter the full name of a valid state, not an abbreviation.")

def get_answer(question_key_in_config : str, prompt : str) -> str:
    if question_key_in_config in config['answers']:
        return config['answers'][question_key_in_config]
    else:
        return get_valid_y_or_n_answer(prompt)


def main():

    input("Hi, my name is Mauricio Fuhrman, and I am using Python to analyze and interpret the United States' Quality of Life and Unemployment. Press Enter to continue.")

    data_processor = QOLAnalysis('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')
    visualizer = DataVisualizer(data_processor)

    answer = get_answer("highest_unemployment", "Would you like to find out which state has the highest unemployment rate? (y/n): ")
    if answer == 'y':
        guess = get_valid_state_guess("First guess which state has the highest unemployment rate. Write your guess and press Enter: ", data_processor.state_abbrev_mapping.values())
        state_with_highest_unemployment = data_processor.find_state_with_highest_unemployment()
        value = round(state_with_highest_unemployment['rate']*100,2)
        if guess.lower() == state_with_highest_unemployment['state'].lower():
            print("You guessed correctly! They have an unemployment rate of", value, "%")
        else:
            print("Incorrect. The state with the highest unemployment rate is", state_with_highest_unemployment['state'], "with a rate of", value, "%")

    answer = get_answer("lowest_unemployment", "Would you like to find out which state has the lowest unemployment rate? (y/n): ")
    if answer == 'y':
        guess = get_valid_state_guess("First guess which state has the lowest unemployment rate. Write your guess and press Enter: ", data_processor.state_abbrev_mapping.values())
        state_with_lowest_unemployment = data_processor.find_state_with_lowest_unemployment()
        value = round(state_with_lowest_unemployment['rate']*100,2)
        if guess.lower() == state_with_lowest_unemployment['state'].lower():
            print("You guessed correctly! They have an unemployment rate of", value, "%")
        else:
            print("Incorrect. The state with the lowest unemployment rate is", state_with_lowest_unemployment['state'], "with a rate of", value, "%")
    
    answer = get_answer("view_unemployment_rates_graph","Would you like to view the Unemployment Rates by State graph? (y/n): ")
    if answer == 'y':
        visualizer.plot_unemployment_rates()

    answer = get_answer("view_happiest_states", "Would you like to see the happiest states? (y/n): ")
    if answer == 'y':
        visualizer.plot_happiness_colorcoded_bars()

    answer = get_answer("view_unemployment_happiness_correlation", "Would you like to see the correlation between unemployment and happiness? (y/n): ")
    if answer == 'y':
        visualizer.plot_happiness_correlation()

    answer = get_answer("view_economic_metrics", "Would you like to see how economic metrics, such as cost of living and median income, differs per state? (y/n): ")
    if answer == 'y':
        visualizer.plot_economy_averages()

    answer = get_answer("view_health_metrics","Would you like to see how health metrics, such as water quality, differs per state? (y/n): ")
    if answer == 'y':
        visualizer.plot_health_averages()
    
    answer = get_answer("view_safety_metrics","Would you like to see how safety metrics, such as crime rate, differs per state? (y/n): ")
    if answer == 'y':
        visualizer.plot_safety_averages()

    answer = get_answer("view_quality_of_life_comparison", "Now that you have gotten a grasp of different factors across the states, such as unemployment, safety, happiness, etc., would you like to view a comparison between the Quality of Life Comparison in different States? (y/n): ")
    if answer == 'y':
        while True:
            if 'states_to_compare' in config['answers']:
                states = config['answers']['states_to_compare']
            else:
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
