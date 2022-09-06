from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext

def authent(site_url,client_id,client_secret):
    try:
        client_credentials = ClientCredential(client_id,client_secret)
        ctx = ClientContext(site_url).with_credentials(client_credentials)
        web = ctx.web
        ctx.load(web)
        ctx.execute_query()
        print("Web title: {0}".format(web.properties['Title']))
        return ctx
    except Exception as err:
        print('Authentification failed')