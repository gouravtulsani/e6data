def register_user(client, data):
	return client.post('/api/user/register', json=data)


def login(client, data=None):
	return client.post('/api/user/login', json=data)


def get_user_details(client):
	resp = login(client, data={
		"email": "abc@xyz.com",
		"password": "123456"
	})
	return resp.json['details']


def logout(client, headers):
	return client.get('/api/user/logout', headers=headers)


def list_users(client, headers=None):
	return client.get('/api/user/all', headers=headers)


def test_register_user_success(client):
	data = {
		"first_name": "hello",
		"last_name": "world",
		"email": "abc@xyz.com",
		"password": "123456"
	}
	resp = register_user(client, data)
	assert resp.status_code == 200
	assert resp.json['status'] == 'success'


def test_register_user_email_exists(client):
	data = {
		"first_name": "hello",
		"last_name": "world",
		"email": "abc@xyz.com",
		"password": "123456"
	}
	resp = register_user(client, data)

	assert resp.status_code == 400
	assert resp.json['msg'] == 'email already exists!'


def test_register_user_invalid_password(client):
	data = {
		"first_name": "hello",
		"last_name": "world",
		"email": "abcef@xyz.com",
		"password": "123"
	}
	resp = register_user(client, data)
	assert resp.status_code == 400


def test_successful_login(client):
	data = {
		"email": "abc@xyz.com",
		"password": "123456"
	}
	resp = login(client, data)
	assert resp.status_code == 200
	assert resp.json['status'] == 'success'


def test_login_invalid_passwd(client):
	data = {
		"email": "abc@xyz.com",
		"password": "12345678"
	}
	resp = login(client, data)

	assert resp.status_code == 400
	assert resp.json['msg'] == 'Invalid email or password'


def test_login_invalid_email(client):
	data = {
		"email": "abcdef@xyz.com",
		"password": "12345678"
	}
	resp = login(client, data)

	assert resp.status_code == 400
	assert resp.json['msg'] == 'user not found!'


def test_list_users(client):
	user_token = get_user_details(client)['auth_token']
	headers = {
		'Authorization': f"Bearer {user_token}"
	}

	resp = list_users(client, headers=headers)

	assert resp.status_code == 200
	assert resp.json['status'] == 'success'

