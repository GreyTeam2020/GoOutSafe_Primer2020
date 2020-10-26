def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password,
        submit=True
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)