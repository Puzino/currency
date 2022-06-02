from currency.models import ContactUsCreate

from django.urls import reverse


def test_contact_us_get_list(api_client):
    response = api_client.get(reverse('api-v1:contact-list'))
    assert response.status_code == 200
    assert response.json()


def test_contact_us_post_empty_data(api_client):
    response = api_client.post(reverse('api-v1:contact-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'name': ['Обязательное поле.'],
        'reply_to': ['Обязательное поле.'],
        'subject': ['Обязательное поле.'],
        'body': ['Обязательное поле.']
    }


def test_contact_us_post_valid_data(api_client):
    payload = {
        'name': 'Example Name',
        'reply_to': 'example@example.com',
        'subject': 'Subject',
        'body': 'Example text',

    }
    response = api_client.post(reverse('api-v1:contact-list'), data=payload)
    assert response.status_code == 201
    assert response.json()


def test_contact_us_patch_valid_data(api_client):
    contact = ContactUsCreate.objects.last()
    payload = {
        'name': 'Conor McGregor',
    }
    response = api_client.patch(reverse('api-v1:contact-detail', args=[contact.id]), data=payload)
    assert response.status_code == 200
    assert response.json()['name'] == 'Conor McGregor'


def test_contact_us_delete(api_client):
    contact = ContactUsCreate.objects.last()
    response = api_client.delete(reverse('api-v1:contact-detail', args=[contact.id]))
    assert response.status_code == 204
    assert response.content == b''
