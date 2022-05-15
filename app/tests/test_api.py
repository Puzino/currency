from currency.models import ContactUsCreate

from django.urls import reverse

from rest_framework.test import APIClient


def test_contact_us_get_list():
    client = APIClient()
    response = client.get(reverse('api-v1:contact-list'))
    assert response.status_code == 200
    assert response.json()


def test_contact_us_post_empty_data():
    client = APIClient()
    response = client.post(reverse('api-v1:contact-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'name': ['Обязательное поле.'],
        'reply_to': ['Обязательное поле.'],
        'subject': ['Обязательное поле.'],
        'body': ['Обязательное поле.']
    }


def test_contact_us_post_valid_data():
    client = APIClient()
    payload = {
        'name': 'Example Name',
        'reply_to': 'example@example.com',
        'subject': 'Subject',
        'body': 'Example text',

    }
    response = client.post(reverse('api-v1:contact-list'), data=payload)
    assert response.status_code == 201
    assert response.json()


def test_contact_us_patch_valid_data():
    client = APIClient()
    contact = ContactUsCreate.objects.last()
    payload = {
        'name': 'Conor McGregor',
    }
    response = client.patch(reverse('api-v1:contact-detail', args=[contact.id]), data=payload)
    assert response.status_code == 200
    assert response.json()['name'] == 'Conor McGregor'


def test_contact_us_delete():
    client = APIClient()
    contact = ContactUsCreate.objects.last()
    response = client.delete(reverse('api-v1:contact-detail', args=[contact.id]))
    assert response.status_code == 204
    assert response.content == b''
