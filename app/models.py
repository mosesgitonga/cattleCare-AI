from mongoengine import Document, StringField, BooleanField, ListField, ReferenceField, DateTimeField, FloatField, ImageField
from datetime import datetime

# User Model - Tracks users (Farmers, Vets, Admins)
class User(Document):
    full_name = StringField(max_length=100, required=True)
    password = StringField(max_length=100, required=True)
    role = StringField(choices=["farmer", "vet", "admin"], required=True)
    last_login = DateTimeField(default=datetime.utcnow)
    
    meta = {"collection": "users"}

    def clean(self):
        # Ensuring that a role is provided and last_login is correctly set
        if not self.role:
            raise ValueError("Role is required for the user.")
        if not self.last_login:
            self.last_login = datetime.utcnow()

# Farm Model - Represents a farm with basic info
class Farm(Document):
    name = StringField(required=True)
    country = StringField()
    county = StringField()
    longitude = StringField(required=False)
    latitude = StringField(required=False)
    owner = ReferenceField(User, required=True)
    meta = {"collection": "farms"}

    def clean(self):
        if not self.owner:
            raise ValueError("A farm must be associated with a user (owner).")

# Cow Model - Represents a cow with health, milk production, feed, and breeding history
class Cow(Document):
    name = StringField(required=True)
    breed = StringField(required=False)
    maturity = ListField(StringField(choices=['calf', 'mature']), required=True)  # Multiple maturity states
    pregnancy_status = StringField(choices=['not_pregnant', 'pregnant', 'calf_bearing'], required=False)
    age = FloatField(required=False)
    is_pregnant = BooleanField(default=False)
    health_status = StringField(choices=['healthy', 'sick', 'under_observation'])
    notes = StringField(required=False)
    cow_images = ListField(ImageField())  # Images of the cow for identification
    health_reports = ListField(ReferenceField('HealthReport'))  # Reference to health reports (List of reports)
    owner_id = ReferenceField("User", required=False)  # Reference to the user (farmer)
    farm_id = ReferenceField("Farm", required=False)  # Reference to the farm the cow is located at
    last_vaccination = DateTimeField(default=datetime.utcnow)  # Date of the last vaccination
    last_checkup = DateTimeField(default=datetime.utcnow)  # Date of the last checkup
    next_due_checkup = DateTimeField(required=False)  # Date when the next checkup is due
    milk_production = FloatField(default=0.0)  # Amount of milk produced
    weight = FloatField(required=False)  # Weight of the cow
    feed_data = ListField(ReferenceField('Feed'))  # Reference to feed given
    breeding_history = ListField(ReferenceField('Breeding'))  # Reference to breeding history
    milking_history = ListField(ReferenceField('MilkingEvent'))  # Reference to milking events
    
    meta = {"collection": "cows"}

    def clean(self):
        # Validation for necessary fields
        if not self.name or not self.maturity:
            raise ValueError("Cow must have a name and at least one maturity state.")
        if not self.health_status:
            self.health_status = "healthy"
        if not self.last_vaccination:
            self.last_vaccination = datetime.utcnow()
        if not self.last_checkup:
            self.last_checkup = datetime.utcnow()

# Health Report Model - Represents health checkup reports for cows
class HealthReport(Document):
    cow = ReferenceField('Cow', required=True)
    report_details = StringField(required=True)
    report_date = DateTimeField(default=datetime.utcnow)
    recommendation = StringField(required=False)
    
    meta = {"collection": "health_reports"}

    def clean(self):
        if not self.report_details:
            raise ValueError("Report details are required.")
        if not self.report_date:
            self.report_date = datetime.utcnow()

# Milking Event Model - Tracks milking events including quantity and time
class MilkingEvent(Document):
    cow = ReferenceField('Cow', required=True)  # The cow that was milked
    milking_time = DateTimeField(default=datetime.utcnow)  # Timestamp for the milking
    milk_quantity = FloatField(required=True)  # Amount of milk produced (in liters)
    milker = StringField(required=True)  # Person who milked the cow
    milking_method = StringField(choices=["manual", "machine"], required=True)  # Type of milking method
    notes = StringField(required=False)
    farm_id = ReferenceField('Farm', required=True)  
    
    meta = {"collection": "milking_events"}

    def clean(self):
        if not self.milk_quantity or self.milk_quantity <= 0:
            raise ValueError("Milk quantity must be a positive value.")
        if not self.milking_method:
            raise ValueError("Milking method is required.")

# Feed Model - Tracks feed given to cows including type, amount, and feeding time
class Feed(Document):
    cow = ReferenceField('Cow', required=True)
    feed_type = StringField(required=True)
    feed_amount = FloatField(required=True)  # Amount of feed in kilograms
    feeding_time = DateTimeField(default=datetime.utcnow)  
    
    meta = {"collection": "feeds"}

    def clean(self):
        if not self.feed_amount or self.feed_amount <= 0:
            raise ValueError("Feed amount must be a positive value.")

# Breeding Model - Tracks breeding events and partner cows
class Breeding(Document):
    cow = ReferenceField('Cow', required=True)
    breeding_date = DateTimeField(required=True)
    breeding_partner = ReferenceField('Cow')  # The other cow that the cow was bred with
    notes = StringField(required=False)
    
    meta = {"collection": "breeding"}

    def clean(self):
        if not self.breeding_date:
            raise ValueError("Breeding date is required.")
        if not self.breeding_partner:
            raise ValueError("Breeding partner is required.")

# Video Analysis Model - Stores results of video analysis for disease detection and recommendations
class VideoAnalysis(Document):
    cow = ReferenceField('Cow', required=True)
    video_url = StringField(required=True)  # URL of the uploaded video
    analysis_results = StringField(required=True)  # Results of the analysis (e.g., detected diseases)
    recommendation = StringField(required=True)  # Recommendations for cow care
    analysis_time = DateTimeField(default=datetime.utcnow) 
    
    meta = {"collection": "video_analyses"}

    def clean(self):
        if not self.analysis_results:
            raise ValueError("Analysis results are required.")
        if not self.recommendation:
            raise ValueError("Recommendation is required.")
