import unittest
import json
from unittest.mock import patch
from src.backend.app import app
import requests
from flask import Flask


class TestAppInitialization(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_it_app_initialization(self):
        # Ensure app is a Flask app, and it has 'test_client' method.
        self.assertIsInstance(self.app.application, Flask)  # Access the Flask app instance
        self.assertTrue(hasattr(self.app.application, 'test_client'))  # Check if it has 'test_client'


class TestSearchRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_it_search_books(self):
        response = self.app.get('/search?title=Python')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))

    def test_it_search_with_author_query(self):
        response = self.app.get('/search?author=Martin')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))

    def test_it_search_with_subject_query(self):
        response = self.app.get('/search?subject=Science')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))

    def test_it_search_missing_all_params(self):
        response = self.app.get('/search')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'At least one of title, author, or subject query parameters is required')


class TestExternalAPIConnection(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_it_mock_external_api_connection(self):
        mocked_response = {
            "docs": [{
                "title": "Test Book",
                "author_name": ["Test Author"],
                "key": "/works/OL12345W",
                "cover_i": "123456"
            }]
        }

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mocked_response

            response = self.app.get('/search?title=Python')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data[0]['title'], "Test Book")
            self.assertEqual(data[0]['author'], "Test Author")


class TestResponseStructure(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_it_search_response_is_json(self):
        response = self.app.get('/search?title=Python')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_it_search_response_field_structure(self):
        response = self.app.get('/search?title=Python')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        for book in data:
            self.assertIn('title', book)
            self.assertIsInstance(book['title'], str)

            self.assertIn('author', book)
            self.assertIsInstance(book['author'], str)

            self.assertIn('link', book)
            self.assertIsInstance(book['link'], str)

            self.assertIn('image', book)
            self.assertTrue(isinstance(book['image'], str) or book['image'] is None)


class TestErrorHandling(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_it_search_no_results(self):
        response = self.app.get('/search?title=NonExistentBook')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])

    def test_it_search_api_failure(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("API request failed")

            response = self.app.get('/search?title=Python')
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'API request failed')


class TestEdgeCases(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_it_search_with_special_characters(self):
        response = self.app.get('/search?title=%C2%A9%20Python')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))

    def test_it_search_with_empty_query(self):
        response = self.app.get('/search?title=')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'At least one of title, author, or subject query parameters is required')


class TestIndexRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_it_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
