import os
import requests


def _request(path, method="get", data=None):
    url = f"https://api.statuspage.io/v1/pages/{settings.statuspage_page}/{path}"
    headers = {"Authorization": f"OAuth {settings.statuspage_key}"}
    r = requests.request(method, url, headers=headers, data=data)
    if r.status_code != 200 and r.status_code != 201:
        print(f"Received error {r.status_code} for {url} with body:\n{r.content}")
        r.raise_for_status()
    return r.json()


def _get_incidents():
    return _request("incidents/unresolved.json")


def _create_incident(name, body, incident_status, component_id, component_status):
    data = {
        "incident[name]": name,
        "incident[body]": body,
        "incident[status]": incident_status,
        "incident[component_ids][]": component_id,
        f"incident[components][{component_id}]": component_status,
    }
    _request("incidents.json", method="post", data=data)


def _update_incident(incident_id, incident_status, component_id, component_status):
    data = {
        "incident[status]": incident_status,
        "incident[component_ids]": component_id,
        f"incident[components][{component_id}]": component_status,
    }
    _request(f"incidents/{incident_id}.json", method="patch", data=data)


def _component_from_incident(incident):
    return incident["incident_updates"][-1]["affected_components"][-1]["code"]

