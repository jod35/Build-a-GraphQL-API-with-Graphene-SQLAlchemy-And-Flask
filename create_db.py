from db import User,Post,Base,engine


print("Creating database......")


Base.metadata.create_all(bind=engine)
