# from fastapi.testclient import TestClient
# import pytest
# from app.main  import app
# from app import schemas
# from app.config import settings
# from app.database import get_db

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from app.database import Base

# #####################
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ################



# ## add fixture
# @pytest.fixture # (scope="module") #returns my database object 
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = Testing_SessionLocal()
#     ## session fixture yielding database object 
#     try:
#         yield db
#     finally:
#         db.close()
    

# @pytest.fixture #(scope="module") #returns my client object 
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db 
#     yield TestClient(app)
