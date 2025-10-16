from app.database import engine, Base
from app import models

#Creates a table if necessary
Base.metadata.create_all(bind=engine)