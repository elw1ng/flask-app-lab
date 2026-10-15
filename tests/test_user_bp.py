import unittest

from app import app


class UserBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page_displays_uppercase_name_and_age(self):
        response = self.client.get("/users/hi/john?age=30")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"Age: 30", response.data)

    def test_admin_redirects_to_administrator_greeting(self):
        response = self.client.get("/users/admin", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"Age: 45", response.data)


if __name__ == "__main__":
    unittest.main()
