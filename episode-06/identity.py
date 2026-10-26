# A tiny stand-in for AgentCore Identity, to show the ideas:
#  1. Inbound: check WHO is calling the agent (a signed user token).
#  2. Token vault: secrets live here, never in the agent's code.
#  3. Consent: the user must say yes before the agent gets a token.
import functools
import time

import jwt

LOGIN_KEY = "identity-provider-demo-key-0000001"  # sign-ins
VAULT = {  # credential providers, kept out of the agent's code
    "calendar": {"secret": "calendar-demo-secret-not-real-0001"},
}
CONSENT = set()  # (user, provider) pairs the user approved
EVENTS = []      # what the page shows, step by step


def sign_in(user):
    claims = {"sub": user, "exp": time.time() + 3600}
    return jwt.encode(claims, LOGIN_KEY, algorithm="HS256")


def check_inbound(token):
    # Inbound auth: reject anyone without a valid sign-in token.
    user = jwt.decode(token, LOGIN_KEY, algorithms=["HS256"])["sub"]
    EVENTS.append(("inbound", f"Valid token. The user is {user}"))
    return user


class ConsentNeeded(Exception):
    pass


def get_access_token(provider, user):
    if (user, provider) not in CONSENT:
        EVENTS.append(("consent", f"{user} has not allowed it yet"))
        raise ConsentNeeded(provider)
    secret = VAULT[provider]["secret"]
    claims = {"sub": user, "exp": time.time() + 300}  # 5 minutes
    EVENTS.append(("vault", f"Vault issued a 5-minute {provider} "
                            f"token for {user}"))
    return jwt.encode(claims, secret, algorithm="HS256")


def requires_access_token(provider):
    # Like AgentCore's decorator: fetch a token, inject it.
    def wrap(tool):
        @functools.wraps(tool)
        def run(*args, user, **kwargs):
            token = get_access_token(provider, user)
            return tool(*args, access_token=token, **kwargs)
        return run
    return wrap
