from tagcounter.tagService import TagService
from tagcounter.DB.domainRepo import DomainRepo
from tagcounter.DB.pageRepo import PageRepo
import argparse
from tagcounter import urlParser
from tagcounter import yamlService
from tld import get_tld
from tagcounter.gui import start_gui


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--get", help="site which will be parsed")
    parser.add_argument("-v", "--view", help="url about which information will be shown")
    parser.add_argument("-s", "--start", help="start gui", action='store_true')
    args = parser.parse_args()

    counter = TagService()
    page_repo = PageRepo()
    domain_repo = DomainRepo()

    if args.get is not None:
        tags = counter.count_tags(args.get)
        print()
        print('Tags: {}'.format(tags))
    elif args.view is not None:
        value = yamlService.get_value_by_key(args.view)
        url = value if value else args.view

        url = urlParser.add_http_to_url(url)
        urlParser.validate_url(url)
        info = get_tld(url, as_object=True)
        domain_with_suffix = info.parsed_url[1]

        domain = domain_repo.get_domain_by_name(urlParser.url_without_protocol(domain_with_suffix))
        if domain is not None:
            pages = page_repo.get_pages_by_domain_id(domain.id)
            if pages is not None:
                for page in pages:
                    print(page)
            else:
                print('Domain is not exist in database')
    elif args.start:
        start_gui()


if __name__ == '__main__':
    main()
