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
    Status - (Testing - [DONE])
    """
    def setUp(self):
        self.market = MarketData()

    def test_marketdata_initial(self):
        """
        Test: MarketData is initialized with a vaild input 
        """
        self.assertIsNone(self.market, "MarketData should have a value")
        self.assertEqual(self.market._base_currency, 'usd', "Should have USD as default")

    def test_marketdata_initial_check(self):
        """
        Test: MarketData should reject an invalid currency
        """
        with self.assertRaises(ValueError):
            # There is nothing - Should raise
            MarketData("")
        
        with self.assertRaises(ValueError):
            # There is nothing - Should raise
            MarketData(" ")
        
    def test_marketdata_data_fetch_success(self):
        """
        I/O Test: Checking if fetch_data() gets all market Data
        """
        ans = self.market.fetch_data(limit=10)

        if ans:
            self.assertTrue(ans, "Should return True if successful with fetch")
            self.assertFalse(self.market.data.empty, "Must have data")
        else:
            self.skipTest("Unable to fetch API")
    
    def test_marketdata_limit(self):
        """
        Test: fetch_data() limit parameter
        """
        # When limit is zero
        with self.assertRaises(ValueError):
            self.market.fetch_data(limit=0)

        # When limit is above possible value
        with self.assertRaises(ValueError):
            self.market.fetch_data(limit=300)

    def test_marketdata_timestamp(self):
        """
        Test: Update timestamp to be tracked
        """
        self.assertIsNone(self.market.previous_update, "Must be none before fetch")

        ans = self.market.fetch_data(limit=10)

        if ans:
            self.assertIsNotNone(self.market.previous_update, "Must have a timestamp after fetch")
        
    def test_marketdata_lookup_valid(self):
        """
        Test: get_crypto_price() has a vaild input
        """
        with self.assertRaises(ValueError):
            self.market.get_crypto_price("")
        
        with self.assertRaises(ValueError):
            self.market.get_crypto_price(" ")


class TestCryptoMarketDisplay(unittest.TestCase):
    """
    Test suite for CryptoMarketDisplay class (Linwood's section)
    Tests display formatting and user interaction
    Status - (Testing - [DONE])
    """
    
    def setUp(self):
        """setting up fixtures"""
        # An example 
        self.sample_data = pd.DataFrame([
            {
                'name': 'Bitcoin',
                'symbol': 'btc',
                'current_price': 50000.00,
                'change_24h': 2.5
            },
            {
                'name': 'Ethereum',
                'symbol': 'eth',
                'current_price': 3000.00,
                'change_24h': -1.2
            }
        ])

    def test_display_initial(self):
        """Test: CryptoMarketDisplay as DataFrame """
        display = CryptoMarketDisplay(self.sample_data)
        self.assertIsNone(display, "Display should start")

    def test_display_initial_valid(self):
        """Test: Checks if CryptoMarketDisplay reject non-DataFrame"""
        with self.assertRaises(TypeError):
            CryptoMarketDisplay("Not a DataFrame Type")

        with self.assertRaises(TypeError):
            CryptoMarketDisplay(None)
    


class TestPortfolio(unittest.TestCase):
    """
    Test suite for Portfolio class (Bushra's Section)
    Tests wallet management and Transactions
    Status - (Testing - [DONE])
    """
    def setUp(self):
        """Set up test fixtures"""
        self.portfolio = Portfolio(1000)
    
    def test_portfolio_initial(self):
        """Test: Portfolio initializes with starting funds"""
        self.assertEqual(self.portfolio.funds, 10000, "Should start with correct funds")

    def test_portfolio_balance_tracking(self):
        """Persistence Test: Portfolio tracks balance changes"""
        initial = self.portfolio.funds
        self.portfolio.funds -= 1000
        
        self.assertEqual(self.portfolio.funds, initial - 1000, "Balance should persist changes")

    def test_portfolio_see_current_funds(self):
        """Persistence Test: seeCurrentFunds() returns balance"""
        funds = self.portfolio.seeCurrentFunds()
        
        self.assertEqual(funds, 10000.00, "Should return current funds")
        self.assertIsInstance(funds, float, "Should return float")

    def test_portfolio_see_value_empty(self):
        """Test: seePortfolioValue() handles empty portfolio"""
        value = self.portfolio.seePortfolioValue()
        self.assertEqual(value, 0.0, "Empty portfolio should have 0 value")


class TestTransactions(unittest.TestCase):
    """
    Test suite for Buy, Sell and Transcation classes (Bushra's Section)
    Tests Transactions functions
    Status - (Testing - [DONE])
    """
    def test_buy_inheritance(self):
        """Test: Buy inherits from Transaction"""
        self.assertTrue(issubclass(Buy, Transaction), "Buy should be Transaction subclass")

    def test_sell_inheritance(self):
        """Test: Sell inherits from Transaction"""
        self.assertTrue(issubclass(Sell, Transaction), "Sell should be Transaction subclass")

    def test_transaction_abstract_class(self):
        """Test: Transaction is abstract base"""
        self.assertTrue(hasattr(Transaction, 'value'), "Transaction should have value method")

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
    suite.addTest(loader.loadTestsFromTestCase(TestMarketData))
    suite.addTest(loader.loadTestsFromTestCase(TestCryptoMarketDisplay))
    suite.addTest(loader.loadTestsFromTestCase(TestPortfolio))
    suite.addTest(loader.loadTestsFromTestCase(TestTransactions))

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

