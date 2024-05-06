# Quality of Life and Unemployment Rates Throughout the United States
This project uses Python to analyze and visualize data related to Quality of Life and unemployment rates across the United States. It offers an interactive way for users to explore various aspects of the data through questions and visualizations. Users can view graphical representations of unemployment rates, happiness indexes, economic metrics, and more, across different states.
## Installation and Setup
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Getting the Project Going
To get started, clone the repository to your local machine:
1. Navigate to the project directory [FINALPROJECTCHARLES]
2. Setup Virtual Env: python -m venv env
3. Activate the virtual environment:
- On Windows:
project\Scripts\activate
- On MacOS/Linux:
source project/venv/bin/activate
4. Install all dependencies that are required for the project:
- pip install -r requirements.txt

## Once setup...


### Main.py Overview

**`main.py`** is the entry point of the application. It leverages the `QOLAnalysis` and `DataVisualizer` classes to process and visualize data. The script interacts with users through the console, offering a guided exploration based on user responses.

#### Configuration
- The script uses a configuration file (`config.yaml`), located in the `../config` directory. This file contains preset answers to some of the questions posed during execution. Users can alter this file to change or remove preset answers, which allows modifications to the script's execution without direct code changes.

#### Logging
- All significant operations and outcomes are logged to `../tests/main.log`. This logging helps track the flow of operations and assists in troubleshooting and analyzing the application.

### Test.py Overview

**`test.py`** contains tests designed to ensure that the functionalities within `QOLAnalysis` and `DataVisualizer` operate correctly. This file tests various system components to maintain robustness and reliability.

#### Logging for Tests
- Similar to the main application, all test activities are logged to `../tests/test.log`. This provides a detailed record of all test executions.

### Interactive Features

The script prompts users with questions to guide them through different data visualizations:
- Users can guess which states have the highest or lowest unemployment rates and verify their guesses against the actual data.
- Graphical visualizations for unemployment rates, state happiness, and correlations between happiness and unemployment are available based on user choices.
- Users can opt to visualize economic, health, and safety metrics across states.
- Users can select specific states for a detailed comparative analysis of Quality of Life metrics.

### Running the Application

To run the application, navigate to the directory containing `main.py`, which is `project/src`, and execute the following command:
```bash
python main.py
```

To run the tests, navigate to the directory containing `test.py`,  which is `project/src`, and execute the following command:
```bash
python test.py
```


