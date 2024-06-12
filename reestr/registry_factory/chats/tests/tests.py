from datetime import timedelta
from uuid import UUID

from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import Chat
from ..serializers import ChatSerializer
from . import payloads
from links.models import Link
from links.serializers import LinkSerializer


capitalized_app_name = "chats".capitalize()


class BaseTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.object1 = Chat.objects.create(
            object_type='object',
            name='Object 1 Name',
            object_code='1',
            data={"data 1": "test data 1",
                  "data 2": "test data 2",
                  "digits": 12},
            project_id=None,
            account_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            object_item="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )
        cls.object2 = Chat.objects.create(
            object_type='object',
            name='Object 2 Name',
            object_code='2',
            data={"data 3": "test data 3",
                  "data 4": "test data 4",
                  "data 2": "test data 1",
                  "digits": 48},
            project_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            account_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            user_id=None,
            object_item="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )
        cls.object3 = Chat.objects.create(
            object_type='different_object',
            name='Object 3 Name',
            object_code='3',
            meta={'flags': 116},
            data={"data 5": "test data 5",
                  "data 6": "test data 6",
                  "data 7": "object"},
            project_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            account_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            user_id=None,
            object_item="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )
        cls.object4 = Chat.objects.create(
            object_type='different_object',
            name='Object 4 Name',
            object_code='4',
            meta={'status': 'inactive', 'flags': 254},
            data={},
            project_id=None,
            account_id=None,
            user_id=None,
            object_item=None
        )
        cls.object5 = Chat.objects.create(
            object_type='different_object',
            name='Object 4 Name',
            object_code='5',
            meta={'status': 'inactive', 'flags': 254},
            data={'telephone': '+7894561232'},
            project_id=None,
            account_id=None,
            user_id=None,
            object_item=None
        )
        cls.object6 = Chat.objects.create(
            object_type='new_object',
            name='Object 66 Name',
            object_code='66',
            data={"some_new_field": "some_new_data"},
            project_id="3fa85f64-5717-4562-b3fc-2c963f66afa1",
            account_id="3fa85f64-5717-4562-b3fc-2c963f66afa2",
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa3",
            object_item="3fa85f64-5717-4562-b3fc-2c963f66afa4"
        )
        cls.link1 = Link.objects.create(
            link_type='O2O',
            object1=cls.object1.id,
            object2=cls.object2.id,
            weight=0.5,
            direction=1,
            data={"additional": "data"},
            project_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            account_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )
        cls.link2 = Link.objects.create(
            link_type='O2O',
            object1=cls.object1.id,
            object2=cls.object3.id,
            weight=0,
            direction=0,
            data={},
            project_id=None,
            account_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )
        cls.link3 = Link.objects.create(
            link_type='O2O',
            object1=cls.object1.id,
            object2=cls.object4.id,
            weight=0.8,
            direction=2,
            meta={"flags": 254},
            data={},
            project_id=None,
            account_id=None,
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )
        cls.link4 = Link.objects.create(
            link_type='O2O',
            object1=cls.object2.id,
            object2=cls.object1.id,
            weight=1,
            direction=2,
            data={"additional": "data 2"},
            project_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            account_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )
        cls.link5 = Link.objects.create(
            link_type='defaults_O2O',
            object1=cls.object4.id,
            object2=cls.object3.id,
            meta={"status": "inactive"},
            project_id=None,
            account_id=None,
            user_id=None
        )
        cls.link6 = Link.objects.create(
            link_type='some_new_type',
            object1=cls.object5.id,
            object2=cls.object6.id,
            data={"some_field": "some_data"},
            project_id="3fa85f64-5717-4562-b3fc-2c963f66afa1",
            account_id="3fa85f64-5717-4562-b3fc-2c963f66afa2",
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa3"
        )


class GetAllObjectsTest(BaseTestCase):
    """
    Test module for GET all objects API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_get_all_objects(self):
        url = reverse("chats-list")
        response = self.client.get(url)
        objects = Chat.objects.all()
        serializer = ChatSerializer(objects, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_objects_by_ids(self):
        id_str = ','.join([str(self.object1.id), str(self.object2.id)])
        url = f"/api/chats/?id={id_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_get_objects_by_object_type(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'object_type': 'object'})
        self.assertEqual(len(response.data), 2)

    def test_get_objects_by_object_types(self):
        obj_types_str = ','.join([str(self.object1.object_type), str(self.object3.object_type)])
        url = f"/api/chats/?object_type={obj_types_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 5)

    def test_get_objects_by_name(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'name': 'Object 2 Name'})
        self.assertEqual(len(response.data), 1)

    def test_get_objects_by_names(self):
        names_str = ','.join([str(self.object1.name), str(self.object2.name)])
        url = f"/api/chats/?name={names_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_get_objects_by_object_code(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'object_code': '1'})
        self.assertEqual(len(response.data), 1)

    def test_get_objects_by_object_codes(self):
        obj_codes_str = ','.join([str(self.object1.object_code), str(self.object2.object_code)])
        url = f"/api/chats/?object_code={obj_codes_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_get_objects_by_project_id(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'project_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'})
        self.assertEqual(len(response.data), 2)

    def test_get_objects_by_project_ids(self):
        project_ids_str = ','.join([str(self.object2.project_id), str(self.object6.project_id)])
        url = f"/api/chats/?project_id={project_ids_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)

    def test_get_objects_by_account_id(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'account_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'})
        self.assertEqual(len(response.data), 3)

    def test_get_objects_by_account_ids(self):
        account_ids_str = ','.join([str(self.object1.account_id), str(self.object6.account_id)])
        url = f"/api/chats/?account_id={account_ids_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 4)

    def test_get_objects_by_user_id(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'})
        self.assertEqual(len(response.data), 1)

    def test_get_objects_by_user_ids(self):
        user_ids_str = ','.join([str(self.object1.user_id), str(self.object6.user_id)])
        url = f"/api/chats/?user_id={user_ids_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_get_objects_by_object_item(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'object_item': '3fa85f64-5717-4562-b3fc-2c963f66afa6'})
        self.assertEqual(len(response.data), 3)

    def test_get_objects_by_object_items(self):
        object_items_str = ','.join([str(self.object1.object_item), str(self.object6.object_item)])
        url = f"/api/chats/?object_item={object_items_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 4)

    def test_get_objects_by_created_date(self):
        url = reverse("chats-list")
        date = timezone.now().date()
        response = self.client.get(url, {'created_date': date})
        self.assertEqual(len(response.data), 6)

    def test_get_objects_by_created_date__gt(self):
        url = reverse("chats-list")
        date = timezone.now().date()
        response = self.client.get(url, {'created_date__gt': date})
        self.assertEqual(len(response.data), 0)
        past_date = timezone.now().date() - timedelta(days=1)
        response = self.client.get(url, {'created_date__gt': past_date})
        self.assertEqual(len(response.data), 6)

    def test_get_objects_by_created_date__lt(self):
        url = reverse("chats-list")
        date = timezone.now().date()
        response = self.client.get(url, {'created_date__lt': date})
        self.assertEqual(len(response.data), 0)
        future_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(url, {'created__date_lt': future_date})
        self.assertEqual(len(response.data), 6)

    def test_get_objects_by_modified_date(self):
        url = reverse("chats-list")
        date = timezone.now().date()
        response = self.client.get(url, {'modified_date': date})
        self.assertEqual(len(response.data), 6)

    def test_get_objects_by_modified_date_gt(self):
        url = reverse("chats-list")
        date = timezone.now().date()
        response = self.client.get(url, {'modified_date__gt': date})
        self.assertEqual(len(response.data), 0)
        past_date = timezone.now().date() - timedelta(days=1)
        response = self.client.get(url, {'modified_date__gt': past_date})
        self.assertEqual(len(response.data), 6)

    def test_get_objects_by_modified_date_lt(self):
        url = reverse("chats-list")
        date = timezone.now().date()
        response = self.client.get(url, {'modified_date__lt': date})
        self.assertEqual(len(response.data), 0)
        future_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(url, {'modified_date__lt': future_date})
        self.assertEqual(len(response.data), 6)

    def test_get_objects_by_meta_status(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'meta_status': 'active'})
        self.assertEqual(len(response.data), 4)

    def test_get_objects_by_meta_flags(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'meta_flags': 254})
        self.assertEqual(len(response.data), 2)

    def test_get_objects_by_meta_flags__gt(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'meta_flags__gt': 0})
        self.assertEqual(len(response.data), 3)

    def test_get_objects_by_meta_flags__lt(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'meta_flags__lt': 116})
        self.assertEqual(len(response.data), 3)

    def test_get_objects_by_meta_internal_id(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'meta_internal_id': 3})
        self.assertEqual(len(response.data), 1)

    def test_get_objects_by_meta_internal_ids(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'meta_internal_id': '3,4,5'})
        self.assertEqual(len(response.data), 3)

    def test_get_objects_by_meta_internal_id__gt(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'meta_internal_id__gt': 3})
        self.assertEqual(len(response.data), 3)

    def test_get_objects_by_meta_internal_id__lt(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'meta_internal_id__lt': 2})
        self.assertEqual(len(response.data), 1)

    def test_get_objects_by_data(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'data': 'data 2__exact=test data 2'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'data 2__iexact=Test data 2'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'digits__gte=12::int'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'digits__gt=12::int'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'digits__gt=12.0::float'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'digits__lte=48::int'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'digits__lt=48::int'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'data 2__icontains=data'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'data 2__startswith=test'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'data 2__istartswith=teSt'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'data 2__endswith=2::str'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'data 2__iendswith=2::str'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'data 2=test data 2'})
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'telephone__exact=+7894561232'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'telephone__icontains=789::int'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'telephone__icontains=abc::int'})
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/chats/?data=data 2__icontains=test data&'
                                   'data=data 1__exact=test data 1')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/chats/?data=data 1__exact=test data 1&'
                                   'data=data 2__icontains=test data')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_objects_by_search_all_fields(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'search': '2'})
        self.assertEqual(len(response.data), 6)

    def test_get_object_by_search_data_field(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'search': '2', 'field': 'data'})
        self.assertEqual(len(response.data), 3)

    def test_get_object_by_search_meta_status_field(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'search': 'inactive', 'field': 'meta__status'})
        self.assertEqual(len(response.data), 2)

    def test_get_object_by_search_meta_flags_field(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'search': 254, 'field': 'meta__flags'})
        self.assertEqual(len(response.data), 2)

    def test_get_object_by_search_multiple_fields(self):
        url = ("/api/chats/?search=1&field=name&field=data")
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)

    def test_get_objects_by_multiple_parameters(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'project_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                                         'object_item': '3fa85f64-5717-4562-b3fc-2c963f66afa6'})
        self.assertEqual(len(response.data), 2)

    def test_get_objects_by_invalid_parameters(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'name': 123})
        self.assertEqual(len(response.data), 0)

    def test_objects_asc_ordering(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'ordering': 'object_code'})
        self.assertEqual(response.data[0]['object_code'], '1')
        self.assertEqual(response.data[1]['object_code'], '2')
        self.assertEqual(response.data[2]['object_code'], '3')
        self.assertEqual(response.data[3]['object_code'], '4')
        self.assertEqual(response.data[4]['object_code'], '5')
        self.assertEqual(response.data[5]['object_code'], '66')

    def test_objects_desc_ordering(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'ordering': '-object_code'})
        self.assertEqual(response.data[0]['object_code'], '66')
        self.assertEqual(response.data[1]['object_code'], '5')
        self.assertEqual(response.data[2]['object_code'], '4')
        self.assertEqual(response.data[3]['object_code'], '3')
        self.assertEqual(response.data[4]['object_code'], '2')
        self.assertEqual(response.data[5]['object_code'], '1')

    def test_objects_data_asc_ordering(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'ordering': 'data__data 2'})
        self.assertEqual(response.data[0]['object_code'], '2')
        self.assertEqual(response.data[1]['object_code'], '1')

    def test_objects_data_desc_ordering(self):
        url = reverse("chats-list")
        response = self.client.get(url, {'ordering': '-data__data 2'})
        self.assertEqual(response.data[4]['object_code'], '1')
        self.assertEqual(response.data[5]['object_code'], '2')


class GetAllLinksTest(BaseTestCase):
    """
    Test module for GET all links API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_get_all_links(self):
        url = reverse("links-list")
        response = self.client.get(url)
        objects = Link.objects.all()
        serializer = LinkSerializer(objects, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_links_by_ids(self):
        id_str = ','.join([str(self.link1.id), str(self.link2.id)])
        url = f"/api/links/?id={id_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_get_links_by_link_type(self):
        url = reverse("links-list")
        response = self.client.get(url, {'link_type': 'O2O'})
        self.assertEqual(len(response.data), 4)

    def test_get_links_by_link_types(self):
        link_types_str = ','.join([str(self.link1.link_type), str(self.link5.link_type)])
        url = f"/api/links/?link_type={link_types_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 5)

    def test_get_links_by_object1(self):
        url = reverse("links-list")
        response = self.client.get(url, {'object1': self.object1.id})
        self.assertEqual(len(response.data), 3)

    def test_get_links_by_multiple_object1(self):
        object1_str = ','.join([str(self.object1.id), str(self.object2.id)])
        url = f"/api/links/?object1={object1_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 4)

    def test_get_links_by_object2(self):
        url = reverse("links-list")
        response = self.client.get(url, {'object2': self.object3.id})
        self.assertEqual(len(response.data), 2)

    def test_get_links_by_weight(self):
        url = reverse("links-list")
        response = self.client.get(url, {'weight': 0.5})
        self.assertEqual(len(response.data), 1)

    def test_get_links_by_weight__gt(self):
        url = reverse("links-list")
        response = self.client.get(url, {'weight__gt': 0.5})
        self.assertEqual(len(response.data), 2)

    def test_get_links_by_weight__lt(self):
        url = reverse("links-list")
        response = self.client.get(url, {'weight__lt': 0.5})
        self.assertEqual(len(response.data), 3)

    def test_get_links_by_direction(self):
        url = reverse("links-list")
        response = self.client.get(url, {'direction': 1})
        self.assertEqual(len(response.data), 3)

    def test_get_links_by_direction__gt(self):
        url = reverse("links-list")
        response = self.client.get(url, {'direction__gt': 1})
        self.assertEqual(len(response.data), 2)

    def test_get_links_by_direction__lt(self):
        url = reverse("links-list")
        response = self.client.get(url, {'direction__lt': 1})
        self.assertEqual(len(response.data), 1)

    def test_get_links_by_created_date(self):
        url = reverse("links-list")
        date = timezone.now().date()
        response = self.client.get(url, {'created_date': date})
        self.assertEqual(len(response.data), 6)

    def test_get_links_by_created_date__gt(self):
        url = reverse("links-list")
        date = timezone.now().date()
        response = self.client.get(url, {'created_date__gt': date})
        self.assertEqual(len(response.data), 0)
        past_date = timezone.now().date() - timedelta(days=1)
        response = self.client.get(url, {'created_date__gt': past_date})
        self.assertEqual(len(response.data), 6)

    def test_get_links_by_created_date__lt(self):
        url = reverse("links-list")
        date = timezone.now().date()
        response = self.client.get(url, {'created_date__lt': date})
        self.assertEqual(len(response.data), 0)
        future_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(url, {'created_date__lt': future_date})
        self.assertEqual(len(response.data), 6)

    def test_get_links_by_modified_date(self):
        url = reverse("links-list")
        date = timezone.now().date()
        response = self.client.get(url, {'modified_date': date})
        self.assertEqual(len(response.data), 6)

    def test_get_links_by_modified_date__gt(self):
        url = reverse("links-list")
        date = timezone.now().date()
        response = self.client.get(url, {'modified_date__gt': date})
        self.assertEqual(len(response.data), 0)
        past_date = timezone.now().date() - timedelta(days=1)
        response = self.client.get(url, {'modified_date__gt': past_date})
        self.assertEqual(len(response.data), 6)

    def test_get_links_by_modified_date__lt(self):
        url = reverse("links-list")
        date = timezone.now().date()
        response = self.client.get(url, {'modified_date__lt': date})
        self.assertEqual(len(response.data), 0)
        future_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(url, {'modified_date__lt': future_date})
        self.assertEqual(len(response.data), 6)

    def test_get_links_by_project_id(self):
        url = reverse("links-list")
        response = self.client.get(url, {'project_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'})
        self.assertEqual(len(response.data), 2)

    def test_get_links_by_project_ids(self):
        project_ids_str = ','.join([str(self.link1.project_id), str(self.link6.project_id)])
        url = f"/api/links/?project_id={project_ids_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)

    def test_get_links_by_account_id(self):
        url = reverse("links-list")
        response = self.client.get(url, {'account_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'})
        self.assertEqual(len(response.data), 3)

    def test_get_links_by_account_ids(self):
        account_ids_str = ','.join([str(self.link1.account_id), str(self.link6.account_id)])
        url = f"/api/links/?account_id={account_ids_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 4)

    def test_get_links_by_user_id(self):
        url = reverse("links-list")
        response = self.client.get(url, {'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'})
        self.assertEqual(len(response.data), 4)

    def test_get_links_by_user_ids(self):
        user_ids_str = ','.join([str(self.link1.user_id), str(self.link6.user_id)])
        url = f"/api/links/?user_id={user_ids_str}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 5)

    def test_get_links_by_meta_status(self):
        url = reverse("links-list")
        response = self.client.get(url, {'meta_status': 'active'})
        self.assertEqual(len(response.data), 5)

    def test_get_links_by_meta_flags(self):
        url = reverse("links-list")
        response = self.client.get(url, {'meta_flags': 254})
        self.assertEqual(len(response.data), 1)

    def test_get_links_by_meta_flags__gt(self):
        url = reverse("links-list")
        response = self.client.get(url, {'meta_flags__gt': 0})
        self.assertEqual(len(response.data), 1)

    def test_get_links_by_meta_flags__lt(self):
        url = reverse("links-list")
        response = self.client.get(url, {'meta_flags__lt': 254})
        self.assertEqual(len(response.data), 5)

    def test_get_links_by_meta_internal_id(self):
        url = reverse("links-list")
        response = self.client.get(url, {'meta_internal_id': 3})
        self.assertEqual(len(response.data), 1)

    def test_get_links_by_meta_internal_ids(self):
        url = reverse("links-list")
        response = self.client.get(url, {'meta_internal_id': '3,4,5'})
        self.assertEqual(len(response.data), 3)

    def test_get_links_by_meta_internal_id__gt(self):
        url = reverse("links-list")
        response = self.client.get(url, {'meta_internal_id__gt': 3})
        self.assertEqual(len(response.data), 3)

    def test_get_links_by_meta_internal_id__lt(self):
        url = reverse("links-list")
        response = self.client.get(url, {'meta_internal_id__lt': 2})
        self.assertEqual(len(response.data), 1)

    def test_get_links_by_data(self):
        url = reverse("links-list")
        response = self.client.get(url, {'data': 'additional__exact=data'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__iexact=dAta'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__gte=data'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__gt=data'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__lte=data 2'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__lt=data 2'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__icontains=data'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__startswith=da'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__istartswith=D'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__endswith=2'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__iendswith=2'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional=data'})
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__icontains=+'})
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__gt=1::int'})
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__gt=1::float'})
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'data': 'additional__gt=abc::float'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_links_by_search_all_fields(self):
        url = reverse("links-list")
        response = self.client.get(url, {'search': '2'})
        self.assertEqual(len(response.data), 6)

    def test_get_links_by_search_data_field(self):
        url = reverse("links-list")
        response = self.client.get(url, {'search': '2', 'field': 'data'})
        self.assertEqual(len(response.data), 1)

    def test_get_links_by_search_multiple_fields(self):
        url = ("/api/links/?search=1&field=weight&field=direction")
        response = self.client.get(url)
        self.assertEqual(len(response.data), 4)

    def test_get_links_by_multiple_parameters(self):
        url = reverse("links-list")
        response = self.client.get(url, {'project_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                                         'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'})
        self.assertEqual(len(response.data), 2)

    def test_get_links_by_invalid_parameters(self):
        url = reverse("links-list")
        response = self.client.get(url, {'weight': 123})
        self.assertEqual(len(response.data), 0)

    def test_links_asc_ordering(self):
        url = reverse("links-list")
        response = self.client.get(url, {'ordering': 'direction'})
        self.assertEqual(response.data[0]['direction'], 0)
        self.assertEqual(response.data[1]['direction'], 1)
        self.assertEqual(response.data[2]['direction'], 1)
        self.assertEqual(response.data[3]['direction'], 1)
        self.assertEqual(response.data[4]['direction'], 2)
        self.assertEqual(response.data[4]['direction'], 2)

    def test_links_desc_ordering(self):
        url = reverse("links-list")
        response = self.client.get(url, {'ordering': '-direction'})
        self.assertEqual(response.data[0]['direction'], 2)
        self.assertEqual(response.data[1]['direction'], 2)
        self.assertEqual(response.data[2]['direction'], 1)
        self.assertEqual(response.data[3]['direction'], 1)
        self.assertEqual(response.data[4]['direction'], 1)
        self.assertEqual(response.data[5]['direction'], 0)

    def test_links_multiple_column_asc_ordering(self):
        url = reverse("links-list")
        response = self.client.get(url, {'ordering': 'direction,weight'})
        self.assertEqual(response.data[0]['direction'], 0)
        self.assertEqual(response.data[0]['weight'], 0.0)
        self.assertEqual(response.data[1]['direction'], 1)
        self.assertEqual(response.data[1]['weight'], 0.0)
        self.assertEqual(response.data[2]['direction'], 1)
        self.assertEqual(response.data[2]['weight'], 0.0)
        self.assertEqual(response.data[3]['direction'], 1)
        self.assertEqual(response.data[3]['weight'], 0.5)
        self.assertEqual(response.data[4]['direction'], 2)
        self.assertEqual(response.data[4]['weight'], 0.8)
        self.assertEqual(response.data[5]['direction'], 2)
        self.assertEqual(response.data[5]['weight'], 1.0)

    def test_links_multiple_column_asc_desc_ordering(self):
        url = reverse("links-list")
        response = self.client.get(url, {'ordering': 'direction,-weight'})
        self.assertEqual(response.data[0]['direction'], 0)
        self.assertEqual(response.data[0]['weight'], 0.0)
        self.assertEqual(response.data[1]['direction'], 1)
        self.assertEqual(response.data[1]['weight'], 0.5)
        self.assertEqual(response.data[2]['direction'], 1)
        self.assertEqual(response.data[2]['weight'], 0.0)
        self.assertEqual(response.data[3]['direction'], 1)
        self.assertEqual(response.data[3]['weight'], 0.0)
        self.assertEqual(response.data[4]['direction'], 2)
        self.assertEqual(response.data[4]['weight'], 1.0)
        self.assertEqual(response.data[5]['direction'], 2)
        self.assertEqual(response.data[5]['weight'], 0.8)


class GetSingleObjectTest(BaseTestCase):
    """
     Test module for GET single object API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_get_valid_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.object1.id})
        response = self.client.get(url)
        obj = Chat.objects.get(id=self.object1.id)
        serializer = ChatSerializer(obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': '12345'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetSingleLinkTest(BaseTestCase):
    """
     Test module for GET single object API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_get_valid_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.link1.id})
        response = self.client.get(url)
        link = Link.objects.get(id=self.link1.id)
        serializer = LinkSerializer(link)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_link(self):
        url = reverse("link-detail", kwargs={'pk': '12345'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateSingleObjectTest(BaseTestCase):
    """
    Test module for POST single object API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_create_valid_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-list")
        data = payloads.single_valid_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 7)
        self.assertEqual(Chat.objects.filter(name='Object 1 Name').count(), 2)

    def test_create_invalid_object_item_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-list")
        data = payloads.single_invalid_object_item_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)

    def test_create_invalid_account_id_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-list")
        data = payloads.single_invalid_account_id_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)

    def test_create_null_code_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-list")
        data = payloads.single_null_object_code_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 7)

    def test_create_non_unique_code_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-list")
        data = payloads.single_non_unique_object_code_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)

    def test_create_valid_object_with_passed_id(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-list")
        data = payloads.single_valid_payload
        data["id"] = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 7)
        self.assertEqual(Chat.objects.filter(name='Object 1 Name').count(), 2)
        obj = Chat.objects.get(id="3fa85f64-5717-4562-b3fc-2c963f66afa6")
        self.assertEqual(obj.object_type, data["object_type"])
        self.assertEqual(obj.name, data["name"])
        self.assertEqual(obj.data, data["data"])
        self.assertEqual(obj.project_id, data["project_id"])
        self.assertEqual(obj.account_id, UUID(data["account_id"]))
        self.assertEqual(obj.user_id, UUID(data["user_id"]))
        self.assertEqual(obj.object_item, UUID(data["object_item"]))


class CreateSingleLinkTest(BaseTestCase):
    """
    Test module for POST single link API.
    """
    def setUp(self):
        self.valid_link_payload = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": 0.5,
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.invalid_type_link_payload = {
            "link_type": "",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": 0.5,
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.invalid_object1_link_payload = {
            "link_type": "O2O",
            "object1": None,
            "object2": self.object2.id,
            "weight": 0.5,
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.invalid_object2_link_payload = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": None,
            "weight": 0.5,
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.single_invalid_weight_link_payload = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": 1.5,
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.single_invalid_negative_weight_link_payload = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": -2.0,
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.single_invalid_non_numeric_weight_link_payload = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": "abc",
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.single_invalid_direction_link_payload = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": 0.5,
            "direction": 4,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.single_invalid_negative_direction_link_payload = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": 0.5,
            "direction": -3,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.single_invalid_non_numeric_direction_link_payload = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": 0.5,
            "direction": "abc",
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

    def test_create_valid_link(self):
        url = reverse("link-list")
        data = self.valid_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 7)
        self.assertEqual(len(Link.objects.filter(object2=self.object2.id)), 2)

    def test_create_invalid_type_link(self):
        url = reverse("link-list")
        data = self.invalid_type_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_invalid_object1_link(self):
        url = reverse("link-list")
        data = self.invalid_object2_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_invalid_object2_link(self):
        url = reverse("link-list")
        data = self.invalid_object1_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_invalid_weight_link(self):
        url = reverse("link-list")
        data = self.single_invalid_weight_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_invalid_negative_weight_link(self):
        url = reverse("link-list")
        data = self.single_invalid_negative_weight_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_invalid_non_numeric_weight_link(self):
        url = reverse("link-list")
        data = self.single_invalid_non_numeric_weight_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_invalid_direction_link(self):
        url = reverse("link-list")
        data = self.single_invalid_direction_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_invalid_negative_direction_link(self):
        url = reverse("link-list")
        data = self.single_invalid_negative_direction_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_invalid_non_numeric_direction_link(self):
        url = reverse("link-list")
        data = self.single_invalid_non_numeric_direction_link_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_valid_link_with_passed_id(self):
        url = reverse("link-list")
        data = self.valid_link_payload
        data["id"] = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 7)
        self.assertEqual(len(Link.objects.filter(object2=self.object2.id)), 2)
        obj = Link.objects.get(id="3fa85f64-5717-4562-b3fc-2c963f66afa6")
        self.assertEqual(obj.link_type, data["link_type"])
        self.assertEqual(obj.object1, data["object1"])
        self.assertEqual(obj.object2, data["object2"])
        self.assertEqual(obj.weight, data["weight"])
        self.assertEqual(obj.direction, data["direction"])
        self.assertEqual(obj.data, data["data"])
        self.assertEqual(obj.project_id, UUID(data["project_id"]))
        self.assertEqual(obj.account_id, UUID(data["account_id"]))
        self.assertEqual(obj.user_id, UUID(data["user_id"]))


class CreateMultipleObjectsTest(APITestCase):
    """
    Test module for POST multiple objects API.
    """
    def setUp(self):
        self.object1 = payloads.object1
        self.object2 = payloads.object2
        self.object3 = payloads.object3
        self.object4 = payloads.object4
        self.object5 = payloads.object5
        self.invalid_object = payloads.single_invalid_account_id_payload

    def test_create_valid_objects(self):
        url = reverse("chats-list")
        data = [self.object1, self.object2, self.object3, self.object4]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 4)

    def test_create_invalid_objects(self):
        url = reverse("chats-list")
        data = [self.object1, self.object2, self.object3, self.object4,
                self.invalid_object]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 0)

    def test_create_non_unique_code_objects(self):
        url = reverse("chats-list")
        data = [self.object1, self.object2, self.object5]
        try:
            with transaction.atomic():
                self.client.post(url, data, format='json')
        except Exception as e:
            print(f"This exception is expected: {e}")

        self.assertEqual(Chat.objects.count(), 0)

    def test_create_valid_objects_with_passed_id(self):
        url = reverse("chats-list")
        data = [self.object1, self.object2, self.object3]
        data[0]["id"] = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        data[1]["id"] = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 3)
        self.assertEqual(Chat.objects.filter(id="3fa85f64-5717-4562-b3fc-2c963f66afa6").count(), 1)
        self.assertEqual(Chat.objects.filter(id="3fa85f64-5717-4562-b3fc-2c963f66afa7").count(), 1)


class CreateMultipleLinksTest(BaseTestCase):
    """
    Test module for POST multiple links API.
    """
    def setUp(self):
        self.link1 = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": 0.5,
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.link2 = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object3.id,
            "weight": 0,
            "direction": 0,
            "data": {},
            "project_id": None,
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.link3 = {
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object4.id,
            "weight": 0.8,
            "direction": 2,
            "meta": {"status": "active", "flags": 254},
            "data": {},
            "project_id": None,
            "account_id": None,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.link4 = {
            "link_type": "O2O",
            "object1": self.object2.id,
            "object2": self.object1.id,
            "weight": 1,
            "direction": 2,
            "data": {"additional": "data 2"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.link5 = {
            "link_type": "O2O",
            "object1": self.object4.id,
            "object2": self.object3.id,
            "project_id": None,
            "account_id": None,
            "user_id": None
        }

        self.invalid_link = {
            "link_type": "",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": 0.5,
            "direction": 1,
            "meta": {"status": "inactive", "flags": 0},
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

    def test_create_valid_links(self):
        url = reverse("links-list")
        data = [self.link1, self.link2, self.link3, self.link4, self.link5]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 11)

    def test_create_invalid_objects(self):
        url = reverse("links-list")
        data = [self.link1, self.link2, self.link3, self.link4, self.link5,
                self.invalid_link]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_create_valid_links_with_passed_id(self):
        url = reverse("links-list")
        data = [self.link1, self.link2, self.link3]
        data[0]["id"] = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        data[1]["id"] = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 9)
        self.assertEqual(Link.objects.filter(id="3fa85f64-5717-4562-b3fc-2c963f66afa6").count(), 1)
        self.assertEqual(Link.objects.filter(id="3fa85f64-5717-4562-b3fc-2c963f66afa7").count(), 1)


class UpdateSingleObjectTest(BaseTestCase):
    """
    Test module for PUT single object API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_valid_update_single_object(self):
        model_name = 'Chat'.lower()
        initial_id = self.object1.id
        initial_created_date = self.object1.created_date
        initial_modified_date = self.object1.modified_date
        url = reverse(f"{model_name}-detail", kwargs={'pk': initial_id})
        data = payloads.valid_single_put
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=initial_id)

        self.assertEqual(obj.object_type, "different object")
        self.assertEqual(obj.name, "Object 1 Other Name")
        self.assertEqual(obj.object_code, "6")
        self.assertEqual(obj.created_date, initial_created_date)
        self.assertGreater(obj.modified_date, initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active",
                                    "flags": 0,
                                    "internal_id": 1})
        self.assertEqual(obj.data, {"data 7": "test data 7",
                                    "data 8": "test data 8"})
        self.assertEqual(obj.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.account_id, None)
        self.assertEqual(obj.user_id, None)
        self.assertEqual(obj.object_item, None)

    def test_invalid_update_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.object2.id})
        data = payloads.invalid_single_put
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)

    def test_valid_update_single_object_with_passed_id(self):
        model_name = 'Chat'.lower()
        initial_id = self.object1.id
        new_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        initial_created_date = self.object1.created_date
        initial_modified_date = self.object1.modified_date
        url = reverse(f"{model_name}-detail", kwargs={'pk': initial_id})
        data = payloads.valid_single_put
        data["id"] = new_id
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 7)

        obj_new = Chat.objects.get(id=new_id)

        self.assertEqual(obj_new.object_type, "different object")
        self.assertEqual(obj_new.name, "Object 1 Other Name")
        self.assertEqual(obj_new.object_code, "6")
        self.assertGreater(obj_new.created_date, initial_created_date)
        self.assertGreater(obj_new.modified_date, initial_modified_date)
        self.assertEqual(obj_new.meta, {"status": "active",
                                    "flags": 0,
                                    "internal_id": 7})
        self.assertEqual(obj_new.data, {"data 7": "test data 7",
                                    "data 8": "test data 8"})
        self.assertEqual(obj_new.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj_new.account_id, None)
        self.assertEqual(obj_new.user_id, None)
        self.assertEqual(obj_new.object_item, None)

        obj_old = Chat.objects.get(id=initial_id)

        self.assertEqual(obj_old.object_type, "object")
        self.assertEqual(obj_old.name, "Object 1 Name")
        self.assertEqual(obj_old.object_code, "1")
        self.assertEqual(obj_old.created_date, initial_created_date)
        self.assertEqual(obj_old.modified_date, initial_modified_date)
        self.assertEqual(obj_old.meta, {"status": "active",
                                    "flags": 0,
                                    "internal_id": 1})
        self.assertEqual(obj_old.data, {"data 1": "test data 1",
                                        "data 2": "test data 2",
                                        "digits": 12})
        self.assertEqual(obj_old.project_id, None)
        self.assertEqual(obj_old.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj_old.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj_old.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))


class UpdateSingleLinkTest(BaseTestCase):
    """
    Test module for PUT single link API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.valid_single_link_put_payload = {
            "link_type": "Object_to_object",
            "object1": self.object3.id,
            "object2": self.object2.id,
            "weight": 0.1,
            "direction": 3,
            "meta": {"flags": 119},
            "data": {"additional_data": "test data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "user_id": None
        }

        self.invalid_single_link_put_payload = {
            "link_type": "",
            "object1": self.object1.id,
            "object2": None,
            "weight": 0.5,
            "meta": {"status": "active", "flags": 119, "internal_id": 1},
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

    def test_valid_update_single_link(self):
        initial_id = self.link1.id
        initial_created_date = self.link1.created_date
        initial_modified_date = self.link1.modified_date
        url = reverse("link-detail", kwargs={'pk': initial_id})
        data = self.valid_single_link_put_payload
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=initial_id)

        self.assertEqual(link.link_type, "Object_to_object")
        self.assertEqual(link.object1, self.object3.id)
        self.assertEqual(link.object2, self.object2.id)
        self.assertEqual(link.weight, 0.1)
        self.assertEqual(link.direction, 3)
        self.assertEqual(link.created_date, initial_created_date)
        self.assertGreater(link.modified_date, initial_modified_date)
        self.assertEqual(link.meta, {"status": "active", "flags": 119, 'internal_id': 1})
        self.assertEqual(link.data, {"additional_data": "test data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link.user_id, None)

    def test_invalid_update_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.link2.id})
        data = self.invalid_single_link_put_payload
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

    def test_valid_update_single_link_with_passed_id(self):
        initial_id = self.link1.id
        new_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        initial_created_date = self.link1.created_date
        initial_modified_date = self.link1.modified_date
        url = reverse("link-detail", kwargs={'pk': initial_id})
        data = self.valid_single_link_put_payload
        data["id"] = new_id
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 7)

        link_new = Link.objects.get(id=new_id)

        self.assertEqual(link_new.link_type, "Object_to_object")
        self.assertEqual(link_new.object1, self.object3.id)
        self.assertEqual(link_new.object2, self.object2.id)
        self.assertEqual(link_new.weight, 0.1)
        self.assertEqual(link_new.direction, 3)
        self.assertGreater(link_new.created_date, initial_created_date)
        self.assertGreater(link_new.modified_date, initial_modified_date)
        self.assertEqual(link_new.meta, {"status": "active", "flags": 119, 'internal_id': 7})
        self.assertEqual(link_new.data, {"additional_data": "test data"})
        self.assertEqual(link_new.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link_new.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link_new.user_id, None)

        link_old = Link.objects.get(id=initial_id)

        self.assertEqual(link_old.link_type, "O2O")
        self.assertEqual(link_old.object1, self.object1.id)
        self.assertEqual(link_old.object2, self.object2.id)
        self.assertEqual(link_old.weight, 0.5)
        self.assertEqual(link_old.direction, 1)
        self.assertEqual(link_old.created_date, initial_created_date)
        self.assertEqual(link_old.modified_date, initial_modified_date)
        self.assertEqual(link_old.meta, {"status": "active", "flags": 0, 'internal_id': 1})
        self.assertEqual(link_old.data, {"additional": "data"})
        self.assertEqual(link_old.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link_old.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link_old.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))


class UpdateMultipleObjectsTest(BaseTestCase):
    """
    Test module for PUT multiple objects API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.obj1_initial_id = self.object1.id
        self.obj1_initial_created_date = self.object1.created_date
        self.obj1_initial_modified_date = self.object1.modified_date
        self.object1_invalid_put = {
            "id": self.obj1_initial_id,
            "object_type": "",
            "name": "Object 1 Other Name",
            "object_code": "10",
            "data": {"data 7": "test data 7",
                     "data 8": "test data 8"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": None,
            "user_id": None,
            "object_item": None
        }

        self.obj2_initial_id = self.object2.id
        self.obj2_initial_created_date = self.object2.created_date
        self.obj2_initial_modified_date = self.object2.modified_date
        self.object2_put = {
            "id": self.obj2_initial_id,
            "object_type": "different object",
            "name": "Object 2 Different Name",
            "object_code": "20",
            "meta": {"status": "active",
                     "flags": 0,
                     "internal_id": None},
            "data": {"data 30": "test data 30",
                     "data 40": "test data 40"},
            "project_id": None,
            "account_id": None,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        }

        self.obj3_initial_id = self.object3.id
        self.obj3_initial_created_date = self.object3.created_date
        self.obj3_initial_modified_date = self.object3.modified_date
        self.object3_put = {
            "id": self.obj3_initial_id,
            "object_type": "object",
            "name": "Object 3 Other Name",
            "object_code": "30",
            "meta": {"status": "inactive",
                     "flags": 254,
                     "internal_id": 48},
            "data": {},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "user_id": None,
            "object_item": None
        }
        self.object3_invalid_put = {
            "id": self.obj3_initial_id,
            "object_type": "object",
            "name": "Object 3 Other Name",
            "object_code": "20",
            "meta": {"status": "inactive",
                     "flags": 254,
                     "internal_id": 3},
            "data": {},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "user_id": None,
            "object_item": None
        }

    def test_valid_update_multiple_objects(self):
        url = reverse("chats-list")
        data = [self.object2_put, self.object3_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "different object")
        self.assertEqual(obj3.object_type, "object")
        self.assertEqual(obj2.name, "Object 2 Different Name")
        self.assertEqual(obj3.name, "Object 3 Other Name")
        self.assertEqual(obj2.object_code, "20")
        self.assertEqual(obj3.object_code, "30")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": None})
        self.assertEqual(obj3.meta, {"status": "inactive", "flags": 254, "internal_id": 48})
        self.assertEqual(obj2.data, {"data 30": "test data 30",
                                     "data 40": "test data 40"})
        self.assertEqual(obj3.data, {})
        self.assertEqual(obj2.project_id, None)
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(obj2.account_id, None)
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(obj2.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(obj3.object_item, None)

    def test_invalid_update_multiple_objects(self):
        url = reverse("chats-list")
        data = [self.object1_invalid_put, self.object2_put, self.object3_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)

        obj1 = Chat.objects.get(id=self.obj1_initial_id)
        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj1.object_type, "object")
        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj1.name, "Object 1 Name")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj1.object_code, "1")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj1.created_date, self.obj1_initial_created_date)
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertEqual(obj1.modified_date, self.obj1_initial_modified_date)
        self.assertEqual(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertEqual(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj1.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj1.data, {"data 1": "test data 1",
                                     "data 2": "test data 2",
                                     "digits": 12})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj1.project_id, None)
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj1.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj1.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj1.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_non_unique_object_code_update_multiple_objects(self):
        url = reverse("chats-list")
        data = [self.object2_put, self.object3_invalid_put]

        try:
            with transaction.atomic():
                self.client.put(url, data, format='json')
        except Exception as e:
            print(f'This exception is exptected: {e}')

        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertEqual(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertEqual(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))


class UpdateMultipleLinksTest(BaseTestCase):
    """
    Test module for PUT multiple links API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.link1_initial_id = self.link1.id
        self.link1_initial_created_date = self.link1.created_date
        self.link1_initial_modified_date = self.link1.modified_date
        self.link1_invalid_put = {
            "id": self.link1_initial_id,
            "link_type": "",
            "object1": self.object1.id,
            "object2": None,
            "weight": 0.5,
            "direction": 1,
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.link2_initial_id = self.link2.id
        self.link2_initial_created_date = self.link2.created_date
        self.link2_initial_modified_date = self.link2.modified_date
        self.link2_put = {
            "id": self.link2_initial_id,
            "link_type": "Object_to_object",
            "object1": self.object3.id,
            "object2": self.object2.id,
            "weight": 0.1,
            "direction": 3,
            "data": {"additional_data": "test data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "user_id": None
        }

        self.link3_initial_id = self.link3.id
        self.link3_initial_created_date = self.link3.created_date
        self.link3_initial_modified_date = self.link3.modified_date
        self.link3_put = {
            "id": self.link3_initial_id,
            "link_type": "Object_to_object",
            "object1": self.object4.id,
            "object2": self.object2.id,
            "weight": 0.0,
            "direction": 0,
            "meta": {"status": "active", "flags": 119, "internal_id": 48},
            "data": {},
            "project_id": None,
            "account_id": None,
            "user_id": None
        }

    def test_valid_update_multiple_links(self):
        url = reverse("links-list")
        data = [self.link2_put, self.link3_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link2 = Link.objects.get(id=self.link2_initial_id)
        link3 = Link.objects.get(id=self.link3_initial_id)

        self.assertEqual(link2.link_type, "Object_to_object")
        self.assertEqual(link3.link_type, "Object_to_object")
        self.assertEqual(link2.object1, self.object3.id)
        self.assertEqual(link3.object1, self.object4.id)
        self.assertEqual(link2.object2, self.object2.id)
        self.assertEqual(link3.object2, self.object2.id)
        self.assertEqual(link2.created_date, self.link2_initial_created_date)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertGreater(link2.modified_date, self.link2_initial_modified_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertEqual(link2.weight, 0.1)
        self.assertEqual(link3.weight, 0.0)
        self.assertEqual(link2.direction, 3)
        self.assertEqual(link3.direction, 0)
        self.assertEqual(link2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(link3.meta, {"status": "active", "flags": 119, "internal_id": 48})
        self.assertEqual(link2.data, {"additional_data": "test data"})
        self.assertEqual(link3.data, {})
        self.assertEqual(link2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link2.user_id, None)
        self.assertEqual(link3.user_id, None)

    def test_invalid_update_multiple_links(self):
        url = reverse("links-list")
        data = [self.link1_invalid_put, self.link2_put, self.link3_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

        link1 = Link.objects.get(id=self.link1_initial_id)
        link2 = Link.objects.get(id=self.link2_initial_id)
        link3 = Link.objects.get(id=self.link3_initial_id)

        self.assertEqual(link1.link_type, "O2O")
        self.assertEqual(link2.link_type, "O2O")
        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link1.object1, self.object1.id)
        self.assertEqual(link2.object1, self.object1.id)
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link1.object2, self.object2.id)
        self.assertEqual(link2.object2, self.object3.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link1.weight, 0.5)
        self.assertEqual(link2.weight, 0)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link1.direction, 1)
        self.assertEqual(link2.direction, 0)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link1.created_date, self.link1_initial_created_date)
        self.assertEqual(link2.created_date, self.link2_initial_created_date)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link1.modified_date, self.link1_initial_modified_date)
        self.assertEqual(link2.modified_date, self.link2_initial_modified_date)
        self.assertEqual(link3.modified_date, self.link3_initial_modified_date)
        self.assertEqual(link1.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link1.data, {"additional": "data"})
        self.assertEqual(link2.data, {})
        self.assertEqual(link3.data, {})
        self.assertEqual(link1.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link2.project_id, None)
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link1.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link1.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link2.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))


class PatchSingleObjectTest(BaseTestCase):
    """
    Test module for PATCH single object API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.initial_id = self.object1.id
        self.initial_created_date = self.object1.created_date
        self.initial_modified_date = self.object1.modified_date

    def test_object_type_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"object_type": "different object"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(obj.object_type, "different object")
        self.assertEqual(obj.name, "Object 1 Name")
        self.assertEqual(obj.object_code, "1")
        self.assertEqual(obj.created_date, self.initial_created_date)
        self.assertGreater(obj.modified_date, self.initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj.data, {"data 1": "test data 1",
                                    "data 2": "test data 2",
                                    "digits": 12})
        self.assertEqual(obj.project_id, None)
        self.assertEqual(obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_name_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"name": "Object 1 Other Name"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(obj.object_type, "object")
        self.assertEqual(obj.name, "Object 1 Other Name")
        self.assertEqual(obj.object_code, "1")
        self.assertEqual(obj.created_date, self.initial_created_date)
        self.assertGreater(obj.modified_date, self.initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj.data, {"data 1": "test data 1",
                                    "data 2": "test data 2",
                                    "digits": 12})
        self.assertEqual(obj.project_id, None)
        self.assertEqual(obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_object_code_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"object_code": "10"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(obj.object_type, "object")
        self.assertEqual(obj.name, "Object 1 Name")
        self.assertEqual(obj.object_code, "10")
        self.assertEqual(obj.created_date, self.initial_created_date)
        self.assertGreater(obj.modified_date, self.initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj.data, {"data 1": "test data 1",
                                    "data 2": "test data 2",
                                    "digits": 12})
        self.assertEqual(obj.project_id, None)
        self.assertEqual(obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_meta_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"meta": {"flags": 254}}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(obj.object_type, "object")
        self.assertEqual(obj.name, "Object 1 Name")
        self.assertEqual(obj.object_code, "1")
        self.assertEqual(obj.created_date, self.initial_created_date)
        self.assertGreater(obj.modified_date, self.initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active", "flags": 254, "internal_id": 1})
        self.assertEqual(obj.data, {"data 1": "test data 1",
                                    "data 2": "test data 2",
                                    "digits": 12})
        self.assertEqual(obj.project_id, None)
        self.assertEqual(obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

        data = {"meta": {"internal_id": 48}}
        response = self.client.patch(url, data, format='json')
        obj = Chat.objects.get(id=self.initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "active", "flags": 254, "internal_id": 48})

    def test_data_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"data": {"data 10": "test data 1", "data 2": "test data 22"}}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(obj.object_type, "object")
        self.assertEqual(obj.name, "Object 1 Name")
        self.assertEqual(obj.object_code, "1")
        self.assertEqual(obj.created_date, self.initial_created_date)
        self.assertGreater(obj.modified_date, self.initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj.data, {"data 1": "test data 1",
                                    "data 10": "test data 1",
                                    "data 2": "test data 22",
                                    "digits": 12})
        self.assertEqual(obj.project_id, None)
        self.assertEqual(obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_project_id_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(obj.object_type, "object")
        self.assertEqual(obj.name, "Object 1 Name")
        self.assertEqual(obj.object_code, "1")
        self.assertEqual(obj.created_date, self.initial_created_date)
        self.assertGreater(obj.modified_date, self.initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj.data, {"data 1": "test data 1",
                                    "data 2": "test data 2",
                                    "digits": 12})
        self.assertEqual(obj.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_account_id_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(obj.object_type, "object")
        self.assertEqual(obj.name, "Object 1 Name")
        self.assertEqual(obj.object_code, "1")
        self.assertEqual(obj.created_date, self.initial_created_date)
        self.assertGreater(obj.modified_date, self.initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj.data, {"data 1": "test data 1",
                                    "data 2": "test data 2",
                                    "digits": 12})
        self.assertEqual(obj.project_id, None)
        self.assertEqual(obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_user_id_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"user_id": None}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(obj.object_type, "object")
        self.assertEqual(obj.name, "Object 1 Name")
        self.assertEqual(obj.object_code, "1")
        self.assertEqual(obj.created_date, self.initial_created_date)
        self.assertGreater(obj.modified_date, self.initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj.data, {"data 1": "test data 1",
                                    "data 2": "test data 2",
                                    "digits": 12})
        self.assertEqual(obj.project_id, None)
        self.assertEqual(obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.user_id, None)
        self.assertEqual(obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_object_item_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa7"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(obj.object_type, "object")
        self.assertEqual(obj.name, "Object 1 Name")
        self.assertEqual(obj.object_code, "1")
        self.assertEqual(obj.created_date, self.initial_created_date)
        self.assertGreater(obj.modified_date, self.initial_modified_date)
        self.assertEqual(obj.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj.data, {"data 1": "test data 1",
                                    "data 2": "test data 2",
                                    "digits": 12})
        self.assertEqual(obj.project_id, None)
        self.assertEqual(obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))

    def test_invalid_patch_single_object(self):
        model_name = 'Chat'.lower()
        initial_id = self.object2.id
        initial_created_date = self.object2.created_date
        initial_modified_date = self.object2.modified_date
        url = reverse(f"{model_name}-detail", kwargs={'pk': initial_id})
        data = {"name": ""}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=initial_id)
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj2.created_date, initial_created_date)
        self.assertEqual(obj2.modified_date, initial_modified_date)

    def test_id_and_object_code_patch_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.initial_id})
        data = {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "object_code": "6"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 7)

        new_obj = Chat.objects.get(id="3fa85f64-5717-4562-b3fc-2c963f66afa6")

        self.assertEqual(new_obj.object_type, "object")
        self.assertEqual(new_obj.name, "Object 1 Name")
        self.assertEqual(new_obj.object_code, "6")
        self.assertGreater(new_obj.created_date, self.initial_created_date)
        self.assertGreater(new_obj.modified_date, self.initial_modified_date)
        self.assertEqual(new_obj.meta, {"status": "active", "flags": 0, "internal_id": 7})
        self.assertEqual(new_obj.data, {"data 1": "test data 1",
                                        "data 2": "test data 2",
                                        "digits": 12})
        self.assertEqual(new_obj.project_id, None)
        self.assertEqual(new_obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(new_obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(new_obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

        old_obj = Chat.objects.get(id=self.initial_id)

        self.assertEqual(old_obj.object_type, "object")
        self.assertEqual(old_obj.name, "Object 1 Name")
        self.assertEqual(old_obj.object_code, "1")
        self.assertEqual(old_obj.created_date, self.initial_created_date)
        self.assertEqual(old_obj.modified_date, self.initial_modified_date)
        self.assertEqual(old_obj.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(old_obj.data, {"data 1": "test data 1",
                                        "data 2": "test data 2",
                                        "digits": 12})
        self.assertEqual(old_obj.project_id, None)
        self.assertEqual(old_obj.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(old_obj.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(old_obj.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))


class PatchSingleLinkTest(BaseTestCase):
    """
    Test module for PATCH single link API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.initial_id = self.link1.id
        self.initial_created_date = self.link1.created_date
        self.initial_modified_date = self.link1.modified_date

    def test_link_type_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"link_type": "Object 2 object"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=self.initial_id)

        self.assertEqual(link.link_type, "Object 2 object")
        self.assertEqual(link.object1, self.object1.id)
        self.assertEqual(link.object2, self.object2.id)
        self.assertEqual(link.weight, 0.5)
        self.assertEqual(link.direction, 1)
        self.assertEqual(link.created_date, self.initial_created_date)
        self.assertGreater(link.modified_date, self.initial_modified_date)
        self.assertEqual(link.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link.data, {"additional": "data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_object1_object2_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"object1": self.object2.id, "object2": self.object3.id}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=self.initial_id)

        self.assertEqual(link.link_type, "O2O")
        self.assertEqual(link.object1, self.object2.id)
        self.assertEqual(link.object2, self.object3.id)
        self.assertEqual(link.weight, 0.5)
        self.assertEqual(link.direction, 1)
        self.assertEqual(link.created_date, self.initial_created_date)
        self.assertGreater(link.modified_date, self.initial_modified_date)
        self.assertEqual(link.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link.data, {"additional": "data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_weight_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"weight": 1.0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=self.initial_id)

        self.assertEqual(link.link_type, "O2O")
        self.assertEqual(link.object1, self.object1.id)
        self.assertEqual(link.object2, self.object2.id)
        self.assertEqual(link.weight, 1.0)
        self.assertEqual(link.direction, 1)
        self.assertEqual(link.created_date, self.initial_created_date)
        self.assertGreater(link.modified_date, self.initial_modified_date)
        self.assertEqual(link.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link.data, {"additional": "data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_direction_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"direction": 0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=self.initial_id)

        self.assertEqual(link.link_type, "O2O")
        self.assertEqual(link.object1, self.object1.id)
        self.assertEqual(link.object2, self.object2.id)
        self.assertEqual(link.weight, 0.5)
        self.assertEqual(link.direction, 0)
        self.assertEqual(link.created_date, self.initial_created_date)
        self.assertGreater(link.modified_date, self.initial_modified_date)
        self.assertEqual(link.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link.data, {"additional": "data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_meta_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"meta": {"status": "inactive"}}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=self.initial_id)

        self.assertEqual(link.link_type, "O2O")
        self.assertEqual(link.object1, self.object1.id)
        self.assertEqual(link.object2, self.object2.id)
        self.assertEqual(link.weight, 0.5)
        self.assertEqual(link.direction, 1)
        self.assertEqual(link.created_date, self.initial_created_date)
        self.assertGreater(link.modified_date, self.initial_modified_date)
        self.assertEqual(link.meta, {"status": "inactive", "flags": 0, "internal_id": 1})
        self.assertEqual(link.data, {"additional": "data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_data_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"data": {"more": "more data"}}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=self.initial_id)

        self.assertEqual(link.link_type, "O2O")
        self.assertEqual(link.object1, self.object1.id)
        self.assertEqual(link.object2, self.object2.id)
        self.assertEqual(link.weight, 0.5)
        self.assertEqual(link.direction, 1)
        self.assertEqual(link.created_date, self.initial_created_date)
        self.assertGreater(link.modified_date, self.initial_modified_date)
        self.assertEqual(link.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link.data, {"additional": "data", "more": "more data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_project_id_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=self.initial_id)

        self.assertEqual(link.link_type, "O2O")
        self.assertEqual(link.object1, self.object1.id)
        self.assertEqual(link.object2, self.object2.id)
        self.assertEqual(link.weight, 0.5)
        self.assertEqual(link.direction, 1)
        self.assertEqual(link.created_date, self.initial_created_date)
        self.assertGreater(link.modified_date, self.initial_modified_date)
        self.assertEqual(link.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link.data, {"additional": "data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_account_id_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=self.initial_id)

        self.assertEqual(link.link_type, "O2O")
        self.assertEqual(link.object1, self.object1.id)
        self.assertEqual(link.object2, self.object2.id)
        self.assertEqual(link.weight, 0.5)
        self.assertEqual(link.direction, 1)
        self.assertEqual(link.created_date, self.initial_created_date)
        self.assertGreater(link.modified_date, self.initial_modified_date)
        self.assertEqual(link.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link.data, {"additional": "data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_user_id_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link = Link.objects.get(id=self.initial_id)

        self.assertEqual(link.link_type, "O2O")
        self.assertEqual(link.object1, self.object1.id)
        self.assertEqual(link.object2, self.object2.id)
        self.assertEqual(link.weight, 0.5)
        self.assertEqual(link.direction, 1)
        self.assertEqual(link.created_date, self.initial_created_date)
        self.assertGreater(link.modified_date, self.initial_modified_date)
        self.assertEqual(link.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link.data, {"additional": "data"})
        self.assertEqual(link.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))

    def test_invalid_patch_single_link(self):
        initial_id = self.link2.id
        initial_created_date = self.link2.created_date
        initial_modified_date = self.link2.modified_date
        url = reverse("link-detail", kwargs={'pk': initial_id})
        data = {"object2": None}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

        link2 = Link.objects.get(id=initial_id)
        self.assertEqual(link2.object2, self.object3.id)
        self.assertEqual(link2.created_date, initial_created_date)
        self.assertEqual(link2.modified_date, initial_modified_date)

    def test_id_patch_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.initial_id})
        data = {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 7)

        link_new = Link.objects.get(id="3fa85f64-5717-4562-b3fc-2c963f66afa6")

        self.assertEqual(link_new.link_type, "O2O")
        self.assertEqual(link_new.object1, self.object1.id)
        self.assertEqual(link_new.object2, self.object2.id)
        self.assertEqual(link_new.weight, 0.5)
        self.assertEqual(link_new.direction, 1)
        self.assertGreater(link_new.created_date, self.initial_created_date)
        self.assertGreater(link_new.modified_date, self.initial_modified_date)
        self.assertEqual(link_new.meta, {"status": "active", "flags": 0, "internal_id": 7})
        self.assertEqual(link_new.data, {"additional": "data"})
        self.assertEqual(link_new.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link_new.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link_new.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

        link_old = Link.objects.get(id=self.initial_id)

        self.assertEqual(link_old.link_type, "O2O")
        self.assertEqual(link_old.object1, self.object1.id)
        self.assertEqual(link_old.object2, self.object2.id)
        self.assertEqual(link_old.weight, 0.5)
        self.assertEqual(link_old.direction, 1)
        self.assertEqual(link_old.created_date, self.initial_created_date)
        self.assertEqual(link_old.modified_date, self.initial_modified_date)
        self.assertEqual(link_old.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(link_old.data, {"additional": "data"})
        self.assertEqual(link_old.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link_old.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link_old.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))


class PatchMultipleObjectsTest(BaseTestCase):
    """
    Test module for PATCH multiple objects API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.obj1_initial_id = self.object1.id
        self.obj2_initial_id = self.object2.id
        self.obj2_initial_created_date = self.object2.created_date
        self.obj2_initial_modified_date = self.object2.modified_date
        self.obj3_initial_id = self.object3.id
        self.obj3_initial_created_date = self.object3.created_date
        self.obj3_initial_modified_date = self.object3.modified_date

    def test_object_type_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "object_type": "different object"},
                {"id": self.obj3_initial_id, "object_type": "object"}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "different object")
        self.assertEqual(obj3.object_type, "object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_name_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "name": "Object 2 Other Name"},
                {"id": self.obj3_initial_id, "name": "Object 3 Other Name"}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Other Name")
        self.assertEqual(obj3.name, "Object 3 Other Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_object_code_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "object_code": "7"},
                {"id": self.obj3_initial_id, "object_code": "8"}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "7")
        self.assertEqual(obj3.object_code, "8")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_meta_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj1_initial_id, "meta": {}},
                {"id": self.obj2_initial_id, "meta": {"flags": 254}},
                {"id": self.obj3_initial_id, "meta": {"status": "inactive", "flags2": 0}}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj1 = Chat.objects.get(id=self.obj1_initial_id)
        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj1.meta, {"status": "active", "flags": 0, "internal_id": 1})
        self.assertEqual(obj2.meta, {"status": "active", "flags": 254, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "inactive", "flags": 116, "flags2": 0, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_data_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "data": {"data 3": "test data 33",
                                                      "data 5": "test data 5"}},
                {"id": self.obj3_initial_id, "data": {}}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 33",
                                     "data 4": "test data 4",
                                     "data 5": "test data 5",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_project_id_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7"},
                {"id": self.obj3_initial_id, "project_id": None}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(obj3.project_id, None)
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_account_id_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7"},
                {"id": self.obj3_initial_id, "account_id": None}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(obj3.account_id, None)
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_user_id_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                {"id": self.obj3_initial_id, "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_object_item_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "object_item": None},
                {"id": self.obj3_initial_id, "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa7"}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertGreater(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertGreater(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, None)
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))

    def test_invalid_patch_single_object(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "name": "Object 2 Other Name"},
                {"id": self.obj3_initial_id, "name": ""}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertEqual(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertEqual(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_non_unique_object_code_patch_multiple_objects(self):
        url = reverse("chats-list")
        data = [{"id": self.obj2_initial_id, "object_code": "5"},
                {"id": self.obj3_initial_id, "object_code": "5"}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.object_type, "object")
        self.assertEqual(obj3.object_type, "different_object")
        self.assertEqual(obj2.name, "Object 2 Name")
        self.assertEqual(obj3.name, "Object 3 Name")
        self.assertEqual(obj2.object_code, "2")
        self.assertEqual(obj3.object_code, "3")
        self.assertEqual(obj2.created_date, self.obj2_initial_created_date)
        self.assertEqual(obj3.created_date, self.obj3_initial_created_date)
        self.assertEqual(obj2.modified_date, self.obj2_initial_modified_date)
        self.assertEqual(obj3.modified_date, self.obj3_initial_modified_date)
        self.assertEqual(obj2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active", "flags": 116, "internal_id": 3})
        self.assertEqual(obj2.data, {"data 2": "test data 1",
                                     "data 3": "test data 3",
                                     "data 4": "test data 4",
                                     "digits": 48})
        self.assertEqual(obj3.data, {"data 5": "test data 5",
                                     "data 6": "test data 6",
                                     "data 7": "object"})
        self.assertEqual(obj2.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj2.user_id, None)
        self.assertEqual(obj3.user_id, None)
        self.assertEqual(obj2.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(obj3.object_item, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))


class PatchMultipleLinksTest(BaseTestCase):
    """
    Test module for PATCH multiple links API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.link2_initial_id = self.link2.id
        self.link3_initial_id = self.link3.id
        self.link3_initial_created_date = self.link3.created_date
        self.link3_initial_modified_date = self.link3.modified_date
        self.link4_initial_id = self.link4.id
        self.link4_initial_created_date = self.link4.created_date
        self.link4_initial_modified_date = self.link4.modified_date

    def test_link_type_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link3_initial_id, "link_type": "Object 2 object"},
                {"id": self.link4_initial_id, "link_type": "Object 2 object"}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "Object 2 object")
        self.assertEqual(link4.link_type, "Object 2 object")
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link4.object1, self.object2.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link4.object2, self.object1.id)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link4.weight, 1)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link4.direction, 2)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertGreater(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 0, "internal_id": 4})
        self.assertEqual(link3.data, {})
        self.assertEqual(link4.data, {"additional": "data 2"})
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link4.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_object1_object2_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link3_initial_id, "object1": self.object2.id, "object2": self.object1.id},
                {"id": self.link4_initial_id, "object1": self.object3.id, "object2": self.object4.id}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link4.link_type, "O2O")
        self.assertEqual(link3.object1, self.object2.id)
        self.assertEqual(link4.object1, self.object3.id)
        self.assertEqual(link3.object2, self.object1.id)
        self.assertEqual(link4.object2, self.object4.id)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link4.weight, 1)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link4.direction, 2)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertGreater(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 0, "internal_id": 4})
        self.assertEqual(link3.data, {})
        self.assertEqual(link4.data, {"additional": "data 2"})
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link4.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_weight_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link3_initial_id, "weight": 1},
                {"id": self.link4_initial_id, "weight": 0}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link4.link_type, "O2O")
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link4.object1, self.object2.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link4.object2, self.object1.id)
        self.assertEqual(link3.weight, 1)
        self.assertEqual(link4.weight, 0)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link4.direction, 2)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertGreater(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 0, "internal_id": 4})
        self.assertEqual(link3.data, {})
        self.assertEqual(link4.data, {"additional": "data 2"})
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link4.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_direction_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link3_initial_id, "direction": 0},
                {"id": self.link4_initial_id, "direction": 3}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link4.link_type, "O2O")
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link4.object1, self.object2.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link4.object2, self.object1.id)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link4.weight, 1)
        self.assertEqual(link3.direction, 0)
        self.assertEqual(link4.direction, 3)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertGreater(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 0, "internal_id": 4})
        self.assertEqual(link3.data, {})
        self.assertEqual(link4.data, {"additional": "data 2"})
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link4.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_meta_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link2_initial_id, "meta": {}},
                {"id": self.link3_initial_id, "meta": {"status": "inactive"}},
                {"id": self.link4_initial_id, "meta": {"flags": 254}}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link2 = Link.objects.get(id=self.link2_initial_id)
        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link4.link_type, "O2O")
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link4.object1, self.object2.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link4.object2, self.object1.id)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link4.weight, 1)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link4.direction, 2)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertGreater(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link2.meta, {"status": "active", "flags": 0, "internal_id": 2})
        self.assertEqual(link3.meta, {"status": "inactive", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 254, "internal_id": 4})
        self.assertEqual(link3.data, {})
        self.assertEqual(link4.data, {"additional": "data 2"})
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link4.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_data_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link3_initial_id, "data": {"some": "data"}},
                {"id": self.link4_initial_id, "data": {"additional": "N/A",
                                                       "even more": "data"}}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link4.link_type, "O2O")
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link4.object1, self.object2.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link4.object2, self.object1.id)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link4.weight, 1)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link4.direction, 2)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertGreater(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 0, "internal_id": 4})
        self.assertEqual(link3.data, {"some": "data"})
        self.assertEqual(link4.data, {"additional": "N/A", "even more": "data"})
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link4.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_project_id_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link3_initial_id, "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                {"id": self.link4_initial_id, "project_id": None}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link4.link_type, "O2O")
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link4.object1, self.object2.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link4.object2, self.object1.id)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link4.weight, 1)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link4.direction, 2)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertGreater(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 0, "internal_id": 4})
        self.assertEqual(link3.data, {})
        self.assertEqual(link4.data, {"additional": "data 2"})
        self.assertEqual(link3.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.project_id, None)
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_account_id_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link3_initial_id, "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                {"id": self.link4_initial_id, "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7"}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link4.link_type, "O2O")
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link4.object1, self.object2.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link4.object2, self.object1.id)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link4.weight, 1)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link4.direction, 2)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertGreater(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 0, "internal_id": 4})
        self.assertEqual(link3.data, {})
        self.assertEqual(link4.data, {"additional": "data 2"})
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link4.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))

    def test_user_id_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link3_initial_id, "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7"},
                {"id": self.link4_initial_id, "user_id": None}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link4.link_type, "O2O")
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link4.object1, self.object2.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link4.object2, self.object1.id)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link4.weight, 1)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link4.direction, 2)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertGreater(link3.modified_date, self.link3_initial_modified_date)
        self.assertGreater(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 0, "internal_id": 4})
        self.assertEqual(link3.data, {})
        self.assertEqual(link4.data, {"additional": "data 2"})
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link4.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa7"))
        self.assertEqual(link4.user_id, None)

    def test_invalid_patch_multiple_links(self):
        url = reverse("links-list")
        data = [{"id": self.link3_initial_id, "object1": self.object2.id, "object2": self.object1.id},
                {"id": self.link4_initial_id, "object1": self.object3.id, "object2": None}]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

        link3 = Link.objects.get(id=self.link3_initial_id)
        link4 = Link.objects.get(id=self.link4_initial_id)

        self.assertEqual(link3.link_type, "O2O")
        self.assertEqual(link4.link_type, "O2O")
        self.assertEqual(link3.object1, self.object1.id)
        self.assertEqual(link4.object1, self.object2.id)
        self.assertEqual(link3.object2, self.object4.id)
        self.assertEqual(link4.object2, self.object1.id)
        self.assertEqual(link3.weight, 0.8)
        self.assertEqual(link4.weight, 1)
        self.assertEqual(link3.direction, 2)
        self.assertEqual(link4.direction, 2)
        self.assertEqual(link3.created_date, self.link3_initial_created_date)
        self.assertEqual(link4.created_date, self.link4_initial_created_date)
        self.assertEqual(link3.modified_date, self.link3_initial_modified_date)
        self.assertEqual(link4.modified_date, self.link4_initial_modified_date)
        self.assertEqual(link3.meta, {"status": "active", "flags": 254, "internal_id": 3})
        self.assertEqual(link4.meta, {"status": "active", "flags": 0, "internal_id": 4})
        self.assertEqual(link3.data, {})
        self.assertEqual(link4.data, {"additional": "data 2"})
        self.assertEqual(link3.project_id, None)
        self.assertEqual(link4.project_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.account_id, None)
        self.assertEqual(link4.account_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link3.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))
        self.assertEqual(link4.user_id, UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"))


class DeleteSingleObjectTest(BaseTestCase):
    """
    Test module for DELETE single object API.
    DELETE deactivates an object, but doesn't destroy it.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_valid_delete_single_object(self):
        model_name = 'Chat'.lower()
        initial_id = self.object3.id
        url = reverse(f"{model_name}-detail", kwargs={'pk': initial_id})
        response = self.client.delete(url, format='json')
        obj = Chat.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Chat deactivated')
        self.assertEqual(obj.meta['status'], "inactive")
        self.assertEqual(obj.meta['flags'], 116)
        self.assertEqual(obj.meta['internal_id'], 3)
        self.assertEqual(Chat.objects.count(), 6)

    def test_invalid_delete_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': 123456})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteMultipleObjectsTest(BaseTestCase):
    """
    Test module for DELETE multiple objects API.
    DELETE deactivates objects, but doesn't destroy them.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.obj2_initial_id = self.object2.id
        self.obj3_initial_id = self.object3.id

    def test_valid_delete_multiple_objects(self):
        id_str = ','.join([str(self.object2.id), str(self.object3.id)])
        url = f"/api/chats/?id={id_str}"
        response = self.client.delete(url)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'{capitalized_app_name} deactivated')
        self.assertEqual(obj2.meta['status'], "inactive")
        self.assertEqual(obj3.meta['status'], "inactive")
        self.assertEqual(obj2.meta['flags'], 0)
        self.assertEqual(obj3.meta['flags'], 116)
        self.assertEqual(obj2.meta['internal_id'], 2)
        self.assertEqual(obj3.meta['internal_id'], 3)
        self.assertEqual(Chat.objects.count(), 6)

    def test_incomplete_delete_multiple_objects(self):
        id_str = ','.join([str(self.object2.id), str(self.object3.id), '3fa85f64-5717-4562-b3fc-2c963f66afa6'])
        url = f"/api/chats/?id={id_str}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '2 chats deactivated out of 3. '
                                                   'Some ids are either duplicated or not in the database.')


class DeleteSingleLinkTest(BaseTestCase):
    """
    Test module for DELETE single link API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_valid_delete_single_link(self):
        initial_id = self.link3.id
        url = reverse("link-detail", kwargs={'pk': initial_id})
        response = self.client.delete(url, format='json')
        link3 = Link.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Link deactivated')
        self.assertEqual(link3.meta['status'], "inactive")
        self.assertEqual(link3.meta['flags'], 254)
        self.assertEqual(link3.meta['internal_id'], 3)
        self.assertEqual(Link.objects.count(), 6)

    def test_invalid_delete_single_object(self):
        url = reverse("link-detail", kwargs={'pk': 123456})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteMultipleLinksTest(BaseTestCase):
    """
    Test module for DELETE multiple links API.
    DELETE deactivates links, but doesn't destroy them.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.link2_initial_id = self.link2.id
        self.link3_initial_id = self.link3.id

    def test_valid_delete_multiple_links(self):
        id_str = ','.join([str(self.link2.id), str(self.link3.id)])
        url = f"/api/links/?id={id_str}"
        response = self.client.delete(url)

        link2 = Link.objects.get(id=self.link2_initial_id)
        link3 = Link.objects.get(id=self.link3_initial_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Links deactivated')
        self.assertEqual(link2.meta['status'], "inactive")
        self.assertEqual(link3.meta['status'], "inactive")
        self.assertEqual(link2.meta['flags'], 0)
        self.assertEqual(link3.meta['flags'], 254)
        self.assertEqual(link2.meta['internal_id'], 2)
        self.assertEqual(link3.meta['internal_id'], 3)
        self.assertEqual(Link.objects.count(), 6)

    def test_incomplete_delete_multiple_link(self):
        id_str = ','.join([str(self.link2.id), str(self.link3.id), '3fa85f64-5717-4562-b3fc-2c963f66afa6'])
        url = f"/api/links/?id={id_str}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '2 links deactivated out of 3. '
                                                   'Some ids are either duplicated or not in the database.')


class OptionsObjectsTest(BaseTestCase):
    """
    Test module for OPTIONS single and multiple objects API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_options_valid_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': self.object3.id})
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_options_invalid_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-detail", kwargs={'pk': 123456})
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_options_multiple_objects(self):
        url = reverse("chats-list")
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OptionsLinksTest(BaseTestCase):
    """
    Test module for OPTIONS single and multiple links API.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_options_valid_single_link(self):
        url = reverse("link-detail", kwargs={'pk': self.link3.id})
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_options_invalid_single_link(self):
        url = reverse("link-detail", kwargs={'pk': 123456})
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_options_multiple_links(self):
        url = reverse("links-list")
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MetaFieldCreateSingleTest(BaseTestCase):
    """
    Test module for meta field for single object and
    link creation.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_meta_create_single_object(self):
        model_name = 'Chat'.lower()
        url = reverse(f"{model_name}-list")
        data = payloads.single_valid_payload
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 7})
        self.assertEqual(Chat.objects.filter(name='Object 1 Name').count(), 2)
        data = payloads.meta_payload_1
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 8})
        self.assertEqual(Chat.objects.filter(name='Object 1 Name').count(), 3)
        data = payloads.meta_payload_2
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'inactive', 'flags': 0, 'internal_id': 9})
        self.assertEqual(Chat.objects.filter(name='Object 1 Name').count(), 4)
        data = payloads.meta_payload_3
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 116, 'internal_id': 10})
        self.assertEqual(Chat.objects.filter(name='Object 1 Name').count(), 5)
        data = payloads.meta_payload_4
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 11})
        self.assertEqual(Chat.objects.filter(name='Object 1 Name').count(), 6)
        data = payloads.single_null_object_code_payload
        self.client.post(url, data, format='json')
        self.assertEqual(Chat.objects.filter(name='Object 1 Name').count(), 7)
        data = payloads.meta_payload_5
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 13})
        self.assertEqual(Chat.objects.filter(name='Object 1 Name').count(), 8)

    def test_meta_create_single_link(self):
        url = reverse("link-list")
        data = payloads.link_meta_payload_1
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 7})
        self.assertEqual(Link.objects.all().count(), 7)
        data = payloads.link_meta_payload_2
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 8})
        self.assertEqual(Link.objects.all().count(), 8)
        data = payloads.link_meta_payload_3
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'inactive', 'flags': 0, 'internal_id': 9})
        self.assertEqual(Link.objects.all().count(), 9)
        data = payloads.link_meta_payload_4
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 116, 'internal_id': 10})
        self.assertEqual(Link.objects.all().count(), 10)
        data = payloads.link_meta_payload_5
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 11})
        self.assertEqual(Link.objects.all().count(), 11)
        data = payloads.link_invalid_meta_payload
        self.client.post(url, data, format='json')
        self.assertEqual(Link.objects.all().count(), 11)
        data = payloads.link_meta_payload_1
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 12})
        self.assertEqual(Link.objects.all().count(), 12)


class MetaFieldCreateMultipleTest(BaseTestCase):
    """
    Test module for meta field for multiple objects and
    links creation.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.object1 = payloads.single_valid_payload
        self.object2 = payloads.meta_payload_1
        self.object3 = payloads.meta_payload_2
        self.object4 = payloads.meta_payload_3
        self.object5 = payloads.meta_payload_4
        self.object6 = payloads.meta_payload_5
        self.object7 = payloads.meta_payload_6
        self.object8 = payloads.meta_payload_7
        self.link1 = payloads.link_meta_payload_1
        self.link2 = payloads.link_meta_payload_2
        self.link3 = payloads.link_meta_payload_3
        self.link4 = payloads.link_meta_payload_4
        self.link5 = payloads.link_meta_payload_5
        self.link6 = payloads.link_invalid_meta_payload

    def test_meta_create_multiple_objects(self):
        url = reverse("chats-list")
        data = [self.object1, self.object2]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 8)
        self.assertEqual(response.data[0]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 7})
        self.assertEqual(response.data[1]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 8})
        data = [self.object3, self.object4, self.object5]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 11)
        self.assertEqual(response.data[0]['meta'],
                         {'status': 'inactive', 'flags': 0, 'internal_id': 9})
        self.assertEqual(response.data[1]['meta'],
                         {'status': 'active', 'flags': 116, 'internal_id': 10})
        self.assertEqual(response.data[2]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 11})
        data = [self.object6, self.object1]
        self.client.post(url, data, format='json')
        self.assertEqual(Chat.objects.count(), 11)
        data = [self.object7, self.object8]
        response = self.client.post(url, data, format='json')
        self.assertEqual(Chat.objects.count(), 13)
        self.assertEqual(response.data[0]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 12})
        self.assertEqual(response.data[1]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 13})

    def test_meta_create_multiple_links(self):
        url = reverse("links-list")
        data = [self.link1, self.link2]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 8)
        self.assertEqual(response.data[0]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 7})
        self.assertEqual(response.data[1]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 8})
        data = [self.link3, self.link4, self.link5]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 11)
        self.assertEqual(response.data[0]['meta'],
                         {'status': 'inactive', 'flags': 0, 'internal_id': 9})
        self.assertEqual(response.data[1]['meta'],
                         {'status': 'active', 'flags': 116, 'internal_id': 10})
        self.assertEqual(response.data[2]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 11})
        data = [self.link1, self.link6]
        self.client.post(url, data, format='json')
        self.assertEqual(Link.objects.count(), 11)
        data = [self.link1, self.link2]
        response = self.client.post(url, data, format='json')
        self.assertEqual(Link.objects.count(), 13)
        self.assertEqual(response.data[0]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 12})
        self.assertEqual(response.data[1]['meta'],
                         {'status': 'active', 'flags': 0, 'internal_id': 13})


class MetaFieldPutSingleTest(BaseTestCase):
    """
    Test module for meta field for single object and
    link put.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_meta_put_single_object(self):
        model_name = 'Chat'.lower()
        initial_id = self.object1.id
        url = reverse(f"{model_name}-detail", kwargs={'pk': initial_id})
        data = payloads.meta_put_payload_1
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Chat.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "active",
                                    "flags": 0,
                                    "internal_id": 1})
        data = payloads.meta_put_payload_2
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Chat.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "active",
                                    "flags": 0,
                                    "internal_id": 1})
        data = payloads.meta_put_payload_3
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Chat.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "inactive",
                                    "flags": 0,
                                    "internal_id": 1})
        data = payloads.meta_put_payload_4
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Chat.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "inactive",
                                    "flags": 116,
                                    "internal_id": 1})
        data = payloads.meta_put_payload_5
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Chat.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "inactive",
                                    "flags": 116,
                                    "internal_id": 48})
        data = payloads.invalid_single_put
        response = self.client.put(url, data, format='json')
        obj = Chat.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "inactive",
                                    "flags": 116,
                                    "internal_id": 48})
        data = payloads.meta_put_payload_6
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Chat.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "active",
                                    "flags": 0,
                                    "internal_id": 1})

    def test_meta_put_single_link(self):
        initial_id = self.link1.id
        url = reverse("link-detail", kwargs={'pk': initial_id})
        data = payloads.meta_link_put_payload_1
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Link.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "active",
                                    "flags": 0,
                                    "internal_id": 1})
        data = payloads.meta_link_put_payload_2
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Link.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "active",
                                    "flags": 0,
                                    "internal_id": 1})
        data = payloads.meta_link_put_payload_3
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Link.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "inactive",
                                    "flags": 0,
                                    "internal_id": 1})
        data = payloads.meta_link_put_payload_4
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Link.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "inactive",
                                    "flags": 116,
                                    "internal_id": 1})
        data = payloads.meta_link_put_payload_5
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Link.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "inactive",
                                    "flags": 116,
                                    "internal_id": 48})
        data = payloads.meta_link_invalid_put_payload
        response = self.client.put(url, data, format='json')
        obj = Link.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "inactive",
                                    "flags": 116,
                                    "internal_id": 48})
        data = payloads.meta_link_put_payload_6
        data["id"] = initial_id
        response = self.client.put(url, data, format='json')
        obj = Link.objects.get(id=initial_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)
        self.assertEqual(obj.meta, {"status": "active",
                                    "flags": 0,
                                    "internal_id": 1})


class MetaFieldPutMultipleTest(BaseTestCase):
    """
    Test module for meta field for multiple objects and
    links put.
    """
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.obj1_initial_id = self.object1.id
        self.object1_put = {
            "id": self.obj1_initial_id,
            "object_type": "object",
            "name": "Object 1 Name",
            "object_code": "1",
            "meta": {"flags": 116},
            "data": {"data 1": "test data 1",
                     "data 2": "test data 2",
                     "digits": 12},
            "project_id": None,
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.obj2_initial_id = self.object2.id
        self.object2_put = {
            "id": self.obj2_initial_id,
            "object_type": "different object",
            "name": "Object 2 Different Name",
            "object_code": "20",
            "data": {"data 30": "test data 30",
                     "data 40": "test data 40"},
            "project_id": None,
            "account_id": None,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        }

        self.obj3_initial_id = self.object3.id
        self.object3_put = {
            "id": self.obj3_initial_id,
            "object_type": "object",
            "name": "Object 3 Other Name",
            "object_code": "30",
            "meta": {},
            "data": {},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "user_id": None,
            "object_item": None
        }
        self.object3_invalid_put = {
            "id": self.obj3_initial_id,
            "object_type": "object",
            "name": "Object 3 Other Name",
            "object_code": "20",
            "meta": {"status": "inactive",
                     "flags": 254,
                     "internal_id": 3},
            "data": {},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "user_id": None,
            "object_item": None
        }

        self.link1_initial_id = self.link1.id
        self.link1_put = {
            "id": self.link1_initial_id,
            "link_type": "O2O",
            "object1": self.object1.id,
            "object2": self.object2.id,
            "weight": 0.5,
            "direction": 1,
            "meta": {"internal_id": 48},
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
        self.link1_invalid_put = {
            "id": self.link1_initial_id,
            "link_type": "",
            "object1": self.object1.id,
            "object2": None,
            "weight": 0.5,
            "direction": 1,
            "meta": {"internal_id": 1},
            "data": {"additional": "data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        self.link2_initial_id = self.link2.id
        self.link2_put = {
            "id": self.link2_initial_id,
            "link_type": "Object_to_object",
            "object1": self.object3.id,
            "object2": self.object2.id,
            "weight": 0.1,
            "direction": 3,
            "data": {"additional_data": "test data"},
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "user_id": None
        }

        self.link3_initial_id = self.link3.id
        self.link3_put = {
            "id": self.link3_initial_id,
            "link_type": "Object_to_object",
            "object1": self.object4.id,
            "object2": self.object2.id,
            "weight": 0.0,
            "direction": 0,
            "meta": {},
            "data": {},
            "project_id": None,
            "account_id": None,
            "user_id": None
        }

    def test_meta_put_multiple_objects(self):
        url = reverse("chats-list")
        data = [self.object2_put, self.object3_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.meta, {"status": "active",
                                     "flags": 0,
                                     "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active",
                                     "flags": 116,
                                     "internal_id": 3})
        data = [self.object1_put, self.object2_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Chat.objects.count(), 6)

        obj1 = Chat.objects.get(id=self.obj1_initial_id)
        obj2 = Chat.objects.get(id=self.obj2_initial_id)

        self.assertEqual(obj1.meta, {"status": "active",
                                     "flags": 116,
                                     "internal_id": 1})
        self.assertEqual(obj2.meta, {"status": "active",
                                     "flags": 0,
                                     "internal_id": 2})
        data = [self.object2_put, self.object3_invalid_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 6)

        obj2 = Chat.objects.get(id=self.obj2_initial_id)
        obj3 = Chat.objects.get(id=self.obj3_initial_id)

        self.assertEqual(obj2.meta, {"status": "active",
                                     "flags": 0,
                                     "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active",
                                     "flags": 116,
                                     "internal_id": 3})

    def test_meta_put_multiple_links(self):
        url = reverse("links-list")
        data = [self.link2_put, self.link3_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        obj2 = Link.objects.get(id=self.link2_initial_id)
        obj3 = Link.objects.get(id=self.link3_initial_id)

        self.assertEqual(obj2.meta, {"status": "active",
                                     "flags": 0,
                                     "internal_id": 2})
        self.assertEqual(obj3.meta, {"status": "active",
                                     "flags": 254,
                                     "internal_id": 3})
        data = [self.link1_put, self.link2_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 6)

        obj1 = Link.objects.get(id=self.link1_initial_id)
        obj2 = Link.objects.get(id=self.link2_initial_id)

        self.assertEqual(obj1.meta, {"status": "active",
                                     "flags": 0,
                                     "internal_id": 48})
        self.assertEqual(obj2.meta, {"status": "active",
                                     "flags": 0,
                                     "internal_id": 2})
        data = [self.link1_invalid_put, self.link2_put]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 6)

        obj1 = Link.objects.get(id=self.link1_initial_id)
        obj2 = Link.objects.get(id=self.link2_initial_id)

        self.assertEqual(obj1.meta, {"status": "active",
                                     "flags": 0,
                                     "internal_id": 48})
        self.assertEqual(obj2.meta, {"status": "active",
                                     "flags": 0,
                                     "internal_id": 2})
