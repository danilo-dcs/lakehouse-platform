# Lakehouse Infra Backend App

# Requirements

- Python >= 3.11
- Resend account and api key (email service provier)
- Passport-Broker service available (only url is needed)
- Couchbase Database >= 7.0 
- Pre-configured encryption keys

# Setup and run

Please check the `src/.env.example` for a template of all the inputs needed to configure the Lakehouse API. Once you have all the details nedeed, do:

1. Copy the file `.env.example` and paste it under the name of `.env` in the root (backend) directory
2. Fill all the environment variables with the appropriate values
3. Install the requirements with `python install -r requirements.txt`
3. Run the app with `fastapi dev src/app.py`
