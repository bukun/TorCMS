import os

c = get_config()
from oauthenticator.django import LocalDjangoOAuthenticator

c.JupyterHub.authenticator_class = LocalDjangoOAuthenticator
# c.JupyterHub.config_file = 'juhub_config.py'
c.ConfigurableHTTPProxy.debug = True
c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.auth_token = "CONFIGPROXY_AUTH_TOKEN"
c.JupyterHub.hub_ip = ""
c.JupyterHub.hub_port = 6797
c.JupyterHub.port = 10882
# c.JupyterHub.logo_file = '/srv/jupyterhub/jupyter.png'
c.JupyterHub.spawner_class = "simplespawner.SimpleLocalProcessSpawner"

c.GenericOAuthenticator.oauth_callback_url = (
    "http://121.42.45.218:6797/hub/oauth_callback"
)

# What is the client ID and client secret for Jupyterhub provided Django?

c.GenericOAuthenticator.client_id = "mZUTp8oysJRMs8MJWQf4pRjnJtFvhAlZwMz7pxCz"
c.GenericOAuthenticator.client_secret = "pbkdf2_sha256$870000$JnQSxM7QQ4UZSOPe6cQuhw$7XMAXUePhFVXZ0Qx56Ka1jYZGQ68a+Nh/tgClfXFp+M="

c.GenericOAuthenticator.authorize_url = "http://121.42.45.218:6795/o/authorize/"

# Where can Jupyterhub get the token from?
c.GenericOAuthenticator.token_url = "http://121.42.45.218:6795/o/token/"

# Where can it get the user name from? What method shall it use?
# What key in the JSON output is the username?
c.GenericOAuthenticator.userdata_url = "http://121.42.45.218:6795/o/usrinfo"
# c.GenericOAuthenticator.userdata_method = 'GET'
# c.GenericOAuthenticator.userdata_method = 'userdata_params'
