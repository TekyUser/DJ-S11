from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    is_private = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.TimeField(default="00:00:00")  # start time
    final_time = models.TimeField(null=True, blank=True)  # final time

    @property
    def duration(self):
        if self.time and self.final_time:
            # Chuyển đổi str thành datetime.time
            start_time = datetime.strptime(str(self.time), "%H:%M:%S").time()
            final_time = datetime.strptime(str(self.final_time), "%H:%M:%S").time()

            start_datetime = datetime.combine(datetime.today(), start_time)
            final_datetime = datetime.combine(datetime.today(), final_time)

            # Nếu final_time trước time, có nghĩa là qua ngày hôm sau
            if final_datetime < start_datetime:
                final_datetime += timedelta(days=1)  # cộng thêm 1 ngày

            # Tính độ dài bằng chênh lệch thời gian
            duration = final_datetime - start_datetime
            return duration
        return None

    def clean(self):
        # Kiểm tra rằng final_time phải lớn hơn time
        if self.final_time and self.time >= self.final_time:
            raise ValidationError('Final time must be greater than start time.')
        
    def save(self, *args, **kwargs):
        # Nếu final_time chưa được nhập, tự động gán final_time = time + 1 giờ
        if not self.final_time:
            start_time = datetime.combine(datetime.today(), self.time)
            final_time = start_time + timedelta(seconds=1)  # cộng thêm 1 giờ
            self.final_time = final_time.time()

        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} joined {self.event.name}'
