ROLE_CHOICES = (
    (-1, 'Staff'),
    (0, 'Cityzen'),
    (1, 'Institutional'),
    (2, 'Professionist'),
    (4, 'Company'),
    (6, 'Istitutional Partition Item'),
    (7, 'App'),
)

USER_FIELDS = (
    'username',
    'email',
)

PROFILE_FIELDS = (
    'role',
    'first_name', 'last_name',
    'description', 'picture', 'birthdate',
    'latitude', 'longitude',
    'country',
    'address',
    'language'
)
