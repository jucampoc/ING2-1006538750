import os
import pytest
from unittest.mock import patch, MagicMock

os.environ.setdefault('MONGO_URI', 'mongodb://mock-uri')


@pytest.fixture
def client():
    with patch('pymongo.MongoClient') as mock_mongo:

        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_db.medical_records = mock_collection
        mock_mongo.return_value.__getitem__.return_value = mock_db
        mock_mongo.return_value.hospital_db = mock_db

        # Recargar app con el mock activo
        import importlib
        import app as flask_app
        importlib.reload(flask_app)

        flask_app.app.config['TESTING'] = True
        flask_app.records_collection = mock_collection

        with flask_app.app.test_client() as test_client:
            test_client._mock_collection = mock_collection
            yield test_client