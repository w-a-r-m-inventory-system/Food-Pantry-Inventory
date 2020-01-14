
/*
    https://docs.djangoproject.com/en/2.2/ref/csrf/#setting-the-token-on-the-ajax-request
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function beforeSend(xml_http_request, settings)
{
    if(csrfSafeMethod(settings.type))
        return;

    if(this.crossDomain)
        return;

    var csrftoken = Cookies.get('csrftoken');
    xml_http_request.setRequestHeader("X-CSRFToken", csrftoken);
}