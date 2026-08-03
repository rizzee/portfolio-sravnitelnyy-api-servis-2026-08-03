from fastapi.testclient import TestClient
import unittest
from fastapi_app import app, tasks

class FastAPIAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        tasks.clear()

    def test_get_tasks_empty(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_task(self):
        task_data = {'id': 1, 'title': 'Test Task'}
        response = self.client.post('/tasks', json=task_data)
        self.assertEqual(response.status_code, 201)
        expected_data = {'id': 1, 'title': 'Test Task', 'description': None, 'assignee': None}
        self.assertEqual(response.json(), expected_data)

    def test_get_task(self):
        task_data = {'id': 1, 'title': 'Test Task'}
        self.client.post('/tasks', json=task_data)
        response = self.client.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        expected_data = {'id': 1, 'title': 'Test Task', 'description': None, 'assignee': None}
        self.assertEqual(response.json(), expected_data)

    def test_update_task(self):
        task_data = {'id': 1, 'title': 'Test Task'}
        self.client.post('/tasks', json=task_data)
        updated_data = {'title': 'Updated Task'}
        response = self.client.put('/tasks/1', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Updated Task')

    def test_delete_task(self):
        task_data = {'id': 1, 'title': 'Test Task'}
        self.client.post('/tasks', json=task_data)
        response = self.client.delete('/tasks/1')
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/tasks/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
