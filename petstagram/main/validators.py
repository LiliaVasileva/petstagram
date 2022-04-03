from django.core.exceptions import ValidationError


# когато искаме да направим къстоме валидатор, който да работи с определени стойности
# примерно чарс да са само - а , б, в, го създаме по този начин, че да връща функцията валидатор
# django работи така, подаваме само референция към функцията, а когато трябва джанго си ги извиква,ь
# не ги извикваме сами със някаква стойност, само ако искаме нещо много специфично го правим както по долу
# def only_chars_validator(chars):
#     def validator(value):
#         #validation
#         pass
#     return validator


def validate_only_letters(
        value):  # винаги взима една стойност трябва да върне None ако всичко е наред, и ValidationError ако има грешка
    for ch in value:
        if not ch.isalpha():
            # Invalid case
            raise ValidationError('Value must contain only letters')
        # valid case


def validate_file_max_size_in_mb(max_size):
    def validate(value):
        file_size = value.file.size  # имаге и файл полетата имат файл стойност, която има и сайзе стойност, получавем един имач, който си има файл и размер;
        if file_size > max_size * 1024 * 1024:
            raise ValidationError(f'Max file size is {max_size}')

    return validate
