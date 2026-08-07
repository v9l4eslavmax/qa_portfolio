import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://reqres.in/api"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def session():
    api_key = os.environ.get("REQRES_API_KEY")
    if not api_key:
        pytest.exit(
            "Не задан REQRES_API_KEY. Зарегистрируйся на https://reqres.in/signup "
            "и передай ключ через переменную окружения REQRES_API_KEY.",
            returncode=1,
        )

    s = requests.Session()
    s.headers.update({"x-api-key": api_key})
    yield s
    s.close()
