from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient


class HotelViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.app_user = AppUser.objects.create_user(
            username="hotelowner1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.client.force_authenticate(user=self.app_user)

        self.hotel_owner = HotelOwner.objects.create(user_id=self.app_user.id)
        self.hotel = Hotel.objects.create(
            name="Test Hotel", hotel_owner=self.hotel_owner
        )

    def create_image(self, filename="test_image.jpg"):
        img = Image.new("RGB", (100, 100), color=(255, 0, 0))
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)

        return SimpleUploadedFile(
            filename, img_byte_arr.read(), content_type="image/jpeg"
        )

    def test_list_hotels(self):
        url = reverse("hotel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.hotel.name)

    def test_create_hotel(self):
        url = reverse("hotel-list")
        data = {
            "name": "New Hotel",
            "address": "123 Street",
            "city": "Test City",
            "description": "A nice hotel",
            "hotel_owner": self.hotel_owner.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Hotel.objects.filter(name="New Hotel").exists())

    def test_update_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel.id})
        data = {
            "name": "Updated Hotel",
            "address": "123 Street",
            "city": "Test City",
            "description": "A nice hotel",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, "Updated Hotel")

    def test_partial_update_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel.id})
        data = {"name": "Partially Updated Hotel"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, "Partially Updated Hotel")

    def test_delete_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Hotel.objects.filter(id=self.hotel.id).exists())

    def test_list_room_types_of_hotel(self):
        url = reverse("hotel-list_room_types_of_hotel", kwargs={"pk": self.hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_image(self):
        image = self.create_image()
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        data = {"image": image}
        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.hotel.refresh_from_db()
        self.assertTrue(self.hotel.images.count() == 1)

    def test_update_image(self):
        initial_image = self.create_image("initial_image.jpg")
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        data = {"image": initial_image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.hotel.refresh_from_db()

        initial_image_url = self.hotel.images.first().image

        updated_image = self.create_image("updated_image.jpg")
        data = {"image": updated_image}
        url = reverse(
            "hotel-image-update-image",
            kwargs={"pk": self.hotel.id, "image_id": self.hotel.images.first().id},
        )
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()

        updated_image_url = self.hotel.images.first().image
        self.assertNotEqual(updated_image_url, initial_image_url)
        self.assertTrue(
            updated_image_url.name.split("/")[-1].startswith("updated_image")
        )

    def test_partial_update_image(self):
        initial_image = self.create_image("initial_image.jpg")
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        data = {"image": initial_image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.hotel.refresh_from_db()

        initial_image_url = self.hotel.images.first().image

        updated_image = self.create_image("updated_image.jpg")
        data = {"image": updated_image}
        url = reverse(
            "hotel-image-partial-update-image",
            kwargs={"pk": self.hotel.id, "image_id": self.hotel.images.first().id},
        )
        response = self.client.patch(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()

        updated_image_url = self.hotel.images.first().image
        self.assertNotEqual(updated_image_url, initial_image_url)
        self.assertTrue(
            updated_image_url.name.split("/")[-1].startswith("updated_image")
        )

    def test_delete_image(self):
        image = self.create_image("test_image.jpg")
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        data = {"image": image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.hotel.refresh_from_db()

        delete_url = reverse(
            "hotel-image-delete-image",
            kwargs={"pk": self.hotel.id, "image_id": self.hotel.images.first().id},
        )
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.hotel.refresh_from_db()

        self.assertIsNone(self.hotel.images.first())

    def test_invalid_image_upload(self):
        data = {
            "image": SimpleUploadedFile(
                "test_text.txt", b"Some text data", content_type="text/plain"
            )
        }
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_images(self):
        image = self.create_image("single_image.jpg")
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        data = {"image": image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.hotel.refresh_from_db()

        url = reverse("hotel-image-list_images_of_hotel", kwargs={"pk": self.hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_image(self):
        image = self.create_image("single_image.jpg")
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        data = {"image": image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.hotel.refresh_from_db()

        url = reverse(
            "hotel-image-get-image",
            kwargs={"pk": self.hotel.id, "image_id": self.hotel.images.first().id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.hotel.images.first().id)

    def test_get_cover_image(self):
        cover_image = self.create_image("cover_image.jpg")
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        data = {"image": cover_image, "is_cover": True}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.hotel.refresh_from_db()

        url = reverse("hotel-image-get-cover-image", kwargs={"pk": self.hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("image" in response.data)

    def test_get_non_cover_images(self):
        image1 = self.create_image("image1.jpg")
        image2 = self.create_image("image2.jpg")
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        self.client.post(url, {"image": image1}, format="multipart")
        self.client.post(url, {"image": image2}, format="multipart")
        self.hotel.refresh_from_db()

        url = reverse("hotel-image-get-non-cover-images", kwargs={"pk": self.hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_set_image_as_cover(self):
        image1 = self.create_image("image1.jpg")
        image2 = self.create_image("image2.jpg")
        url = reverse("hotel-image-upload-image", kwargs={"pk": self.hotel.id})
        response1 = self.client.post(url, {"image": image1}, format="multipart")
        response2 = self.client.post(url, {"image": image2}, format="multipart")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        self.hotel.refresh_from_db()

        image2_id = self.hotel.images.last().id
        url = reverse(
            "hotel-image-set-image-as-cover",
            kwargs={"pk": self.hotel.id, "image_id": image2_id},
        )
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()

        cover_image = self.hotel.images.filter(is_cover=True).first()
        self.assertEqual(cover_image.id, image2_id)

    def test_invalid_set_cover_image(self):
        url = reverse(
            "hotel-image-set-image-as-cover",
            kwargs={"pk": self.hotel.id, "image_id": 999},
        )
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_cover_image_no_cover(self):
        url = reverse("hotel-image-get-cover-image", kwargs={"pk": self.hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
