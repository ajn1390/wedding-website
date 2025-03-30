# wedding-website
Wedding website project in Python and FastAPI


# start up for now
activate venv (cd venv/Scripts, . activate)

# for adding new dependencies
pip install -r requirements.txt

# server
uvicorn main:app --reload

# Tables

- Names (ids, first, last, alternate names)
- Contact Info (joined sub-tables?)
    - Cell phone numbers(name id, country codes, cell numbers)
    - emails (name id, emails)
    - addresses (name id, country, house number, zip etc)
- Parties(one to two name ids, a party id and label)
    - Some type of json form that a party can see all their joined info?
- Guest data(names, 'primary guest', given a plus one)
- RSVP (name ids, invited status per event, datetime of responses, if changed)
- Events(event id, time location, info)
- Guest lists (event ids, attending names)
- Administrators 

# Features

- Admins have write access to all
- Send email invites per event
- Send texts invites per event
- Send updates via email and/or text
- Access with a general site password and some element of personal data
    - tbd, possibly primary guest last name
    - This assumes we've pre loaded the db with much of the guest info already
- Primary guests can *add/delete* a new person to their party
    - Only if authorized for a plus one
      - most plus ones will already be pre loaded into party data by us
    - No more than two people per party
- Any member of a party can *update* any personal info in their party
- Any member of a party can update the RSVP status of any event the people in the party are invited to
- Admins should receive email updates as guest add/update info
- Aggregate event information (guest dashboard ish style)
- Test env?


# Main Menu
- About Us
- Events
    - Restrict event information to only invited guests of that event
- Your Party
    - Portal for adding/updating info
    - Photos
- Travel and Lodging
- FAQ
- Gifts
- Photo gallery