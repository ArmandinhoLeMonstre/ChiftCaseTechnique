import xmlrpc.client

class OdooClient:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password

        try:
            self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        except OSError as e:
            raise RuntimeError(f'{e}, Odoo url probably invalid or unreachable')
        
        self.uid = self.common.authenticate(db, username, password, {})
        if not self.uid:
            raise RuntimeError(f'Authentification failed for {username} on {db}')

        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    def search_read(self, model, fields=None, limit=100, offset=0, order=None):
        kwargs = {}

        if fields:
            kwargs["fields"] = fields
        if limit:
            kwargs["limit"] = limit
        if offset:
            kwargs["offset"] = offset
        if order:
            kwargs["order"] = order

        try:
            data = self.models.execute_kw(
                self.db,
                self.uid,
                self.password,
                model,
                "search_read",
                [],
                kwargs
            )
        except xmlrpc.client.Fault as e:
            raise RuntimeError(f'Query problem : {e.faultString}')
        except Exception as e:
            raise RuntimeError(f'Unexpected error : {e}')

        return(data)

