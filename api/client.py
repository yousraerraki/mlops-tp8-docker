"""Interroge le Service Kubernetes pendant N secondes et resume les reponses."""
import collections, json, sys, time, urllib.request

URL = "http://fraude-api/predict"
DUREE = int(sys.argv[1]) if len(sys.argv) > 1 else 10
corps = json.dumps({"montant": 1800, "anciennete": 30, "freq_24h": 4, "nuit": 1}).encode()
par_pod, fin = collections.Counter(), time.time() + DUREE
while time.time() < fin:
    versions, pods, erreurs, t0 = collections.Counter(), set(), 0, time.time()
    while time.time() - t0 < 2:
        try:
            req = urllib.request.Request(URL, corps, {"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=2))
            versions["v" + r["version"]] += 1
            pods.add(r["hote"])
            par_pod[r["hote"]] += 1
        except Exception:
            erreurs += 1
        time.sleep(0.05)
    print(time.strftime("%H:%M:%S"), dict(versions), "pods:", len(pods), "erreurs:", erreurs, flush=True)
print("reponses par pod :", dict(par_pod))
