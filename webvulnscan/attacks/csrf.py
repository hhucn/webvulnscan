from ..log import vulnerability


def fill_entries(form, filter_type=None):
    for form_input in form.get_inputs():
        input_name = form_input.get_name
        input_value = form_input.guess_value()
        input_type = form_input.get_type

        if filter_type is None:
            yield input_name, input_value
        else:
            if input_type != filter_type:
                yield input_name, input_value


def try_csrf(form, client):
    # First, we send a valid request.
    valid_parameters = dict(fill_entries(form))
    form.send(client, valid_parameters)

    # Now, we supress every thing that looks like a token.
    broken_parameters = dict(fill_entries(form, "hidden"))
    response = form.send(client, broken_parameters)

    # Check if Request passed
    if response.status_code == 200:
        # Request passed, CSRF found...
        vulnerability("Vulnerability: CSRF under " + form.action)


def csrf(target_page, client):
    for form in target_page.get_forms():
        try_csrf(form, client)
