

def generate_periods(soup):
    periods = soup.findAll(id='plnMain_ddlReportCardRuns')[0].contents
    p = []
    for x in periods:
        if str(x.string) != '\n':
            p.append(x['value'])
            if 'selected' in str(x):
                p.insert(1, x['value'])
    p.pop(0)
    return p


def generate_form(soup):
    values = {}
    for field in soup.findAll('input'):
        values.update({field['name']: field['value']})
    values["ctl00$plnMain$ddlClasses"] = "ALL"
    values["ctl00$plnMain$ddlCompetencies"] = "ALL"
    values["cctl00$plnMain$ddlOrderBy"] = "Class"
    values["__EVENTTARGET"] = "ctl00$plnMain$btnRefreshView"
    return values
