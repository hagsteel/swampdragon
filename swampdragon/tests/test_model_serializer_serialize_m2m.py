from django.db import models
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import ParentModel, ChildModel, SDModel


class Address(SDModel):
    name = models.CharField(max_length=100)


class AddressBook(SDModel):
    owner = models.CharField(max_length=100)
    address = models.ManyToManyField(Address)


class AddressBookSerializer(ModelSerializer):
    class Meta:
        model = AddressBook
        publish_fields = ('owner', 'address')


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        publish_fields = ('name', 'addressbook_set')


class ExtendedAddressSerializer(AddressSerializer):
    addressbook_set = AddressBookSerializer


class ExtendedAddressBookSerializer(AddressBookSerializer):
    address = AddressSerializer


class TestModelSerializer(DragonTestCase):
    def test_serialize_m2m(self):
        address = Address.objects.create(name='benedicte')
        address_book = AddressBook.objects.create(owner='veronica')

        address_book.address.add(address)

        ser = ExtendedAddressBookSerializer(instance=address_book)

        data = ser.serialize()
        self.assertEqual(data['address'][0]['name'], address.name)


    def test_serialize_reverse_m2m(self):
        address = Address.objects.create(name='benedicte')
        address_book = AddressBook.objects.create(owner='veronica')
        address_book.address.add(address)

        ser = ExtendedAddressSerializer(instance=address)
        data = ser.serialize()
        self.assertEqual(data['addressbook_set'][0]['owner'], address_book.owner)


    def test_serialize_m2m_without_serializer(self):
        """
        Serialize an m2m relation without a serializer
        should return a list ids
        """
        address_a = Address.objects.create(name='benedicte')
        address_b = Address.objects.create(name='jonas')
        address_book = AddressBook.objects.create(owner='veronica')

        address_book.address.add(address_a)
        address_book.address.add(address_b)

        ser = AddressBookSerializer(instance=address_book)
        data = ser.serialize()
        self.assertListEqual(list(data['address']), [address_a.pk, address_b.pk])

    def test_serialize_reverse_m2m_without_serializer(self):
        """
        Serialize a reverse m2m relation without a serializer
        should return a list ids
        """
        address = Address.objects.create(name='benedicte')
        address_book = AddressBook.objects.create(owner='veronica')
        address_book.address.add(address)

        ser = AddressSerializer(instance=address)
        data = ser.serialize()
        self.assertListEqual(list(data['addressbook_set']), [address_book.pk])
