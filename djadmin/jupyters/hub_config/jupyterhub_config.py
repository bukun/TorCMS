# This is how we tell Jupyter to use OAuth instead of the default
# authentication which is done using local Linux user accounts.
import sys
sys.path.append('.')
from config import *
# c = get_config()

c.JupyterHub.authenticator_class = "generic-oauth"

c.GenericOAuthenticator.oauth_callback_url = (
    f"http://{HOST}:{JUPYTER_PORT}/hub/oauth_callback"
)

c.GenericOAuthenticator.client_id = "gOAwmCuSTIHEIisKbW08LoviK1S3cNWiAocpzbX5"
c.GenericOAuthenticator.client_secret = "rPz7UpAPPApg9eIwsEDJAZZHlFjHGoBDPwhIfp7WR2g3DfOH62U2MXJLtYhaDpas9kD6sbfCEfKIctx91UeHxQY8UgP64FVzMow9ssXNFo7meHewqtsNgAA8cezYzibn"

c.GenericOAuthenticator.authorize_url = f"http://{HOST}:{SERVER_PORT}/o/authorize/"

c.GenericOAuthenticator.token_url = f"http://{HOST}:{SERVER_PORT}/o/token/"
c.GenericOAuthenticator.login_service = "联合登录"

c.GenericOAuthenticator.userdata_url = f"http://{HOST}:{SERVER_PORT}/userdata"
c.GenericOAuthenticator.enable_auth_state = False
c.GenericOAuthenticator.scope = ["read", "openid"]
# c.GenericOAuthenticator.userdata_params = {'username': 'username'}
c.GenericOAuthenticator.username_claim = "username"

# c.GenericOAuthenticator.userdata_method = 'GET'
# c.GenericOAuthenticator.userdata_method = 'userdata_params'

c.JupyterHub.port = JUPYTER_PORT  # 6797
c.JupyterHub.hub_port = 18079
c.OAuthenticator.allow_all = True

# 以下不必配置。
# c.GenericOAuthenticator.allowed_users = {"bk"}
# c.GenericOAuthenticator.allowed_groups = {"staff"}
# c.GenericOAuthenticator.admin_users = {"bk"}
# c.GenericOAuthenticator.admin_groups = {"administrator"}
