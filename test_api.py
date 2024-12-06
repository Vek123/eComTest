import pytest_asyncio
from fastapi.testclient import TestClient
from tinydb import TinyDB

from db import fill_table
from main import app


@pytest_asyncio.fixture()
def db(tmp_path):
    db = TinyDB(tmp_path / "db.json")
    table = db.table("schemas")
    fill_table(table)
    return table


@pytest_asyncio.fixture()
def client():
    client = TestClient(app)
    return client


class TestForms:
    def test_existed_form(self, db, client):
        response = client.post(
            "/get_form",
            content="phone_field=+7 123 456 78 90&email_field=user@mail.ru&text_field=Hello World",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == 200
        assert response.text.strip("\"") == "Form email_phone_text"

    def test_existed_form_extra(self, db, client):
        response = client.post(
            "/get_form",
            content="phone_field=+7 123 456 78 90&email_field=user@mail.ru&text_field=Hello World&extra=+7 123 456 78 90",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == 200
        assert response.text.strip("\"") == "Form email_phone_text"

    def test_existed_form_extra_on_size(self, db, client):
        response = client.post(
            "/get_form",
            content="phone_field=+7 123 456 78 90&email_field=user@mail.ru&text_field=Hello&date_field=01.01.2001",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == 200
        assert response.text.strip("\"") == "Form email_phone_date"

    def test_not_existed_form(self, db, client):
        response = client.post(
            "/get_form",
            content="field1=+7 123 456 78 90&field2=user@mail.ru&field3=Hello World",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == 200
        assert response.json() == {"field1": "phone", "field2": "email", "field3": "text"}

    def test_invalid_form(self, db, client):
        response = client.post(
            "/get_form",
            content="field1:+7 123 456 78 90",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == 422
