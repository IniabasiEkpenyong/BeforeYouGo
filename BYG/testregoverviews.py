#-----------------------------------------------------------------------
# testregoverviews.py (Assignment 3)
# Author: Judah Guggenhim
#-----------------------------------------------------------------------

import sys
import argparse
import playwright.sync_api

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

#-----------------------------------------------------------------------

def get_args():

    parser = argparse.ArgumentParser(
        description='Test the ability of the reg application to '
            + 'handle "primary" (class overviews) queries')

    parser.add_argument(
        'serverURL', metavar='serverURL', type=str,
        help='the URL of the reg application')

    parser.add_argument(
        'browser', metavar='browser', type=str,
        choices=['firefox', 'chrome'],
        help='the browser (firefox or chrome) that you want to use')

    args = parser.parse_args()

    return (args.serverURL, args.browser)

#-----------------------------------------------------------------------

def print_flush(message):

    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def run_test(server_url, browser_process, input_values):

    print_flush(UNDERLINE)
    for key, value in input_values.items():
        print_flush(key + ': |' + value + '|')

    try:
        page = browser_process.new_page()
        page.goto(server_url)

        dept_input = page.locator('#deptInput')
        coursenum_input = page.locator('#coursenumInput')
        area_input = page.locator('#areaInput')
        title_input = page.locator('#titleInput')

        dept_input.fill(input_values.get('dept', ''))
        coursenum_input.fill(input_values.get('coursenum', ''))
        area_input.fill(input_values.get('area', ''))
        title_input.fill(input_values.get('title', ''))

        button = page.locator('#submitButton')
        button.click()

        overviews_table = page.locator('#overviewsTable')
        print_flush(overviews_table.inner_text())

    except Exception as ex:
        print(str(ex), file=sys.stderr)

#-----------------------------------------------------------------------

def main():

    server_url, browser = get_args()

    with playwright.sync_api.sync_playwright() as pw:

        if browser == 'chrome':
            browser_process = pw.chromium.launch()
        else:
            browser_process = pw.firefox.launch()

        run_test(server_url, browser_process,
            {'dept':'COS'})

        run_test(server_url, browser_process,
            {'dept':'COS', 'coursenum':'2', 'area':'qr',
            'title':'intro'})

        # Add more tests here.

        # all classes (no filters)
        run_test(server_url, browser_process,
            {'dept':'', 'coursenum':'', 'area':'',
            'title':''})
        run_test(server_url, browser_process,
                 {'dept': 'WWS'})
        # only course number
        run_test(server_url, browser_process,
            {'coursenum':'333'})

        # only course number, containing letter
        run_test(server_url, browser_process,
            {'coursenum':'b'})

        # only area (case insensitivity)
        run_test(server_url, browser_process,
            {'area':'Qr'})

        # only title keyword
        run_test(server_url, browser_process,
            {'title':'intro'})

        # only title keyword (case insensitivity)
        run_test(server_url, browser_process,
            {'title':'SCIENCE'})

        # multiple filters
        run_test(server_url, browser_process,
            {'dept':'cos', 'coursenum':'3'})

        # case insensitivity
        run_test(server_url, browser_process,
            {'title':'InTrO'})

        # special characters (ensures proper escaping)
        run_test(server_url, browser_process,
            {'title':'C_S'})
        run_test(server_url, browser_process,
            {'title':'c%S'})

        # Spaces:
        run_test(server_url, browser_process,
            {'title':'Independent Study'})
        run_test(server_url, browser_process,
            {'title':'Independent Study '})
        run_test(server_url, browser_process,
            {'title':'Independent Study  '})
        run_test(server_url, browser_process,
            {'title':' Independent Study'})
        run_test(server_url, browser_process,
            {'title':'   Independent Study'})

        # Treat '-c' properly
        run_test(server_url, browser_process,
            {'title':'-c'})

        ### Test inputs that don't quite work:


        # extra ""
        run_test(server_url, browser_process,
            {'dept':'"COS"'})

        # multiple args of same type (attempt at cross-listing)
        run_test(server_url, browser_process,
            {'dept':'PSY/NEU'})
        run_test(server_url, browser_process,
            {'dept':'PSY, NEU'})

        # non-existent department
        run_test(server_url, browser_process,
            {'dept':"XYZ"})

        # non-existent course number
        run_test(server_url, browser_process,
            {'coursenum':'999'})

        # non-existent area
        run_test(server_url, browser_process,
            {'area':'FAKE'})

        # non-existent title substring
        run_test(server_url, browser_process,
            {'title':'Judah Studies'})

        # SQL Injection attempt
        run_test(server_url, browser_process,
            {'title':"intro\' OR \'1\'=\'1"})

if __name__ == '__main__':
    main()
