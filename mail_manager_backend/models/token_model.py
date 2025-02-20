from django.db import models


class TokenManager(models.Manager):
    def get_token_by_user_id(self, user_id: int):
        token = Tokens.objects.get(user_id=user_id)
        return token

    def save_token(
        user_id: int,
        token: str,
        refresh_token: str,
        token_uri: str,
        client_id: str,
        client_secret: str,
        scopes: str,
        expires_at: int,
        universe_domain: str,
        account: str,
    ):
        Tokens.save(
            user_id=user_id,
            token=token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            expires_at=expires_at,
            universe_domain=universe_domain,
            account=account,
        )


class Tokens(models.Model):
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="tokens"
    )
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_uri = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    scopes = models.CharField(max_length=255)
    expires_at = models.IntegerField()
    universe_domain = models.CharField(max_length=255)
    account = models.CharField(max_length=255, null=True, blank=True)

    objects = TokenManager

    class Meta:
        db_table = "tokens"
        # schema = 'public'
