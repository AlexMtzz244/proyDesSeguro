import unittest

from src.webapp import app


class SearchSecurityTest(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_search_escapes_html_supplied_by_the_user(self):
        response = self.client.get(
            "/buscar",
            query_string={"nombre": "<script>alert(1)</script>"},
        )

        body = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("<script>alert(1)</script>", body)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", body)


if __name__ == "__main__":
    unittest.main()