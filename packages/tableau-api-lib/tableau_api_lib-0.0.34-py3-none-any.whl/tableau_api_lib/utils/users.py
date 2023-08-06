from tableau_api_lib.utils import extract_pages
from tableau_api_lib.exceptions import InvalidParameterException


def get_all_users(conn):
    users = extract_pages(conn.get_users_on_site, parameter_dict={'fields': 'fields=_all_'})
    return users
