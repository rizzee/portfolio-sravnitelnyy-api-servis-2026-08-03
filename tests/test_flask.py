import unittest
from flask_app import app as flask_app, tasks

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = flask_app.test_client()
        self.app.testing = True
        tasks.clear()

    def test_get_tasks_empty(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_task(self):
        task_data = {'id': 1, 'title': 'Test Task'}
        response = self.app.post('/tasks', json=task_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], 'Test Task')

    def test_get_task_by_id(self):
        task_data = {'id': 1, 'title': 'Test Task'}
        self.app.post('/tasks', json=task_data)
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Test Task')

    def test_update_task(self):
        task_data = {'id': 1, 'title': 'Test Task'}
        self.app.post('/tasks', json=task_data)
        updated_data = {'title': 'Updated Task'}
        response = self.app.put('/tasks/1', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Updated Task')

    def test_delete_task(self):
        task_data = {'id': 1, 'title': 'Test Task'}
        self.app.post('/tasks', json=task_data)
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 204)
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
