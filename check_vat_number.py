#!/usr/local/bin/python3
import zeep
import inquirer
import re

def main():
    print("===============================")
    print("Check a VAT number against VIES")
    print("===============================")
    country_codes = ['AT','BE','BG','CY','CZ','DE','DK','EE','EL','ES','FI','FR','GB','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','RO','SE','SI','SK']
    countries = ['Austria','Belgium','Bulgaria','Cyprus','Czech Republic','Germany','Denmark','Estonia','Greece','Spain','Finland','France','United Kingdom','Croatia','Hungary','Ireland','Italy','Lithuania','Luxembourg','Latvia','Malta','Netherlands','Poland','Portugal','Romania','Sweden','Slovenia','Slovakia']
    questions = [
        inquirer.List('country',
                      message="What's the country code?",
                      choices=country_codes,
                      ),

        inquirer.Text('vat', message="VAT number to check",
                      validate=lambda _, x: re.match('^[-+]?[0-9]+$', x),
                      )
    ]
    answers = inquirer.prompt(questions)
    countrycode = answers['country']
    vat = answers['vat']
    print(checkvat(countrycode, vat))


def checkvat(countrycode, vat):
    wsdl = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    client = zeep.Client(wsdl=wsdl)
    return client.service.checkVat(countrycode, vat)


main()
