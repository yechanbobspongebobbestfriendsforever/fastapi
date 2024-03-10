#special file that pytest uses.
#It allows us to define fixtures in here. And any fixture you define in this fille will automatically be accessible to to any of the test in the package - anything within the test folder


from fastapi.testclient import TestClient
import pytest
from app.main  import app
from app import schemas
from app.config import settings
from app.database import get_db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
from app.oauth2 import create_access_token
from app import models

#####################
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

################


## add fixture
@pytest.fixture # (scope="module") #returns my database object 
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    ## session fixture yielding database object 
    try:
        yield db
    finally:
        db.close()
    

@pytest.fixture #(scope="module") #returns my client object 
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db 
    yield TestClient(app)


@pytest.fixture(scope="function")
def test_user(client):
    user_data = {
        "email": "yck@gmail.com",
        "password": "password123"
    }
    res = client.post('/users/', json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    
    return new_user

@pytest.fixture(scope="function")
def test_user2(client):
    user_data = {
        "email": "YECHANK@gmail.com",
        "password": "password123"
    }
    res = client.post('/users/', json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user.get('id')})


@pytest.fixture(scope="function")
def test_posts(test_user, test_user2, session):
    posts_data = [{
    "title": "first title",
    "content": "first content",
    "owner_id": test_user['id']
    }, {
    "title": "2nd title",
    "content": "2nd content",
    "owner_id": test_user['id']
    },
    {
    "title": "3rd title",
    "content": "3rd content",
    "owner_id": test_user['id']
    }, {
    "title": "4th title",
    "content": "4th content",
    "owner_id": test_user2['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)
        
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts
 
@pytest.fixture
def authorized_client(client, token):
    #take original client, add specific header that we get from token fixture  
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
        
    }
    return client



