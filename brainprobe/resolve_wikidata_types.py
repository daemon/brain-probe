import argparse
import sys
import time

from tqdm import tqdm
import requests

from .args import add_dict_options, opt


ARGS = [
    opt('--api-endpoint', type=str, default='http://tuna.cs.uwaterloo.ca:5555/wikidata/query'),
    opt('--delay', type=float, default=0.001)
]


RESOLVE_TEMPLATE = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?instance
WHERE 
{
  %s wdt:P31 ?instance.
}
LIMIT 5
"""


def main():
    parser = argparse.ArgumentParser()
    add_dict_options(parser, ARGS)
    args = parser.parse_args()
    lines = list(sys.stdin)
    print('entity_name\tentity_type\tentity_instance\tviews')
    for line in tqdm(lines):
        time.sleep(args.delay)
        entity, entity_type, views = line.strip().split('\t')
        data = dict(query=RESOLVE_TEMPLATE % f'wd:{entity_type}')
        try:
            response = requests.post(args.api_endpoint, data=data).json()
            entity_instance = response['results']['bindings'][0]['instance']['value']
            entity_instance = entity_instance.split('/')[-1]
        except:
            entity_instance = ''
        print('\t'.join((entity, entity_type, entity_instance, views)))


if __name__ == '__main__':
    main()