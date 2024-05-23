from e6blogs.utils import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


db = SQLAlchemy()


class ModelBase:
	def fetch_all(self, query):
		query = text(query)
		cursor = db.session.execute(query)
		keys = cursor.keys()
		data = cursor.fetchall()
		if data:
			return jsonify(keys, data, many=True)

		return []

	def fetch_one(self, query):
		query = text(query)

		cursor = db.session.execute(query)
		keys = cursor.keys()
		data = cursor.fetchone()
		if data:
			return jsonify(keys, data, many=False)

		return {}

	def execute_query(self, query, fetch=False):
		query = text(query)
		cursor = db.session.execute(query)
		json_data = {}
		if fetch:
			keys = cursor.keys()
			data = cursor.fetchone()
			if data:
				json_data = jsonify(keys, data, many=False)

		db.session.commit()
		return json_data

	def parse_update_cols(self, data):
		if len(data) == 1:
			update_columns = f"""
	            {', '.join(str(key) for key in data.keys())} = {", ".join([f"'{str(val)}'" for val in data.values()])}
	        """
		else:
			update_columns = f"""
			( {', '.join(str(key) for key in data.keys())} ) 
			=
			( {", ".join([f"'{str(val)}'" for val in data.values()])} ) 
			"""

		return update_columns

	def parse_insert_cols(self, details):
		keys = ', '.join(details.keys())
		values = [f"'{i}'" for i in details.values()]
		values = ", ".join(values)

		return keys, values


class User(ModelBase):
	def __init__(self):
		self.meta = {}
		self.found = False

	def add(self, data):
		keys, values = self.parse_insert_cols(data)
		
		query = f"""INSERT INTO user ( {keys} ) VALUES ( {values} ) RETURNING *"""

		json_data = self.execute_query(query, fetch=True)
		self.found = True
		self.meta = json_data
		return self

	def update(self, data):
		update_columns = self.parse_update_cols(data)

		query = f"""
			UPDATE user
			SET {update_columns}
			WHERE id = {self.meta['id']}
			RETURNING *
		"""
		json_data = self.execute_query(query, fetch=True)
		self.meta = json_data

	def query(self, user_id=None, email=None, auth_token=None):
		auth_token_clause = ''
		if auth_token:
			auth_token_clause = f" AND auth_token = '{auth_token}' "

		user_id_clause = ''
		if user_id:
			user_id_clause = f" AND id = {user_id} "

		email_clause = ''
		if email:
			email_clause = f" AND email = '{email}' "

		query = f"""SELECT * FROM user
			WHERE True
			{user_id_clause}
			{email_clause}
			{auth_token_clause}
		"""

		data = self.fetch_one(query)
		if data:
			self.found = True
			self.meta = data
		return self

	def query_all(self, data):
		user_id_clause = ''
		if 'user_id' in data:
			user_id_clause = f" AND id = {data['user_id']} "

		email_clause = ''
		if 'email' in data:
			email_clause = f""" AND email = '{data["email"]}' """

		query = f"""SELECT * FROM user
			WHERE True
			{user_id_clause}
			{email_clause}
		"""

		return self.fetch_all(query)

	def login(self, auth_token):
		query = f"""UPDATE user
		SET auth_token = '{auth_token}'
		WHERE id = {self.meta['id']}
		RETURNING *
		"""
		resp = self.execute_query(query, fetch=True)
		self.meta = resp

	def logout(self):
		query = f"""UPDATE user
		SET auth_token = null
		WHERE id = {self.meta['id']}
		"""
		self.execute_query(query)


class Blog(ModelBase):
	def __init__(self):
		self.meta = {}
		self.found = False

	def add(self, data):
		keys, values = self.parse_insert_cols(data)

		query = f"""INSERT INTO blog ( {keys} ) VALUES ( {values} ) RETURNING *"""

		json_data = self.execute_query(query, fetch=True)
		self.found = True
		self.meta = json_data
		return self

	def update(self, data):
		update_columns = self.parse_update_cols(data)

		query = f"""
			UPDATE blog
			SET {update_columns}
			WHERE id = {self.meta['id']}
			RETURNING *
		"""
		json_data = self.execute_query(query, fetch=True)
		self.meta = json_data

	def delete(self):
		query = f"""
		DELETE FROM blog WHERE id = {self.meta['id']}
		"""
		return self.execute_query(query)

	def query(self, blog_id, author=None):
		author_clause = ''
		if author:
			author_clause = f""" AND author = {author} """

		query = f"""SELECT * FROM blog
			WHERE id = {blog_id}
			{author_clause}
		"""

		data = self.fetch_one(query)
		if data:
			self.found = True
			self.meta = data
		return self

	def query_all(self, data):
		offset_clause = f" AND id > {data.get('cursor', 0)} "

		blog_id_clause = ''
		if 'blog_id' in data:
			blog_id_clause = f" AND id = {data['blog_id']} "

		created_at_clause = ''
		if 'created_at' in data:
			created_at_clause = f" AND created_at = {data['created_at']} "

		author_clause = ''
		if 'author' in data:
			author_clause = f""" AND author = {data['author']} """

		query = f"""SELECT * FROM blog
			WHERE True
			{blog_id_clause}
			{created_at_clause}
			{author_clause}
			{offset_clause}
			LIMIT 30
		"""

		return self.fetch_all(query)
