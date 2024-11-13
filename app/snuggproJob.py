import requests
import hmac
import hashlib
from datetime import datetime
import config

class SnuggProJob:

    def __init__(self, firstName, lastName, email, homePhone, address1, city, state, zipCode, 
                 jobType=1, accountId=12056, companyId=2811, programId=7, 
                 fromTemplateId=248196, stageId=2):
        self.jobType = jobType  # Type is Audit
        self.accountId = accountId  # For Steven Qian
        self.companyId = companyId  # For Local Energy Alliance Program
        self.programId = programId  # For LEAP
        self.fromTemplateId = fromTemplateId
        self.stageId = stageId  # Audit

        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.homePhone = homePhone
        self.address1 = address1
        self.city = city
        self.state = state
        self.zipCode = zipCode

        self.public_key = config.SNUGGPRO_PUBLIC_KEY
        self.private_key = config.SNUGGPRO_PRIVATE_KEY
        self.base_url = "https://api.snuggpro.com"

    def get_payload(self):
        return {
            "jobType": self.jobType,
            "accountId": self.accountId,
            "companyId": self.companyId,
            "programId": self.programId,
            "fromTemplateId": self.fromTemplateId,
            "stageId": self.stageId,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "homePhone": self.homePhone,
            "address1": self.address1,
            "city": self.city,
            "state": self.state,
            "zip": self.zipCode
        }
    
    def generate_signature(self, date):
        """
        Generate HMAC SHA256 signature.
        """
        message = date.encode('utf-8')
        secret = self.private_key.encode('utf-8')
        signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
        return signature
    
    
    def create_job(self):
        date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        # Generate timestamp and signature
        signature = self.generate_signature(date)

        # Define headers for the request
        headers = {
            "Authorization": f"Credential={self.public_key},Signature={signature}",
            "X-Date": date,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Define the payload for the new job - customize as required
        payload = self.get_payload()

        # Convert payload to application/x-www-form-urlencoded format
        formatted_payload = "&".join(f"{key}={value}" for key, value in payload.items())

        # Endpoint to create a job
        url = f"{self.base_url}/jobs"
        
        # Send POST request to create the job
        response = requests.post(url, headers=headers, data=formatted_payload)

        # Check response
        if response.status_code == 200:
            print("Job created successfully:", response.json())
        else:
            print("Failed to create job:", response.status_code, response.text)