import json


class TestPageEndpoints:
    # Test if the homepage responds with a 200 status.
    def test_home_page_works(self, app):
        with app.test_client() as tc:
            response = tc.get('/')
            assert response.status_code == 200

    # Test if the posts endpoint responds with a 200 status when the post is found.
    # Post one should exist because it has been placed in the database in the migration.
    def test_post_page_works(self, app):
        with app.test_client() as tc:
            response = tc.get('/post/1')
            assert response.status_code == 200

    # Test if the posts endpoint responds with a 404 status if the post was not found.
    # Post 1000 should not exist.
    def test_non_existing_post(self, app):
        with app.test_client() as tc:
            response = tc.get('/post/1000')
            assert response.status_code == 404


class TestUserLogin:
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    def test_login_correct_credentials(self, client):
        data = {
            'username': 'admin',
            'password': '24augustus'
        }
        url = '/do_login'

        response = client.post(url, data=json.dumps(data), headers=self.headers)
        assert response.status_code == 200

    def test_login_wrong_credentials(self, client):
        data = {
            'username': 'admin',
            'password': '29augustus'
        }
        url = '/do_login'

        response = client.post(url, data=json.dumps(data), headers=self.headers)
        # This test should result in a 401, password incorrect.
        assert response.status_code == 401

    def test_registration_new_credentials(self, client):
        data = {
            'username': 'someArbitraryUserName',
            'password': '@penstaartje',
            'email': 'test@gebruiker.com',
        }
        url = '/do_register'

        response = client.post(url, data=json.dumps(data), headers=self.headers)
        # This test should return 200 for a successful user registration.
        assert response.status_code == 200

    def test_registration_with_existing_username(self, client):
        data = {
            'username': 'admin',
            'password': '@penstaartje',
            'email': 'test@gebruiker.com',
        }
        url = '/do_register'

        response = client.post(url, data=json.dumps(data), headers=self.headers)
        # This test should return 500 because the user exists.
        assert response.status_code == 500
