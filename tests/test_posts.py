import pytest

from app import schemas
from tests.conftest import authorized_client


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = list(map(lambda post: schemas.PostOut(**post), res.json()))
    assert len(posts) == len(test_posts)
    assert res.status_code == 200


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert res.status_code == 200


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/69")
    assert res.status_code == 404


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401


def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


@pytest.mark.parametrize('title, content, published', [
    ("awesome_new_title", "awesome_new_content", True),
    ("beach", "beaches are good for sumer", False),
    ("pizza", "i love veggie pizz", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published}
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/",
        json={"title": "title-1", "content": "content-1"}
    )
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.published == False


def test_unauthorized_create_post(client, test_posts):
    res = client.post(
        "/posts/",
        json={"title": "title-1", "content": "content-1"}
    )
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_existent_post(authorized_client, test_user):
    res = authorized_client.delete(f"/posts/69")
    assert res.status_code == 404


def test_delete_other_users_post(authorized_client, test_user, test_posts):
    # test_user trying to delete test_user2's post
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": 'updated_title',
        "content": 'updated_content',
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**res.json())

    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert res.status_code == 202


def test_update_other_users_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": 'updated_title',
        "content": 'updated_content',
        "id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403


def test_unauthorized_update_post(client, test_posts):
    data = {
        "title": 'updated_title',
        "content": 'updated_content',
        "id": test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_update_non_existent_post(authorized_client, test_posts):
    data = {
        "title": 'updated_title',
        "content": 'updated_content',
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/69", json=data)
    assert res.status_code == 404
