from typing import List
from app import schemas
import pytest


def test_get_all_post(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        return schemas.PostOut(**post)
    
    post_map = list(map(validate, res.json()))
    post_list = list(post_map)
    
    assert isinstance(post_map[0], schemas.PostOut)
    assert res.status_code == 200
    
    
def test_unauthroized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    

def test_unauthroized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/1992")
    assert res.status_code == 404
    
    
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={
            "title":title,
            "content":content,
            "published":published
        }
    )
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    
    
def test_create_post_default_published_true(authorized_client, test_user,test_posts):
    res = authorized_client.post(
        "/posts/",
        json={
            "title":"RANDOM TITLE",
            "content":"RANDOM CONTENT",
        }
    )
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "RANDOM TITLE"
    assert created_post.content == "RANDOM CONTENT"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']
    
def test_unauthroized_user_create_post(client, test_posts):
    res = client.post(
        "/posts/",
        json={
            "title":"RANDOM TITLE",
            "content":"RANDOM CONTENT",
        }
    )
    assert res.status_code == 401
    

def test_unauthroized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
    
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    
def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/1992")
    assert res.status_code == 404
    
    
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[-1].id

    }
    res = authorized_client.put(f"/posts/{test_posts[-1].id}", json=data)

    assert res.status_code == 403
    
    
def test_unauthroized_user_update_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[-1].id

    }
    res = authorized_client.put(f"/posts/1992", json=data)
    assert res.status_code == 404
    
    