import unittest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

class TestMainEndpoints(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test_register_user(self):
        response = client.post(
            "/register/",
            json={"email": "test@example.com", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.json())

    def test_confirm_email(self):
        from utils.token import generate_verification_token
        token = generate_verification_token("test@example.com")
        response = client.get(f"localhost:8000/confirm-email/?token={token}&email=test@example.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Email has been confirmed"})

if __name__ == "__main__":
    unittest.main()
