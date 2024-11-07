from app.models import Cow

import uuid 
new_cow = Cow(
    
    name="lucy",
    breed="fresian",
    maturity=['mature'],
    age = 4.0,
    is_pregnant = False,
    health_status="healthy"
)

new_cow.save()
print(f"cow {new_cow.name} has been saved in the db")


