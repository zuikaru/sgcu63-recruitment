import requests
from bs4 import BeautifulSoup
import esprima
import re
from jinja2 import Template

RUBNONGKAOMAI_BASE_URL = 'https://rubnongkaomai.com'  # home page location


def get_baan_list() -> list:
    """ Get list of baan from rubnongkaomai.com 

    Returns:
        A list of baan dictionary contains nameURL(relative url to baan's page) and size(S/M/L/XL)
    """
    # Find js component location
    baan_response = requests.get(RUBNONGKAOMAI_BASE_URL + '/baan')
    # parse html using beautifulsoup
    baan_soup = BeautifulSoup(baan_response.text, 'html.parser')
    # find all link as=script tags
    possible_js_tags = baan_soup.find_all(
        'link', {'as': 'script', 'rel': 'preload'})
    component_js_location = None
    for tag in possible_js_tags:
        if 'src-pages-baan-js' in tag['href']:
            component_js_location = tag['href']
            break
    # not found
    if component_js_location == None:
        return []
    # get js component file
    baan_js_response = requests.get(
        RUBNONGKAOMAI_BASE_URL + component_js_location)
    # parse js file
    tokens = esprima.tokenize(baan_js_response.text)
    # find allBaanJson variable
    collecting = False
    look_for_size_field = False
    all_bann = []
    current_baan = {}
    idx = 0
    # for each token
    while idx < len(tokens):
        # begin collecting data if we found allBaanJson
        if (tokens[idx].value == 'allBaanJson' and tokens[idx].type == 'Identifier' and
                tokens[idx + 1].type == 'Punctuator' and tokens[idx + 1].value == ':'):
            collecting = True
            idx += 2  # skip head 2 tokens
            continue
        # end collecting data if we found allFile
        if (tokens[idx].value == 'allFile' and tokens[idx].type == 'Identifier' and
                tokens[idx + 1].type == 'Punctuator' and tokens[idx + 1].value == ':'):
            collecting = False
            break
        # If we are in range of allBaanJson object definition
        if collecting:
            # If we found nameURL key
            if tokens[idx].type == 'Identifier' and tokens[idx].value == 'nameURL':
                current_baan['nameURL'] = tokens[idx + 2].value.strip('\"')
                # Try to look for size key
                look_for_size_field = True
                # skip ahead by 3
                idx += 3
                continue
            # If we found size key
            if look_for_size_field and tokens[idx].type == 'Identifier' and tokens[idx].value == 'size':
                # record and push to list
                current_baan['size'] = tokens[idx + 2].value.strip('\"')
                all_bann.append(dict(current_baan))
                # stop looking for size key
                look_for_size_field = False
                # skip ahead by 3
                idx += 3
                continue
        idx += 1
    return all_bann


def get_baan_info(baan: str) -> dict:
    """ Get baan information
    Returns:
        dictionary contains baan name and baan slogan in Thai language4
    """
    # Get baan page
    baan_page_response = requests.get(RUBNONGKAOMAI_BASE_URL + '/baan/' + baan)
    # parse html
    baan_page_soup = BeautifulSoup(baan_page_response.text, 'html.parser')
    # get baan info text wrapper component
    baan_info_text_wrapper = baan_page_soup.find(
        'div', {'class': re.compile('baan-info-module--text-wrapper.*')})
    # name
    baan_name = baan_info_text_wrapper.find('h1', {'type': 'header'}).text
    # slogan
    baan_slogan = baan_info_text_wrapper.find('h3', {'type': 'header'}).text
    return {'name': baan_name, 'slogan': baan_slogan}


def write_table_html(baans: list):
    """ Generate table.html file from given list of baan """
    # read template file
    with open('data/table_template.jinja2', encoding='utf8') as tpl_file:
        template = Template(tpl_file.read())
    # render
    result = template.render(baan_list=baans)
    # write to table.html
    with open('table.html', 'w', encoding='utf8') as table_file:
        table_file.write(result)


def main():
    pass


if __name__ == '__main__':
    main()
