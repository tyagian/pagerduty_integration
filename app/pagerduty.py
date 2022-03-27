import re
import requests


def incident_acknowledged_or_resolved(payload):
    for message in payload["messages"]:
        if (
            message["event"] == "incident.acknowledge"
            or message["event"] == "incident.resolve"
            or message["event"] == "incident.priority_updated"
        ):
            return True
    return False


def _get_acknowledged_incidents(api_key):
    url = "https://api.pagerduty.com/incidents"
    params = {
        "limit": "100",
        "statuses[]": "acknowledged",
        "time_zone": "UTC",
        "include[]": "first_trigger_log_entries",
    }
    headers = {
        "Authorization": f"Token token={api_key}",
        "Accept": "application/vnd.pagerduty+json;version=2",
    }
    r = requests.get(url, params=params, headers=headers)
    if r.status_code != 200:
        print(f"Received error {r.status_code} for {url} with body:\n{r.content}")
        r.raise_for_status()
    incidents = r.json()["incidents"]
    return incidents


def components_with_incidents(api_key):
    components = set()
    incidents = _get_acknowledged_incidents(api_key)
    print(f"Found {len(incidents)} pagerduty incidents")
    for incident in incidents:
        print(f"For pagerduty incident {incident['id']}")
        component = _incident_component(incident)
        if component:
            components.add(component)
    return components

