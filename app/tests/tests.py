def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_contact_us_get(client):
    response = client.get('/currency/contact-us/create/')
    assert response.status_code == 200


def test_contact_us_post_empty_data(client):
    response = client.post('/currency/contact-us/create/')
    assert response.status_code == 200  # when post 200 is error
    assert response.context_data['form'].errors == {
        'name': ['Обязательное поле.'],
        'reply_to': ['Обязательное поле.'],
        'subject': ['Обязательное поле.'],
        'body': ['Обязательное поле.'],
    }


def test_contact_us_post_valid_data(client):
    payload = {
        'name': 'Lionel Messi',
        'reply_to': 'messilionel@example.com',
        'subject': 'Subject',
        'body': 'Example text',
    }
    response = client.post('/currency/contact-us/create/', data=payload)
    assert response.status_code == 302
    assert response.url == '/'


def test_contact_us_post_invalid_email(client):
    payload = {
        'name': 'Lionel Messi',
        'reply_to': 'messilionel',
        'subject': 'Subject',
        'body': 'Example text',
    }
    response = client.post('/currency/contact-us/create/', data=payload)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {'reply_to': ['Введите правильный адрес электронной почты.']}
