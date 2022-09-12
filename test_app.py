import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, db_drop_create, setup_db, Actor, Movie, Show
from config import bearer_tokens
from sqlalchemy import desc
from datetime import date
from app import create_app


casting_assistant_auth_h = {
    'Authorization': bearer_tokens['casting_assistant']
}
casting_director_auth_h = {
    'Authorization': bearer_tokens['casting_director']
}
executive_producer_auth_h = {
    'Authorization': bearer_tokens['executive_producer']
}
database_path =os.environ['DATABASE_URL']

class capstoneTestCases(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path 
        setup_db(self.app, self.database_path)
        db_drop_create()
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
   
    def test_get_actors(self):
        res = self.client().get('/actors?page=1', headers = casting_assistant_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['actors']))

    def test_404_get_actors(self):
        res = self.client().get('/actors?page=999999', headers = casting_assistant_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'resource not found')
    
    def test_401_get_actors(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header not found')

    def test_post_actor(self):
        json_post_actor = {
            'name' : 'alex',
            'age' : 23
        } 
        res = self.client().post('/actors', json = json_post_actor, headers = casting_director_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['created'], 2)
    
    def test_422_post_actor(self):
        json_create_actor_without_name = {'age' : 23} 
        res = self.client().post('/actors', json = json_create_actor_without_name, headers = casting_director_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_401_post_actor(self):
        json_post_actor = {
            'name' : 'alex',
            'age' : 23
        } 
        res = self.client().post('/actors', json = json_post_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header not found')


    def test_patch_actor(self):
        json_patch_actor_with_new_age = {
            'age' : 27
        } 
        res = self.client().patch('/actors/1', json = json_patch_actor_with_new_age, headers = casting_director_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(data['actor']) )
        self.assertEqual(data['updated'], 1)

    def test_400_patch_actor(self):
            res = self.client().patch('/actors/785544', headers = casting_director_auth_h)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'] , 'bad request')

    def test_404_patch_actor(self):
        json_patch_actor_with_new_age = {
            'age' : 27
        } 
        res = self.client().patch('/actors/887765', json = json_patch_actor_with_new_age, headers = casting_director_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'resource not found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=executive_producer_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/122122', headers = casting_director_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'resource not found')
    
    def test_401_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header not found')

    def test_get_movies(self):
        res = self.client().get('/movies?page=1', headers = casting_assistant_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_get_movies(self):
        res = self.client().get('/movies?page=333444', headers = casting_assistant_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'resource not found')
    
    def test_error_401_get_all_movies(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header not found')

    def test_post_movie(self):
        add_movie = {'title': 'New_Movie',
                     'release_date': '12/9/2022'}
        res = self.client().post('/movies', json=add_movie, headers=executive_producer_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 2)

    def test_422_post_movie(self):
        add_movie = {}
        res = self.client().post('/movies', json=add_movie,headers=executive_producer_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual( data['message'], 'unprocessable')

    def test_patch_movie(self):
        json_patch_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/1', json = json_patch_movie, headers = executive_producer_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_400_patch_movie(self):
        res = self.client().patch('/movies/1', headers = executive_producer_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'bad request')
    
    def test_404_patch_movie(self):
        json_patch_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/346665', json = json_patch_movie, headers = executive_producer_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'resource not found in database.')


    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers = executive_producer_auth_h)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '1')

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/87655', headers = executive_producer_auth_h) 
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'resource not found in database.')

    def test_401_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header not found')

if __name__ == "__main__":
    unittest.main()

