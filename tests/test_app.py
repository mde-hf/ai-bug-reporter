import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, calculate_similarity

class TestBugReporter(unittest.TestCase):
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_route(self):
        """Test that the main page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bug Reporter', response.data)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
        self.assertIn('epic', data)
    
    def test_calculate_similarity_exact_match(self):
        """Test similarity calculation for exact matches"""
        title = "Login button not working"
        issue = {
            'fields': {
                'summary': "Login button not working",
                'description': "Same issue"
            }
        }
        similarity = calculate_similarity(title, "Test description", issue)
        self.assertGreaterEqual(similarity, 90)
    
    def test_calculate_similarity_substring_match(self):
        """Test similarity calculation for substring matches"""
        title = "Login error"
        issue = {
            'fields': {
                'summary': "User encounters login error on mobile",
                'description': "Login fails"
            }
        }
        similarity = calculate_similarity(title, "Test description", issue)
        self.assertGreater(similarity, 70)
    
    def test_calculate_similarity_no_match(self):
        """Test similarity calculation for non-matching titles"""
        title = "Payment processing issue"
        issue = {
            'fields': {
                'summary': "Dark mode toggle not working",
                'description': "UI issue"
            }
        }
        similarity = calculate_similarity(title, "Test description", issue)
        self.assertLess(similarity, 50)

if __name__ == '__main__':
    unittest.main()
