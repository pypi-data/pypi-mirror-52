import re
import validators


def url_without_protocol(domain):
    result = domain
    if domain.__contains__('https://'):
        result = domain.replace('https://', '')
    elif domain.__contains__('http://'):
        result = domain.replace('http://', '')

    return result


def add_http_to_url(url):
    check_protocol_in_url = re.match(r'^(http|https)://', url)
    if check_protocol_in_url is None:
        url = 'http://' + url

    return url


def parse_url(url):
    parsed_url = re.match(r'^(?:\/\/|[^\/]+)*', url)
    if parsed_url is None:
        raise Exception('Invalid domain')

    domain_name = parsed_url.group(0)
    path = url.replace(domain_name, '')

    return domain_name, path


def validate_url(url):
    if url is None or url == '':
        raise Exception('Url is empty')
    is_valid = validators.url(url)
    if not is_valid:
        raise Exception('Invalid url')

