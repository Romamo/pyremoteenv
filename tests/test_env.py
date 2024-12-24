from unittest.mock import MagicMock, patch
import unittest
from remoteenv.env import Env


class TestEnv(unittest.TestCase):
    @patch("remoteenv.env.create_backend")
    def test_set_success(self, mock_create_backend):
        # Arrange
        backend_mock = MagicMock()
        mock_create_backend.return_value = backend_mock
        env = Env(backend="mock_backend")
        key = "TEST_KEY"
        value = "TEST_VALUE"

        # Act
        env.set(key, value)

        # Assert
        backend_mock.set.assert_called_once_with(key, value)

    @patch("remoteenv.env.create_backend")
    def test_set_key_empty_string(self, mock_create_backend):
        # Arrange
        backend_mock = MagicMock()
        mock_create_backend.return_value = backend_mock
        env = Env(backend="mock_backend")
        key = ""
        value = "TEST_VALUE"

        # Act / Assert
        with self.assertRaises(ValueError):
            env.set(key, value)

    @patch("remoteenv.env.create_backend")
    def test_set_value_empty_string(self, mock_create_backend):
        # Arrange
        backend_mock = MagicMock()
        mock_create_backend.return_value = backend_mock
        env = Env(backend="mock_backend")
        key = "TEST_KEY"
        value = ""

        # Act / Assert
        with self.assertRaises(ValueError):
            env.set(key, value)

    @patch("remoteenv.env.create_backend")
    def test_set_backend_raises_exception(self, mock_create_backend):
        # Arrange
        backend_mock = MagicMock()
        backend_mock.set.side_effect = Exception("Backend error")
        mock_create_backend.return_value = backend_mock
        env = Env(backend="mock_backend")
        key = "TEST_KEY"
        value = "TEST_VALUE"

        # Act / Assert
        with self.assertRaises(Exception) as context:
            env.set(key, value)
        self.assertEqual(str(context.exception), "Backend error")


if __name__ == "__main__":
    unittest.main()