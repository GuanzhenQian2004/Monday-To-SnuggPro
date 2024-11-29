import pytest
from app.snuggproJob import SnuggProJob

@pytest.mark.skipif(
    True,
    reason='Skipping external API tests by default'
)
def test_create_snuggpro_job():
    # Initialize the SnuggProJob instance with test data
    job = SnuggProJob(
        firstName="Test",
        lastName="User",
        email="test.user@example.com",
        homePhone="123-456-7890",
        address1="123 Test St",
        city="Testville",
        state="TS",
        zipCode="12345"
    )

    # Call the method to create the job
    response = job.create_job()

    # Assert that the response is successful
    assert response.status_code == 200
    assert 'job created successfully' in response.text.lower()
