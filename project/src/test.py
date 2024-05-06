import unittest
from QOLAnalysis import QOLAnalysis
from DataVisualizer import DataVisualizer
import pandas as pd
import logging 

logging.basicConfig(level=logging.INFO,
                    filename='../tests/test.log', 
                    filemode='w',  
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



class TestQOLAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qol_analysis = QOLAnalysis('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')

    def test_load_data(self):
        """
        Test data loading method to ensure data frames are loaded correctly.
        """
        self.assertIsInstance(self.qol_analysis.state_data, pd.DataFrame, "State data should be a DataFrame")
        self.assertIsInstance(self.qol_analysis.county_data, pd.DataFrame, "County data should be a DataFrame")

    def test_calculate_weighted_unemployment_rate(self):
        """
        Test that the weighted unemployment rate calculation returns a float and correctly calculates the rate.
        """
        rate = self.qol_analysis.calculate_weighted_unemployment_rate('CA')  
        self.assertIsInstance(rate, float, "The calculated rate should be a float")
        self.assertGreater(rate, 0, "The unemployment rate should be greater than 0")

    def test_get_all_weighted_unemployment_data(self):
        """
        Test that the function retrieves a DataFrame with the correct structure and data for unemployment rates.
        """
        data = self.qol_analysis.get_all_weighted_unemployment_data()
        self.assertIsInstance(data, pd.DataFrame, "Should return a DataFrame")
        self.assertTrue('state' in data.columns and 'UnemploymentRate' in data.columns, "DataFrame should have correct columns")
        self.assertGreater(data.shape[0], 0, "DataFrame should not be empty")

    def test_find_state_with_lowest_unemployment(self):
        """
        Test that the function correctly identifies the state with the lowest unemployment rate.
        """
        result = self.qol_analysis.find_state_with_lowest_unemployment()
        self.assertIsInstance(result, dict, "Should return a dictionary")
        self.assertIn('state', result, "Dictionary should have a 'state' key")
        self.assertIn('rate', result, "Dictionary should have a 'rate' key")
        self.assertLess(result['rate'], 100, "Rate should be realistic and less than 100")

    def test_find_state_with_highest_unemployment(self):
        """
        Test that the function correctly identifies the state with the highest unemployment rate.
        """
        result = self.qol_analysis.find_state_with_highest_unemployment()
        self.assertIsInstance(result, dict, "Should return a dictionary")
        self.assertIn('state', result, "Dictionary should have a 'state' key")
        self.assertIn('rate', result, "Dictionary should have a 'rate' key")
        self.assertGreater(result['rate'], 0, "Rate should be realistic and greater than 0")


class TestDataVisualizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qol_analysis = QOLAnalysis('../data/qualityoflifescores.csv', '../data/QOL_County_Level.csv')
        cls.data_visualizer = DataVisualizer(cls.qol_analysis)

    def test_plot_unemployment_rates(self):
        """
        Test plotting function to ensure it does not raise exceptions and uses correct figure sizes.
        """
        try:
            self.data_visualizer.plot_unemployment_rates((10, 5)) 
            self.data_visualizer.plot_unemployment_rates() 
        except Exception as e:
            self.fail(f"plot_unemployment_rates raised an exception {e}")
    def test_plot_quality_of_life_comparison(self):
        """
        Test the plotting of quality of life comparisons to ensure no exceptions are raised and the correct data is used.
        """
        try:
            self.data_visualizer.plot_quality_of_life_comparison(['California', 'New York'])
        except Exception as e:
            self.fail(f"plot_quality_of_life_comparison raised an exception {e}")

    def test_plot_happiness_colorcoded_bars(self):
        """
        Test the happiness color-coded bars plotting to ensure no exceptions are raised.
        """
        try:
            self.data_visualizer.plot_happiness_colorcoded_bars()
        except Exception as e:
            self.fail(f"plot_happiness_colorcoded_bars raised an exception {e}")

    def test_plot_happiness_correlation(self):
        """
        Test the plotting of happiness vs unemployment correlation to ensure no exceptions are raised.
        """
        try:
            self.data_visualizer.plot_happiness_correlation()
        except Exception as e:
            self.fail(f"plot_happiness_correlation raised an exception {e}")

    def test_plot_economy_averages(self):
        """
        Test the plotting of economy averages to ensure no exceptions are raised and correct data is used.
        """
        try:
            self.data_visualizer.plot_economy_averages()
        except Exception as e:
            self.fail(f"plot_economy_averages raised an exception {e}")

    def test_plot_health_averages(self):
        """
        Test the plotting of health averages to verify that no exceptions occur during plotting.
        """
        try:
            self.data_visualizer.plot_health_averages()
        except Exception as e:
            self.fail(f"plot_health_averages raised an exception {e}")

    def test_plot_safety_averages(self):
        """
        Test the plotting of safety averages to ensure no exceptions are raised.
        """
        try:
            self.data_visualizer.plot_safety_averages()
        except Exception as e:
            self.fail(f"plot_safety_averages raised an exception {e}")


if __name__ == '__main__':
    unittest.main()
