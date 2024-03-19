import pytest
from app import models 

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/", 
        json={"post_id":test_posts[0].id,
              "dir":1}
    )
    
    assert res.status_code == 201
    
@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()  
    
    return test_posts[3].id

def test_vote_on_post_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/votes/", 
        json={"post_id":test_vote,
              "dir":1}
    )
    
    assert res.status_code == 409
    
def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/votes/", 
        json={"post_id":test_vote,
              "dir":0}
    )
    assert res.status_code == 201
    
def test_delete_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/", 
        json={"post_id":test_posts[0].id,
              "dir":0}
    )
    assert res.status_code == 404
    
def test_vote_post_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/", 
        json={"post_id":1992,
              "dir":1}
    )
    assert res.status_code == 404
    
def test_vote_unauthroized_user(client, test_posts):
    res = client.post(
        "/votes/", 
        json={"post_id":test_posts[0].id,
              "dir":1}
    )
    assert res.status_code == 401  