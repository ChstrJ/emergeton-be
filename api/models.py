import uuid 
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

def get_current_timestamp():
    return int(timezone.now().timestamp())

class User(AbstractUser):
    
    USER_TYPE = (
    ('admin', 'Admin'),
    ('resident', 'Resident'),
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE, null=True)
    created_at = models.IntegerField(default=get_current_timestamp)
    updated_at = models.IntegerField(default=get_current_timestamp)

    def __str__(self):
        return f"{self.id} {self.user_type}"

class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admins")
    created_at = models.IntegerField(default=get_current_timestamp)
    updated_at = models.IntegerField(default=get_current_timestamp)

    def __str__(self):
        return f"{self.id}"

class Resident(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="residents")
    address = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    verified = models.BooleanField(default=False, null=True)
    created_at = models.IntegerField(default=get_current_timestamp)
    updated_at = models.IntegerField(default=get_current_timestamp)
    
    def __str__(self):
        return f"{self.id}"

    
    def __str__(self):
        return f"{self.id}"

class Department(models.Model):

    TAGS = (
    ('fire', 'Fire'),
    ('health', 'Health'),
    ('police', 'Police')
    )

    STATUS = (
    ('dispatched', 'Dispatched'),
    ('available', 'Available'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, validators=[EmailValidator()], unique=True)
    contact_number = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=10, choices=STATUS, null=True, default="available")
    tags = models.CharField(max_length=100, choices=TAGS, null=True)
    created_at = models.IntegerField(default=get_current_timestamp)
    updated_at = models.IntegerField(default=get_current_timestamp)
    
    def __str__(self):
        return self.id 

class Alert(models.Model):
    
    ALERT_TYPE = (
    ('fire', 'Fire'),
    ('health', 'Health'),
    ('police', 'Police')
    )

    ALERT_STATUS = (
    ('ongoing', 'Ongoing'),
    ('dismissed', 'Dismissed'),
    ('pending', 'Pending'),
    ('done', 'Done'),
    )

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, null=True, related_name="residents")
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, related_name="admins")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, related_name="departments")
    alert_type = models.CharField(max_length=100, choices=ALERT_TYPE, null=True)
    alert_status = models.CharField(max_length=100, choices=ALERT_STATUS, default="pending", null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    message = models.CharField(max_length=100, null=True)
    created_at = models.IntegerField(default=get_current_timestamp)
    updated_at = models.IntegerField(default=get_current_timestamp)
