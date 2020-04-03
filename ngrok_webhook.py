import requests
import sys

# Find and import urljoin
if sys.version_info[0] < 3:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin
  
# Constants
NGROK_CLIENT_API_BASE_URL = "http://localhost:4040/api"
WEBHOOK_NAME = "pollbot_ngrok_webhook"
WEBHOOK_URL_SUFFIX = "/events"
WEBHOOK_RESOURCE = "all"
WEBHOOK_EVENT = "all"
#WEBHOOK_RESOURCE = "messages"
#WEBHOOK_EVENT = "created"

  
def get_ngrok_public_url():
    """Get the ngrok public HTTP URL from the local client API."""
    try:
        response = requests.get(url=NGROK_CLIENT_API_BASE_URL + "/tunnels",
                                headers={'content-type': 'application/json'})
        response.raise_for_status()

    except requests.exceptions.RequestException:
        print("Could not connect to the ngrok client API; "
              "assuming not running.")
        return None

    else:
        for tunnel in response.json()["tunnels"]:
            if tunnel.get("public_url", "").startswith("http://"):
                print("Found ngrok public HTTP URL:", tunnel["public_url"])
                return tunnel["public_url"]


def delete_webhooks_with_name(api, name):
    """Find a webhook by name."""
    for webhook in api.webhooks.list():
        if webhook.name == name:
            print("Deleting Webhook:", webhook.name, webhook.targetUrl)
            api.webhooks.delete(webhook.id)


def create_ngrok_webhook(api, ngrok_public_url):
    """Create a Webex Teams webhook pointing to the public ngrok URL."""
    print("Creating Webhook...")
    webhook = api.webhooks.create(
        name=WEBHOOK_NAME,
        targetUrl=urljoin(ngrok_public_url, WEBHOOK_URL_SUFFIX),
        resource=WEBHOOK_RESOURCE,
        event=WEBHOOK_EVENT,
    )
    print(webhook)
    print("Webhook successfully created.")
    return webhook


def create_ngrok_attachementwebhook(api, ngrok_public_url):
    """Create a Webex Teams attachement webhook pointing to the public ngrok URL."""
    print("Creating Webhook for attachements...")
    webhook = api.webhooks.create(
        name="pollbot_ngrok_attachementwebhook",
        targetUrl=urljoin(ngrok_public_url, "/attachements"),
        resource="attachmentActions",
        event="created",
    )
    print(webhook)
    print("Attachement Webhook successfully created.")
    return webhook
