from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models


class Database:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def _get_or_create(self, session, model, unique_field, data: dict):
        instance: model = session.query(model).filter_by(
            **{unique_field: data[unique_field]}
        ).first()
        if not instance:
            instance = model(**data)
            session.add(instance)
            try:
                session.commit()
            except Exception as exc:
                print(exc)
                session.rollback()
        return instance

    def _comment_unpack(self, session, comments):
        comments_list = []
        for comment in comments:
            if comment["comment"]["children"]:
                user = self._get_or_create(
                    session,
                    models.Writer,
                    "url",
                    {
                        "url": comment["comment"]["user"]["url"],
                        "name": comment["comment"]["user"]["full_name"],
                    }
                )
                comm_inserting = self._get_or_create(
                    session,
                    models.Comment,
                    "id",
                    {
                        "id": comment["comment"]["id"],
                        "text": comment["comment"]["body"],
                        "author": user.name
                    }
                )
                comments_list.append(comm_inserting)
                comments_list.extend(self._comment_unpack(session, comment["comment"]["children"]))

        return comments_list

    def create_post(self, data):
        session = self.maker()
        post = self._get_or_create(session, models.Post, "url", data["post_data"])
        writer = self._get_or_create(session, models.Writer, "url", data["writer_data"])
        tags = [
            self._get_or_create(session, models.Tag, "url", tag_data)
            for tag_data in data["tags_data"]
        ]
        comments = self._comment_unpack(session, data["comments_data"])

        post.writer = writer
        post.tags.extend(tags)
        post.comments.extend(comments)
        session.add(post)
        try:
            session.commit()
        except Exception as exc:
            print(exc)
            session.rollback()
        finally:
            session.close()
