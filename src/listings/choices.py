from django.db import models

class HousingTypeChoices(models.TextChoices):
    APARTMENT = "apartment", "Apartment"
    HOUSE = "house", "House"
    ROOM = "room", "Room"
    VILLA = "villa", "Villa"

class ListingStatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"