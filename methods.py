from urllib.error import URLError

import mechanize
from mechanize import _http
from bs4 import BeautifulSoup

import form


def mechanize_method(username, password, link):
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(_http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Chrome')]

    br.open('https://' + link + '/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess/Classes/Classwork%2f')

    br.select_form(nr=0)

    br.form['LogOnDetails.UserName'] = username
    br.form['LogOnDetails.Password'] = password

    br.submit()

    return br


def fetch_grades(br, link, mp):
    response = br.open("https://" + link + "/HomeAccess/Content/Student/Assignments.aspx")

    soup = BeautifulSoup(response.read(), "lxml")
    p = form.generate_periods(soup)
    marking_periods = []
    # -2: past, -1: current, rest are zero-based
    if mp <= -2:
        for i in range(len(p)-1):
            data = form.generate_form(soup)
            data["ctl00$plnMain$ddlReportCardRuns"] = p[i]
            req = mechanize.Request('https://' + link + '/HomeAccess/Content/Student/Assignments.aspx', data)
            res = br.open(req).read()
            marking_periods.append([BeautifulSoup(res, 'lxml'), p[i][0]])

    else:
        data = form.generate_form(soup)
        data["ctl00$plnMain$ddlReportCardRuns"] = p[mp]
        req = mechanize.Request('https://' + link + '/HomeAccess/Content/Student/Assignments.aspx', data)
        res = br.open(req).read()
        marking_periods.append([BeautifulSoup(res, 'lxml'), p[mp][0]])

    br.close()
    return marking_periods


def main(u, p, l, mp):
    while True:
        try:
            br = mechanize_method(u, p, l)
            return fetch_grades(br, l, mp)
        except URLError:  # sometimes hac isnt very nice and just rejects requests :(
            continue


def login(u, p, l):
    try:
        response = mechanize_method(u, p, l).response()
        soup = BeautifulSoup(response.read(), "lxml")
        if len(soup.find_all('span', text='Your attempt to log in was unsuccessful.')) > 0:
            return "Failed"
        else:
            return "Accepted"
    except URLError:
        return "Failed"
