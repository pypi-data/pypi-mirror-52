import re
from typing import List, Dict, Optional

import requests

from robotoff import settings
from robotoff.utils import get_logger

http_session = requests.Session()
USER_AGENT_HEADERS = {
    'User-Agent': settings.ROBOTOFF_USER_AGENT,
}
http_session.headers.update(USER_AGENT_HEADERS)

POST_URL = "https://world.openfoodfacts.org/cgi/product_jqm2.pl"
DRY_POST_URL = "https://world.openfoodfacts.net/cgi/product_jqm2.pl"
AUTH = ("roboto-app", settings.OFF_PASSWORD)
AUTH_DICT = {
    'user_id': AUTH[0],
    'password': AUTH[1],
}

API_URL = "https://world.openfoodfacts.org/api/v0"
PRODUCT_URL = API_URL + "/product"

logger = get_logger(__name__)


BARCODE_PATH_REGEX = re.compile(r"^(...)(...)(...)(.*)$")


def split_barcode(barcode: str) -> List[str]:
    if not barcode.isdigit():
        raise ValueError("unknown barcode format: {}".format(barcode))

    match = BARCODE_PATH_REGEX.fullmatch(barcode)

    if match:
        return [x for x in match.groups() if x]

    return [barcode]


def generate_json_ocr_url(barcode: str, image_name: str) -> str:
    splitted_barcode = split_barcode(barcode)
    path = "/{}/{}.json".format('/'.join(splitted_barcode), image_name)
    return settings.OFF_IMAGE_BASE_URL + path


def generate_image_url(barcode: str, image_name: str) -> str:
    splitted_barcode = split_barcode(barcode)
    path = "/{}/{}.jpg".format('/'.join(splitted_barcode), image_name)
    return settings.OFF_IMAGE_BASE_URL + path


def product_exists(barcode: str) -> bool:
    return get_product(barcode, ['code']) is not None


def is_valid_image(barcode: str, image_id: str) -> bool:
    product = get_product(barcode, fields=['images'])

    if product is None:
        return False

    images = product.get('images', {})

    return image_id in images


def get_product(barcode: str, fields: List[str] = None) -> Optional[Dict]:
    fields = fields or []
    url = PRODUCT_URL + "/{}.json".format(barcode)

    if fields:
        # requests escape comma in URLs, as expected, but openfoodfacts server
        # does not recognize escaped commas.
        # See https://github.com/openfoodfacts/openfoodfacts-server/issues/1607
        url += '?fields={}'.format(','.join(fields))

    r = http_session.get(url)

    if r.status_code != 200:
        return None

    data = r.json()

    if data['status_verbose'] != 'product found':
        return None

    return data['product']


def add_category(barcode: str, category: str, dry=False,
                 insight_id: Optional[str] = None):
    comment = "Adding category '{}'".format(category)

    if insight_id:
        comment += " (automated edit, ID: {})".format(insight_id)
    else:
        comment += " (automated edit)"

    params = {
        'code': barcode,
        'add_categories': category,
        'comment': comment,
        **AUTH_DICT
    }
    update_product(params, dry=dry)


def update_quantity(barcode: str, quantity: str, dry=False,
                    insight_id: Optional[str] = None):
    comment = "Updating quantity to '{}'".format(quantity)

    if insight_id:
        comment += " (automated edit, ID: {})".format(insight_id)
    else:
        comment += " (automated edit)"

    params = {
        'code': barcode,
        'quantity': quantity,
        'comment': comment,
        **AUTH_DICT,
    }
    update_product(params, dry=dry)


def save_ingredients(barcode: str, ingredient_text: str,
                     lang: str = None, dry=False):
    ingredient_key = ('ingredients_text' if lang is None
                      else f'ingredients_{lang}_text')
    params = {
        'code': barcode,
        'comment': "Ingredient spellcheck correction (automated edit)",
        ingredient_key: ingredient_text,
        **AUTH_DICT,
    }
    update_product(params, dry=dry)


def update_emb_codes(barcode: str, emb_codes: List[str], dry=False,
                     insight_id: Optional[str] = None):
    emb_codes_str = ','.join(emb_codes)

    comment = "Adding packager codes '{}'".format(emb_codes_str)

    if insight_id:
        comment += " (automated edit, ID: {})".format(insight_id)
    else:
        comment += " (automated edit)"

    params = {
        'code': barcode,
        'emb_codes': emb_codes_str,
        'comment': comment,
        **AUTH_DICT,
    }
    update_product(params, dry=dry)


def update_expiration_date(barcode: str, expiration_date: str, dry=False,
                           insight_id: Optional[str] = None):
    comment = "Adding expiration date '{}'".format(expiration_date)

    if insight_id:
        comment += " (automated edit, ID: {})".format(insight_id)
    else:
        comment += " (automated edit)"

    params = {
        'code': barcode,
        'expiration_date': expiration_date,
        'comment': comment,
        **AUTH_DICT,
    }
    update_product(params, dry=dry)


def add_label_tag(barcode: str, label_tag: str, dry=False,
                  insight_id: Optional[str] = None):
    comment = "Adding label tag '{}'".format(label_tag)

    if insight_id:
        comment += " (automated edit, ID: {})".format(insight_id)
    else:
        comment += " (automated edit)"

    params = {
        'code': barcode,
        'add_labels': label_tag,
        'comment': comment,
        **AUTH_DICT,
    }
    update_product(params, dry=dry)


def add_brand(barcode: str, brand: str, dry=False,
              insight_id: Optional[str] = None):
    comment = "Adding brand '{}'".format(brand)

    if insight_id:
        comment += " (automated edit, ID: {})".format(insight_id)
    else:
        comment += " (automated edit)"

    params = {
        'code': barcode,
        'add_brands': brand,
        'comment': comment,
        **AUTH_DICT,
    }
    update_product(params, dry=dry)


def add_store(barcode: str, store: str, dry=False,
              insight_id: Optional[str] = None):
    comment = "Adding store '{}'".format(store)

    if insight_id:
        comment += " (automated edit, ID: {})".format(insight_id)
    else:
        comment += " (automated edit)"

    params = {
        'code': barcode,
        'add_stores': store,
        'comment': comment,
        **AUTH_DICT,
    }
    update_product(params, dry=dry)


def update_product(params: Dict, dry=False):
    if dry:
        r = http_session.get(DRY_POST_URL, params=params,
                             auth=('off', 'off'))
    else:
        r = http_session.get(POST_URL, params=params)

    r.raise_for_status()
    json = r.json()

    status = json.get('status_verbose')

    if status != "fields saved":
        logger.warn(
            "Unexpected status during product update: {}".format(
                status))
