from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from simple_salesforce import Salesforce
import base64
import hashlib
import hmac
import json


@csrf_exempt
def index(request):
    """
    When this view is loaded in a canvas app, Salesforce sends a POST request to it containing the
        currently logged in user's data.
    This post data contains a base64 string of the user's data, along with a signature. We can validate
        the signature by comparing it to our own generated expected signature from our Salesforce
        application's secret key.
    The result of parsing the signed request is that we obtain an instance_url and oauth_token we
        can use to query the Salesforce API. Feel free to dive into the parse_signed_request() function
        to see the nitty-gritty details.
    """
    data = parse_signed_request(request.POST['signed_request'], settings.SALESFORCE_CONSUMER_SECRET)
    if data:
        #User authenticated, let's do queries!

        #Create a simple salesforce instance, using our newly obtained instance_url and oauth_token for authentication.
        sf = Salesforce(instance_url=data['client']['instanceUrl'], session_id=data['client']['oauthToken'])

        #execute a query
        stats = {}
        for opp in sf.query_all("SELECT LeadSource FROM Opportunity WHERE IsWon = True")['records']:
            if opp['LeadSource'] not in stats:
                stats[opp['LeadSource']] = 0
            stats[opp['LeadSource']] += 1

        results = []
        for lead_source,total in stats.items():
            results.append({"lead_source": lead_source, "total": total})
        results = sorted(results, key=lambda k: k['total']*-1) #sort results by total

    else:
        #invalid signed request, throw error.
        pass

    return render(request, 'index.html', {
        "results": results
    })

def parse_signed_request(signed_request, secret):
    """ Used for signed requests, Canvas App Authentication """

    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        #Bad Signature
        return None
    else:
        #Valid signed request
        return data

def base64_url_decode(inp):
    """ Used for signed requests, Canvas App Authentication """
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))