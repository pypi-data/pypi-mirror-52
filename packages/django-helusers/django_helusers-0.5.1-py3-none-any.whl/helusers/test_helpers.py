from social_django.utils import load_backend, load_strategy


def logged_in_user(uuid=None, email=None):
    strategy = load_strategy()
    backend = load_backend(
        strategy,
        name='tunnistamo',
        redirect_uri=None
    )

    if not uuid:
        uuid = '12345678-1234-5678-1234-567812345678'

    if not email:
        email = 'test@example.com'

    return backend.authenticate(backend=backend, strategy=strategy, response=dict(
        sub=uuid,
        id_token=dict(email=email),
    ))
