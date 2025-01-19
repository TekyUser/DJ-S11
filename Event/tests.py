from django.test import TestCase
from django.contrib.auth.models import User
from .models import Event, UserEvent
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone 

class EventModelTest(TestCase):

    def setUp(self):
        # Tạo 1 user để sử dụng trong các test case
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_create_event_with_valid_data(self):
        # Tạo một event hợp lệ
        event = Event.objects.create(
            name="Test Event 1",
            description="This is a test event description.",
            location="Test Location",
            date=timezone.now(),  # Sử dụng timezone.now()
            is_private=False,
            creator=self.user,
            time="10:00:00",
            final_time="12:00:00"
        )
        # Kiểm tra rằng event được tạo thành công
        self.assertEqual(event.name, "Test Event 1")
        self.assertEqual(event.time, "10:00:00")
        self.assertEqual(event.final_time, "12:00:00")
        self.assertEqual(event.creator, self.user)
        self.assertTrue(event.duration)  # Kiểm tra rằng duration được tính toán

    def test_event_duration_calculation(self):
        # Tạo một event với thời gian bắt đầu và kết thúc hợp lệ
        event = Event.objects.create(
            name="Test Event 2",
            description="Event with duration calculation.",
            location="Location 2",
            date=timezone.now(),  # Sử dụng timezone.now()
            is_private=False,
            creator=self.user,
            time="08:00:00",
            final_time="10:00:00"
        )
        # Kiểm tra duration của event (2 giờ)
        self.assertEqual(event.duration, timedelta(hours=2))

    def test_event_duration_cross_day(self):
        # Tạo một event qua ngày (final_time < start_time)
        event = Event.objects.create(
            name="Test Event 3",
            description="Event that crosses midnight.",
            location="Location 3",
            date=timezone.now(),  # Sử dụng timezone.now()
            is_private=False,
            creator=self.user,
            time="22:00:00",  # 10:00 PM
            final_time="02:00:00"  # 2:00 AM ngày hôm sau
        )
        # Kiểm tra duration (4 giờ)
        self.assertEqual(event.duration, timedelta(hours=4))

    def test_event_invalid_duration(self):
        # Tạo một event mà final_time nhỏ hơn time (sai)
        event = Event(name="Invalid Event", description="Invalid event duration",
                      location="Invalid Location", date=timezone.now(),  # Sử dụng timezone.now()
                      is_private=False, creator=self.user, time="10:00:00",
                      final_time="08:00:00")

        # Kiểm tra xem có raise ValidationError không
        with self.assertRaises(ValidationError):
            event.clean()  # Phương thức clean() kiểm tra dữ liệu hợp lệ

    def test_create_multiple_events(self):
        # Tạo 10 sự kiện với các dữ liệu hợp lệ
        for i in range(10):
            event = Event.objects.create(
                name=f"Test Event {i + 1}",
                description=f"This is the description for event {i + 1}",
                location=f"Test Location {i + 1}",
                date=timezone.now(),  # Sử dụng timezone.now()
                is_private=False,
                creator=self.user,
                time="10:00:00",
                final_time="12:00:00"
            )
            # Kiểm tra mỗi event được tạo ra
            self.assertEqual(event.name, f"Test Event {i + 1}")
            self.assertEqual(event.creator, self.user)

    def test_user_event_association(self):
        # Tạo sự kiện và tham gia sự kiện từ user
        event = Event.objects.create(
            name="Test Event for User",
            description="A test event for user participation.",
            location="Test Location for User",
            date=timezone.now(),  # Sử dụng timezone.now()
            is_private=False,
            creator=self.user,
            time="08:00:00",
            final_time="10:00:00"
        )
        user_event = UserEvent.objects.create(
            user=self.user,
            event=event
        )
        # Kiểm tra UserEvent được tạo thành công
        self.assertEqual(user_event.user, self.user)
        self.assertEqual(user_event.event, event)
        self.assertIsNotNone(user_event.joined_at)
