from collections import namedtuple as nt, namedtuple

Article_Fields = ['id', 'title', 'article_type', 'body', 'release_time', 'create_by',
                  'create_time', 'update_by', 'update_time']
Article = namedtuple("Article", Article_Fields)

Comment_Fields = ['id', 'article_id', 'comment', 'create_by', 'create_time', 'update_by', 'update_time']
Comment = nt("Comment", Comment_Fields)