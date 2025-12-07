import sys, os
import unittest
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import PullData, Transaction, Buy, Sell, Portfolio, MarketData, Portfolio_Helper, Price_Charts_Graphs, CryptoMarketDisplay

class TestPullData(unittest.TestCase):
    """
    Test suite for PullData class (William's Section)
    Test API data retrieval and formatting
    Status - (Testing - [DONE])

    """
    def setUp(self):
        """Setting up fixtures before test method"""
        self.puller = PullData()

    def test_pulldata_initial(self):
        """
        Test: PullData initialization correctly
        """
        self.assertIsNotNone(self.puller, "PullData should initialize")
        self.assertTrue(hasattr(self.puller, 'url'), "Should have a URL Attr")

    def test_pulldata_market_data_retrieval(self):
        """
        Test: get_market_data() fetches from API
        """
        ans = self.puller.get_market_data(page=1)

        self.assertIsInstance(ans, pd.DataFrame, "Must return DataFrame")

        # Checks that symbol & curr price have columns
        if not ans.empty:
            self.assertIn('symbol', ans.columns, "Must have symbol columns")
            self.assertIn('current_price', ans.columns, "Myst have price columns")

    def test_pulldata_current_price_retrieval(self):
        """
        Test: get_current_price() fetches a specific crypto price
        """
        curr_price = self.puller.get_current_price('bitcoin', 'ethereum')

        self.assertIsInstance(curr_price, dict, "Must return dictionary")

        # Checks if price is positive
        if 'bitcoin' in curr_price:
            self.assertGreater(curr_price['bitcoin'], 0, "Bitcoin price must be non-negative")

    def test_pulldata_history(self):
        """
        Test: get_historical_data() fetches price history
        """
        ans = self.puller.get_historical_data('bitcoin', days=7)

        self.assertIsInstance(ans, pd.DataFrame, "Must return DataFrame")
        if not ans.empty:
            self.assertIn('price', ans.columns, "Must have price columns")
            self.assertIn('timestamp', ans.columns, "Myst have timestamp columns")

class TestMarketData(unittest.TestCase):
    """
    Test suite for MarketData class (Christopher's Section)
    Status - (Testing - [IN-PROCESS])
    """
    pass

class TestCryptoMarketDisplay(unittest.TestCase):
    """
    Test suite for CryptoMarketDisplay class (Linwood's section)
    Tests display formatting and user interaction
    Status - (Testing - [IN-PROCESS])
    """
    pass

class TestPortfolio(unittest.TestCase):
    """
    Test suite for Portfolio class (Bushra's Section)
    Tests wallet management and Transactions
    Status - (Testing - [IN-PROCESS])
    """
    pass

class TestTransactions(unittest.TestCase):
    """
    Test suite for Buy, Sell and Transcation classes (Bushra's Section)
    Tests Transactions functions
    Status - (Testing - [IN-PROCESS])
    """
    pass

class TestPriceChartsGraphs(unittest.TestCase):
    """
    Test suiter for Price_Charts_Graphs class (Christopher's Section)
    Tests for chart Generations and Correct I/O files
    Status - (Testing - [DONE])
    """

    def setUp(self):
        """Set up test features"""
        self.charts = Price_Charts_Graphs()
        self.market = MarketData()

    def test_charts_initial(self):
        """Test: Price_Charts_Graphs initializes properly"""
        self.assertIsNotNone(self.charts, "Charts Should initialize")

    def test_charts_price_chart_generation(self):
        """I/O Test: create_price_chart() generates chart"""
        ans = self.market.fetch_data(limit=10)

        if ans:
            chart_results= self.charts.create_price_chart(self.market, top_n=5)
            self.assertTrue(chart_results, "Charts should be created")
        else:
            # Skips Test if failed to Generate
            self.skipTest("Cannot test without any data")
    
    def test_charts_type(self):
        """Test: Chart methods are valid with input type"""
        with self.assertRaises(TypeError):
            self.charts.create_price_chart("not a MarketData Type")
        
    def test_charts_top_n(self):
        """Tests: Chart methods are vaild with top_n parameter"""
        # Not valid at 0
        with self.assertRaises(ValueError):
            self.charts.create_price_chart(self.market, top_n=0)
        
        # Not valid at this number 100
        with self.assertRaises(ValueError):
            self.charts.create_price_chart(self.market, top_n=100)



def main():
    # Creating test suites for all test classes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adding All test class to loadTestsFromTestCase()
    suite.addTest(loader.loadTestsFromTestCase(TestPullData))
    suite.addTest(loader.loadTestsFromTestCase(TestPriceChartsGraphs))

    # Running tests 
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*70)
    print("COMPLETE TEST SUITE SUMMARY")
    print("="*70)
    print(f"Total Tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    print("\nTEST COVERAGE BY COMPONENT:")
    print("- PullData (William): API data retrieval")
    print("- MarketData (Christopher): Market data & display")
    print("- CryptoMarketDisplay (Linwood): UI & formatting")
    print("- Price_Charts_Graphs (Christopher): Chart generation")
    print("- Portfolio (Bushra): Wallet management")
    print("- Transactions (Bushra): Buy/Sell operations")


if __name__ == "__main__":
    main()

