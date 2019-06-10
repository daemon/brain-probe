import argparse
import sys
import time

from tqdm import tqdm
import requests

from .args import add_dict_options, opt


ARGS = [
    opt('--api-endpoint', type=str, default='https://www.wikidata.org/w/api.php'),
    opt('--delay', type=float, default=0.01)
]


def main():
    parser = argparse.ArgumentParser()
    add_dict_options(parser, ARGS)
    args = parser.parse_args()
    entities = list(sys.stdin)
    print('entity_name\tentity_type\tviews')
    for entity in tqdm(entities):
        time.sleep(args.delay)
        entity, views = entity.strip().split(' ')
        params = dict(action='wbsearchentities', search=entity, language='en', format='json', limit=1)
        try:
            response = requests.get(args.api_endpoint, params=params).json()
            print('\t'.join((entity, response['search'][0]['id'], views)))
        except:
            continue


if __name__ == '__main__':
    main()