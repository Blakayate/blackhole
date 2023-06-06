from airium import Airium
import re
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'

def generate_report(services):
  page = Airium()

  TARGET = services[0]

  page('<!DOCTYPE html>')

  with page.html(lang='en'):
    with page.head():
          page.link(rel="icon", type="image/svg", href="blackhole.svg")
          page.link(rel="stylesheet", href='./report.css')
          page.link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")
          page.meta(charset="utf-8")
          with page.title():
            page("Blackhole report")
    # HTML Body Start
    with page.body():
      with page.div(klass='header'):
        with page.h1(klass='main-title'):
          page('Blackhole Report')

      with page.div(klass='content'):
        # Logo
        page.img(src='blackhole.svg', alt='Blackhole logo', klass='logo')
        
        # Target
        with page.span(klass='target'):
          page('Target : ' + TARGET)

        ## Service overview
        with page.div(klass='section'):
          with page.div(klass='section-title'):
            page.h3(_t='Services Overview')
            page.i(onclick='toggleIcon(this)', klass='fa fa-eye-slash')
          with page.div(klass='section-content'):
            with page.table(id="services-overview", klass='table'):
              with page.thead(klass='table-head'):
                page.th(_t='Name')
                page.th(_t='Product')
                page.th(_t='Version')
                page.th(_t='Port')
              with page.tbody():
                for service in services[1:-2]:
                  try:
                    # Check if keys are present, else write empty string
                    name = service.get("name","")
                    product = service.get("product","")
                    version = service.get("version","")
                    port = service.get("port","")
                    with page.tr():
                      page.td(_t=name)
                      page.td(_t=product)
                      page.td(_t=version)
                      page.td(_t=port)
                  except AttributeError:
                    pass
        
        ## CVEs and exploits
        with page.div(klass='section'):
          with page.div(klass='section-title'):
            page.h3(_t='CVEs')
            page.i(onclick='toggleIcon(this)', klass='fa fa-eye')
          with page.div(klass='section-content disabled'):   
            index_id = 0
            for service in services[1:-2]:
              try:
                section_title = service.get('product', '') + ' ' + service.get('version', '')
                if section_title == ' ':
                  section_title = service.get('name', 'No_name_given')

                if service['cve']:
                  with page.div(klass='service-block'):
                    with page.div(klass='section-title'):
                      page.h4(_t=section_title, klass='service-title')
                      page.i(onclick='toggleSubIcon(this)', klass='fa fa-eye')
                    

                    if section_title == 'No_name_given':
                      id_name = section_title + index_id
                    else:
                      id_name = section_title
                    index_id += 1

                    ## CVEs
                    with page.div(id=id_name, klass='service-subcontent disabled'):
                      for cve in service['cve']:
                        with page.div(id=cve['id'], klass='service-comp'):

                          page.h5(_t=cve['id'], klass='exploit')

                          page.a(klass='cve_url', _t='NVD NIST Link', href=cve['url'])
                          page.br()
                          page.br()

                          ### CVSS severity and metrics
                          page.a(_t='CVSS')
                          score = cve['score']

                          with page.table(klass='table'):
                            with page.thead():
                              page.th(_t='CVSS Version')
                              page.th(_t='Score')
                              page.th(_t='Severity')
                            with page.tbody():
                              with page.tr():
                                page.td(_t=score[0]) # CVSS Version
                                page.td(_t=score[1]) # Score
                                page.td(_t=score[2]) # Severity

                          page.h5(_t='Exploits', klass='exploit')

                          exploits = cve['exploits']
                          if exploits[0] == 'No data available':
                            page.a(_t='No exploits found for this CVE')
                          else:
                            with page.table(klass='table'):
                              with page.thead():
                                page.th(_t='Page URL')
                                page.th(_t='Download link')
                              with page.tbody():
                                for exploit in exploits:
                                  with page.tr():
                                    with page.td():
                                      # Get exploit ID from URL string
                                      exploitdb_link = exploit['exploitdb_link']
                                      exploit_id = re.findall(r"[0-9]+$", exploitdb_link)[0]

                                      page.a(_t=exploit_id, href=exploit['exploitdb_link'])
                                    with page.td():
                                      page.a(_t='Download', href=exploit['download_link'])
                else:
                  page.h4(_t=section_title, klass='service-title')
              except AttributeError:
                pass

        # Subdomains enumeration
        with page.div(klass='section'):
          with page.div(klass='section-title'):
            page.h3(_t='Subdomains enumeration')
            page.i(onclick='toggleIcon(this)', klass='fa fa-eye')
          with page.div(klass='section-content disabled'):
            with page.table(id='subdomains', klass='table'):
              with page.thead(klass='table-head'):
                page.th(_t='URLS')
              with page.tbody():
                # Get list of URLs
                subdomains_info = services[-1]['subdomains']
                for url in subdomains_info:
                  with page.tr():
                    page.td(_t=url)
        
        # Bruteforce table
        with page.div(klass='section'):

          with page.div(klass='section-title'):
            page.h3(_t='Bruteforce data')
            page.i(onclick='toggleIcon(this)', klass='fa fa-eye')

          with page.div(klass='section-content disabled'):
            with page.table(id='bruteforce', klass='table'):

              with page.thead(klass='table-head'):
                page.th(_t='Credentials')

              with page.tbody():
                # Get list of credentials
                bruteforce_info = services[-2]['bruteforce']
                for url in bruteforce_info:
                  with page.tr():
                    page.td(_t=url)




    page.script(src="report.js")
    # HTML Body End #
  report_path = FILE_DIR + 'report/blackhole_report.html'
  with open(report_path, 'wb') as f:
    f.write(bytes(page))