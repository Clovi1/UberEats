import mock
from django.core.files import File
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from stores.models import Kitchen, Restaurant, Category
from stores.serializers import KitchenSerializer
from django.contrib.auth.models import User


class KitchenTests(APITestCase):
    def setUp(self):
        self.kitchen = Kitchen.objects.create(title='японская')
        Kitchen.objects.create(title='китайская')
        Kitchen.objects.create(title='американская')

        user = User.objects.create_user(username='admin', email='admin@example.com', password='admin')
        self.token = AccessToken.for_user(user=user)

    def test_kitchen_list(self):
        response = self.client.get(reverse('kitchen-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertTrue({'id': 1, 'title': 'японская'} in response.json())

    def test_kitchen_detail(self):
        response = self.client.get(reverse('kitchen-detail', kwargs={'pk': self.kitchen.pk}))
        serializer_data = KitchenSerializer(self.kitchen).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_kitchen_invalid_create(self):
        response = self.client.post(reverse('kitchen-list'), {'title': 'европейская'})
        self.assertEqual(Kitchen.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_kitchen_valid_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(reverse('kitchen-list'), {'title': 'европейская'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Kitchen.objects.count(), 4)
        self.assertEqual({'id': 4, 'title': 'европейская'}, response.data)

    def test_kitchen_invalid_update(self):
        response = self.client.patch(reverse('kitchen-detail', kwargs={'pk': self.kitchen.pk}), {'title': 'Japanese'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Kitchen.objects.get(pk=self.kitchen.pk).title, 'японская')

    def test_kitchen_valid_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(reverse('kitchen-detail', kwargs={'pk': self.kitchen.pk}), {'title': 'Japanese'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Kitchen.objects.get(pk=self.kitchen.pk).title, 'Japanese')

    def test_kitchen_invalid_delete(self):
        response = self.client.delete(reverse('kitchen-detail', kwargs={'pk': self.kitchen.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Kitchen.objects.count(), 3)

    def test_kitchen_valid_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(reverse('kitchen-detail', kwargs={'pk': self.kitchen.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Kitchen.objects.count(), 2)


class CategoryTests(APITestCase):
    def setUp(self):
        self.image = mock.MagicMock(spec=File)
        self.image.name = 'kfs.jpg'

        self.user = User.objects.create_user(username='admin', email='admin@example.com', password='admin')
        self.user2 = User.objects.create_user(username='user', email='user@example.com', password='user')
        self.token = AccessToken.for_user(user=self.user)

        self.kitchen = Kitchen.objects.create(title='японская')

        self.restaurant = Restaurant.objects.create(
            title='мак',
            time='20-30',
            image=self.image.name,
            owner=self.user,
        )
        self.restaurant.kitchen.add(self.kitchen)
        self.restaurant2 = Restaurant.objects.create(title='кфс', time='20-30', image=self.image.name, owner=self.user2)

        self.category = Category.objects.create(title='закуски', restaurants=self.restaurant)
        Category.objects.create(title='десерты', restaurants=self.restaurant2)

    def test_category_list(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('category-list'), {'restaurants': 1})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail(self):
        response = self.client.get(reverse('category-detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.json()['title'], 'закуски')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_invalid_create(self):
        response = self.client.post(reverse('category-list'))
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TODO: add valid_create, update, delete

# TODO: add restaurant, food
