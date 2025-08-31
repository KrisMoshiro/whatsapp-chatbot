from google.cloud import secretmanager

def _fetch_secret_raw(secret_path: str) -> str:
    """
    Retrieve the raw value of a secret from Google Secret Manager.
    """
    try:
        with secretmanager.SecretManagerServiceClient() as client:
            response = client.access_secret_version(request={"name": secret_path})
            return response.payload.data.decode("UTF-8").strip()
    except Exception as e:
        raise RuntimeError(f"Error fetching secret: {e}")