import pytest
from mongoengine import connect, disconnect
from datetime import datetime
from app.models import User, Farm, Cow, HealthReport, MilkingEvent, Feed, Breeding, VideoAnalysis


@pytest.fixture(scope="module")
def setup():
    disconnect()
    # Connect to a test database
    connect("test_cattleCare_db", host="localhost", port=27017)
    yield  
    disconnect()

def test_user_creation(setup):
    user = User(full_name="John Doe", password="password123", role="farmer")
    user.save()

    # Assert the user is saved correctly
    assert user.full_name == "John Doe"
    assert user.role == "farmer"
    assert user.last_login is not None  # should have a timestamp
    assert user.id is not None  # Check if user _id is assigned

def test_farm_creation(setup):
    farm = Farm(name="Green Acres")
    farm.save()

    # Assert farm is saved correctly
    assert farm.name == "Green Acres"

def test_cow_creation(setup):
    farm = Farm(name="Green Acres").save()
    cow = Cow(
        name="Bessie", breed="Holstein", maturity=["calf"],
        pregnancy_status="not_pregnant", age=4.5, is_pregnant=False,
        health_status="healthy", farm_id=farm.id
    )
    cow.save()

    # Assert cow is saved correctly
    assert cow.name == "Bessie"
    assert cow.breed == "Holstein"
    assert cow.age == 4.5
    assert str(cow.farm_id.id) == str(farm.id)
    assert cow.id is not None  # Check if cow _id is assigned

def test_health_report_creation(setup):
    cow = Cow(name="Bessie", breed="Holstein", maturity=["calf"]).save()
    health_report = HealthReport(
        cow=cow, report_details="General health checkup", recommendation="Keep up the good work"
    )
    health_report.save()

    # Assert health report is saved correctly
    assert health_report.cow == cow
    assert health_report.report_details == "General health checkup"
    assert health_report.recommendation == "Keep up the good work"
    assert health_report.id is not None  # Check if health report _id is assigned

def test_milking_event_creation(setup):
    cow = Cow(name="Bessie", breed="Holstein", maturity=["calf"]).save()
    farm = Farm(name="Green Acres").save()
    milking_event = MilkingEvent(
        cow=cow, milk_quantity=10.5, milker="John Doe", milking_method="machine", farm_id=farm.id
    )
    milking_event.save()

    # Assert milking event is saved correctly
    assert milking_event.cow == cow
    assert milking_event.milk_quantity == 10.5
    assert milking_event.milker == "John Doe"
    assert str(milking_event.farm_id.id) == str(farm.id)
    assert milking_event.id is not None  # Check if milking event _id is assigned

def test_feed_creation(setup):
    cow = Cow(name="Bessie", breed="Holstein", maturity=["calf"]).save()
    feed = Feed(cow=cow, feed_type="Silage", feed_amount=5.0)
    feed.save()

    # Assert feed is saved correctly
    assert feed.cow == cow
    assert feed.feed_type == "Silage"
    assert feed.feed_amount == 5.0
    assert feed.id is not None  # Check if feed _id is assigned

def test_breeding_creation(setup):
    cow1 = Cow(name="Bessie", breed="Holstein", maturity=["calf"]).save()
    cow2 = Cow(name="Daisy", breed="Jersey", maturity=["calf"]).save()
    breeding = Breeding(cow=cow1, breeding_partner=cow2, breeding_date=datetime.utcnow())
    breeding.save()

    # Assert breeding event is saved correctly
    assert breeding.cow == cow1
    assert breeding.breeding_partner == cow2
    assert breeding.id is not None  # Check if breeding _id is assigned

def test_video_analysis_creation(setup):
    cow = Cow(name="Bessie", breed="Holstein", maturity=["calf"]).save()
    video_analysis = VideoAnalysis(
        cow=cow, video_url="http://example.com/video.mp4", analysis_results="No diseases detected", recommendation="Healthy cow"
    )
    video_analysis.save()

    # Assert video analysis is saved correctly
    assert video_analysis.cow == cow
    assert video_analysis.video_url == "http://example.com/video.mp4"
    assert video_analysis.analysis_results == "No diseases detected"
    assert video_analysis.recommendation == "Healthy cow"
    assert video_analysis.id is not None  # Check if video analysis _id is assigned

def test_invalid_cow_creation(setup):
    # Cow without required field `name`
    with pytest.raises(Exception):
        cow = Cow(breed="Holstein", maturity=["calf"])
        cow.save()
