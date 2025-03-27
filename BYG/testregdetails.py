#-----------------------------------------------------------------------
# testregdetails.py (Assignment 3)
# Author: Judah Guggenheim
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
            + 'handle "secondary" (class details) queries')

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

def run_test(server_url, browser_process, classid):

    print_flush(UNDERLINE)
    try:
        page = browser_process.new_page()
        page.goto(server_url)

        link = page.get_by_text(classid).first
        link.click()

        class_details_table = page.locator('#classDetailsTable')
        print_flush(class_details_table.inner_text())

        course_details_table = page.locator('#courseDetailsTable')
        print_flush(course_details_table.inner_text())

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

        run_test(server_url, browser_process, '8321')


        ### Test valid inputs
        # Test with no value for area, multiple days
        run_test(server_url, browser_process, '8321')

        # Multiple profs and multiple course num/dept crosslistings
        run_test(server_url, browser_process, '9032')

        # Test with no prereqs and a long description
        run_test(server_url, browser_process, '8293')

        # Test with one professor and long (2-line) prereqs
        run_test(server_url, browser_process, '9977')

        # Test with no professor
        run_test(server_url, browser_process, '9012')

        # Test a policy seminar, only 1 day and long (paragraph) prereqs
        run_test(server_url, browser_process, '10188')



#        ### Test invalid inputs:
#        ### NOTE that, as described on Ed, it is not possible
         ### to test these here, and they must be tested manually.

#        # A courseid without corresponding course (exit status 1)
#        run_test(server_url, browser_process, '9034')
#
#        # An empty courseid (yield exit status 2)
#        run_test(server_url, browser_process, '')
#
#        # An alphabetical courseid
#        run_test(server_url, browser_process, 'abcd')
#
#        # A courseid with special characters
#        run_test(server_url, browser_process, '83!@')
#
#        # Multiple courseids
#        run_test(server_url, browser_process, '[\'8321\', \'9032\']')
#
#        # Negative courseid
#        run_test(server_url, browser_process, '-9034')
#
#        # Float courseid
#        run_test(server_url, browser_process, '8321.5')



if __name__ == '__main__':
    main()
