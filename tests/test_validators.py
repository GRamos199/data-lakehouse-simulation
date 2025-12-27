"""
Unit tests for data validation utilities.
"""

import unittest
from src.utils import DataValidator


class TestDataValidator(unittest.TestCase):
    """Test cases for DataValidator class."""
    
    def test_valid_weather_data(self):
        """Test validation of valid weather data."""
        valid_data = {
            'coord': {'lon': -74.0, 'lat': 40.7},
            'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky'}],
            'main': {
                'temp': 20.0,
                'feels_like': 19.0,
                'pressure': 1013,
                'humidity': 65
            },
            'dt': 1234567890,
            'sys': {'country': 'US'},
            'id': 5128581,
            'name': 'New York'
        }
        self.assertTrue(DataValidator.validate_weather_data(valid_data))
    
    def test_missing_required_fields(self):
        """Test validation fails with missing required fields."""
        invalid_data = {
            'coord': {'lon': -74.0, 'lat': 40.7},
            'weather': [{'id': 800}],
            'dt': 1234567890,
            'name': 'New York'
        }
        self.assertFalse(DataValidator.validate_weather_data(invalid_data))
    
    def test_missing_main_fields(self):
        """Test validation fails with missing main fields."""
        invalid_data = {
            'coord': {'lon': -74.0, 'lat': 40.7},
            'weather': [{'id': 800}],
            'main': {'temp': 20.0},  # Missing other required fields
            'dt': 1234567890,
            'sys': {'country': 'US'},
            'id': 5128581,
            'name': 'New York'
        }
        self.assertFalse(DataValidator.validate_weather_data(invalid_data))
    
    def test_invalid_weather_array(self):
        """Test validation fails with invalid weather array."""
        invalid_data = {
            'coord': {'lon': -74.0, 'lat': 40.7},
            'weather': [],  # Empty array
            'main': {
                'temp': 20.0,
                'feels_like': 19.0,
                'pressure': 1013,
                'humidity': 65
            },
            'dt': 1234567890,
            'sys': {'country': 'US'},
            'id': 5128581,
            'name': 'New York'
        }
        self.assertFalse(DataValidator.validate_weather_data(invalid_data))


if __name__ == '__main__':
    unittest.main()
