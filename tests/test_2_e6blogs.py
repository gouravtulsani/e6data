from tests.test_1_users import get_user_details


def create_blog(client, data, headers):
	return client.post('/api/blog/add', json=data, headers=headers)


def update_blog(client, blog_id, data, headers):
	return client.post(
		f'/api/blog/{blog_id}/update', json=data, headers=headers
	)


def list_all_blogs(client, data, headers):
	return client.get('/api/blog/all', query_string=data, headers=headers)


def get_blog_details(client, blog_id, headers):
	return client.get(f'/api/blog/{blog_id}/details', headers=headers)


def delete_blog(client, blog_id, headers):
	return client.delete(
		f'/api/blog/{blog_id}/delete', headers=headers
	)


def test_create_blog(client):
	headers = {"Authorization": f"Bearer {get_user_details(client)['auth_token']}"}
	data = {
		"title": "First Blog!",
		"content": "My first Blog post!"
	}
	resp = create_blog(client, data, headers=headers)

	assert resp.status_code == 200
	assert resp.json['status'] == 'success'


def test_update_blog(client):
	headers = {"Authorization": f"Bearer {get_user_details(client)['auth_token']}"}
	data = {
		"title": "First Blog!",
		"content": "My first Blog post update!"
	}
	blog_id = 1
	resp = update_blog(client, blog_id, data, headers=headers)

	assert resp.status_code == 200
	assert resp.json['status'] == 'success'


def test_fetch_by_id(client):
	headers = {"Authorization": f"Bearer {get_user_details(client)['auth_token']}"}
	blog_id = 1
	resp = get_blog_details(client, blog_id, headers=headers)

	assert resp.status_code == 200
	assert resp.json['status'] == 'success'


def test_delete_blog(client):
	headers = {"Authorization": f"Bearer {get_user_details(client)['auth_token']}"}
	blog_id = 1
	resp = delete_blog(client, blog_id, headers=headers)
	assert resp.status_code == 200
	assert resp.json['status'] == 'success'
