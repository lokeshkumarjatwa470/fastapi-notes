from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def setup_function():
    main.notes_db.clear()
    main.next_id = 1


def test_login_and_me():
    unauthenticated = client.get("/me")
    assert unauthenticated.status_code == 401

    login = client.post(
        "/login",
        json={"username": "admin", "password": "password123"},
    )
    assert login.status_code == 200
    assert login.json() == {"access_token": "demo-token", "token_type": "bearer"}

    me = client.get("/me")
    assert me.status_code == 200
    assert me.json()["username"] == "admin"


def test_invalid_login():
    response = client.post(
        "/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_note_crud_and_patch():
    created = client.post(
        "/notes",
        json={"title": "Learning", "content": "FastAPI notes"},
    )
    assert created.status_code == 201
    note_id = created.json()["id"]

    listed = client.get("/notes")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    patched = client.patch(f"/notes/{note_id}", json={"content": "Updated content"})
    assert patched.status_code == 200
    assert patched.json()["title"] == "Learning"
    assert patched.json()["content"] == "Updated content"

    updated = client.put(
        f"/notes/{note_id}",
        json={"title": "Changed", "content": "Replacement content"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Changed"

    deleted = client.delete(f"/notes/{note_id}")
    assert deleted.status_code == 204
    assert client.get(f"/notes/{note_id}").status_code == 404


def test_validation_and_missing_note():
    invalid = client.post("/notes", json={"title": "", "content": "hello"})
    assert invalid.status_code == 422

    missing = client.get("/notes/999")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Note not found"
