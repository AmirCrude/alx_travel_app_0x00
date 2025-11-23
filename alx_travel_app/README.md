# ALX Travel App Backend - Milestone 2 (Data Modeling & Seeding)

## Project Overview

This repository contains the backend component for a travel booking application, built using **Django** and **Django Rest Framework (DRF)**.

**Milestone 2** focused on establishing the core data structure (Models), implementing data serialization (Serializers) for API readiness, and creating a custom management command (Seeder) to populate the database for development and testing.

## 🛠️ Setup and Installation

Follow these steps to set up the project environment and prepare the database.

### Prerequisites

- Python (3.x)
- MySQL Server (Running locally or accessible via network)
- Git Bash or a similar Unix-like terminal (recommended for Windows users)

### 1. Clone Repository & Navigate

Assuming you've completed the initial setup and are ready to finalize the project:

```bash
cd ~/.../alx_travel_app_0x00

```

### 2. Activate Virtual Environment and Install Dependencies

```bash
# Activate the virtual environment
source venv/Scripts/activate

# Install required packages (Django, DRF, mysql-connector, etc.)
pip install -r alx_travel_app/requirements.txt
```

### 3. Database Configuration

The project uses environment variables from the .env file to connect to the database.

**Action**: Ensure your MySQL server is running and update the .env file in the project root with the correct credentials.

```.env
# .env file content (Update with your specific values)
SECRET_KEY=your_development_secret_key
DEBUG=True

# --- MySQL Database Configuration ---
DB_ENGINE=mysql.connector.django
DB_NAME=alx_travel_db_0x00             # Must be an existing database name
DB_USER=alx_user
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=3306
```

## Data Modeling & Migration

The following steps define and apply the database structure.

### 1. Core Models

Three core models were implemented in listings/models.py:

Listing: Details of the properties (title, price, location, host).

Booking: Records of reservations (start/end dates, total price, guest).

Review: Feedback on listings (rating, comment, reviewer).

### 2. Run Migrations

These commands create the necessary tables in the alx_travel_db database.

```bash
# Generate the SQL instructions (Migration files were created in a previous step)
python manage.py makemigrations listings

# Execute the SQL and create all tables in MySQL
python manage.py migrate
```

## Database Seeding and Validation

A custom management command, seed.py, was created to populate the database with realistic sample data for development.

### 1. Run the Seeder

Execute the command to populate the database:

```bash
python manage.py seed
```

Expected Output:

```
Starting database seeding...
Existing sample data cleared.
Creating 5 sample users...
...
Database seeding complete!
```

## 2. Validate Data and Serializers

The ListingSerializer in listings/serializers.py includes a nested ReviewSerializer and a custom average_rating field. The following steps validate this logic:

```bash
# Enter the interactive Django shell
python manage.py shell
```

Inside the shell, run the following Python commands:

```python
from listings.models import Listing
from listings.serializers import ListingSerializer

# Check count
print(f"Total Listings: {Listing.objects.count()}")

# Test serializer logic on the first listing
first_listing = Listing.objects.first()
if first_listing:
    serializer = ListingSerializer(first_listing)
    print(f"\n--- Serializer Validation ---")
    print(f"Listing Title: {first_listing.title}")
    print(f"Average Rating (Calculated): {serializer.data.get('average_rating')}")
    print(f"Nested Reviews Count: {len(serializer.data.get('reviews'))}")

exit()
```
