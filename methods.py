import urllib

from bs4 import BeautifulSoup
import mechanize
import form


def mechanize_method(username, password, link):
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Chrome')]

    br.open('https://' + link + '/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess/Classes/Classwork%2f')

    br.select_form(nr=0)

    br.form['LogOnDetails.UserName'] = username
    br.form['LogOnDetails.Password'] = password

    br.submit()

    response = br.open("https://" + link + "/HomeAccess/Content/Student/Assignments.aspx")

    soup = BeautifulSoup(response.read(), "lxml")

    p = form.generate_periods(soup)
    marking_periods = []
    for i in p:
        data = form.generate_form(soup)

        data["ctl00$plnMain$ddlReportCardRuns"] = i
        req = mechanize.Request('https://' + link + '/HomeAccess/Content/Student/Assignments.aspx', data)
        res = br.open(req).read()
        marking_periods.append(BeautifulSoup(res, 'lxml'))

    marking_periods.append(soup)

    br.close()
    return marking_periods


def main(u, p, l):
    while True:
        try:
            return mechanize_method(u, p, l)
            break
        except urllib.error.URLError as e:  # sometimes hac isnt very nice and just rejects requests :(
            continue
