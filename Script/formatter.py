def trim_space(text):
    return text.replace(" ", "")


def convert_to_lowercase(text):
    return text.lower()


def email_formatter(input_email):
    if input_email is not None:
        input_email = trim_space(input_email)
        input_email = convert_to_lowercase(input_email)
        return input_email
    else:
        return ''


if __name__ == '__main__':
    string = trim_space(' a@ac.o m')
    print(string)

    string = convert_to_lowercase('AB@ABC.COM')
    print(string)

    email = email_formatter(' AB@ABC.COM')
    print(email)
