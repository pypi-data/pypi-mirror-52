#!/usr/bin/env python
import requests
from requests.adapters import HTTPAdapter
from json import loads
from time import sleep


token = "63c4a071ae4795dcbdd424ff403856170bdb4c359a7b9278f0158b501f98ef17"
headers = {"Authorization" : "Bearer " + token}

s = requests.Session()
s.mount('http', HTTPAdapter(max_retries=3))
s.mount('https', HTTPAdapter(max_retries=3))
s.headers.update(headers)

endpoint = "https://api.digitalocean.com/v2"

create = {
          'name': 'cb-mariner-mydok8stest',
          'region': 'sfo2', 
          'version': '1.14.2-do.0', 
          'node_pools': [
             {
                'size': 's-4vcpu-8gb',
                'name': 'cb-mariner-mydok8stest-pool', 
                'count': 2 
             }
           ]
}

# need tolerate errors, obviously

r = s.post(endpoint + "/kubernetes/clusters", json = create)

kuuid = False
if r.status_code == 201 :
    j = r.json()
    kuuid = j["kubernetes_cluster"]["id"]
    print "Waiting for ready status uuid: " + kuuid 
else :
    print "Create failed: " + str(r.status_code)
    exit(1)

while True :
    r = s.get(endpoint + "/kubernetes/clusters/" + kuuid)

    if r.status_code == 200 :
        if r.json()["kubernetes_cluster"]["status"]["state"] != "provisioning" :
            print "Done."
            break

        print "Still pending, but also checking status: " + str(r.json()["kubernetes_cluster"]["status"])
        sleep(5)
        continue

print "Getting kubeconfig"
r = s.get(endpoint + "/kubernetes/clusters/" + kuuid + "/kubeconfig")

if r.status_code == 200 :
    kubeconfig = r.text
    filename = "/tmp/kubeconfig-" + kuuid + ".yaml"
    print "Writing it out to: " + filename
    fh = open(filename, "w")
    fh.write(kubeconfig)
    fh.close()
else :
    print "Failed to get kubeconfig: " + str(r.status_code)
    exit(1)

fwname = "k8s-" + kuuid + "-worker"
print "Looking up firewall " + fwname + " for this cluster..."

if r.status_code == 200 :
    r = s.get(endpoint + "/firewalls")
else :
    print "Failed to get firewall " + fwname + ": " + str(r.status_code)
    exit(1)

firewalls = r.json()

fwuuid = False

for fw in firewalls["firewalls"] :
    if fw['name'] == fwname :
        fwuuid = fw['id']
        print "Firewall found: " + fwuuid

found = False
while not found :
    r = s.get(endpoint + "/firewalls/" + fwuuid)

    if r.status_code == 200 :
        rules = r.json()
        for rule in rules["firewall"]["inbound_rules"] :
            if str(rule["ports"]).count("30000-32767") :
                print "Found rule: " + str(rule)
                found = True
                break
    else :
        print "Error " + str(r.status_code) + " checking on rule update."
    print "Rule not found yet... Waiting."
    sleep(5)

print "Adding rule to firewall..."

rule = {
  "inbound_rules": [
    {
      "protocol": "tcp",
      "ports": "40000-45000",
      "sources": {
            "addresses": [
              "0.0.0.0/0",
              "::/0"
            ]
      }
    },
    {
      "protocol": "tcp",
      "ports": "22",
      "sources": {
            "addresses": [
              "0.0.0.0/0",
              "::/0"
            ]
      }
    }
  ]
}

r = s.post(endpoint + "/firewalls/" + fwuuid + "/rules", json = rule)

if r.status_code == 204 :
    print "Successfully added firewall rule"
else :
    print "Firewall rule add failed: " + str(r.status_code)

r = s.get(endpoint + "/droplets?tag_name=k8s:" + kuuid)

if r.status_code == 200 :
    for droplet in r.json()["droplets"] :
        print "Droplet ID: " + str(droplet["id"])
        for network in droplet["networks"]["v4"] :
            print " => " + network["type"] + " = " + network["ip_address"]
    raw_input("Press Enter to Cleanup...")
else :
    print "Failed to list droplet IDs. Proceeding with delete: " + str(r.status_code)

print "Deleting..."

r = s.delete(endpoint + "/kubernetes/clusters/" + kuuid)

if r.status_code not in [ 202, 204] :
    print "Failed to delete: " + str(r.status_code)
    exit(1)
    
# Check for delete complete....

print "Waiting for delete to finish..."
while True :
    r = s.get(endpoint + "/kubernetes/clusters/" + kuuid)
    if r.status_code == 404 :
        print "Done."
        break

    print "Still pending, but also checking status: " + str(r.json()["kubernetes_cluster"]["status"])
    sleep(5)
        
print "Deleted"
