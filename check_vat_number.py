#!/usr/local/bin/python3
import zeep
import inquirer
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
    vat_response = checkvat(countrycode, vat)
    if not vat_response['valid']:
        print('')
        print(bcolors.FAIL + 'VAT number is invalid!' + bcolors.ENDC)
        print('')
    else:
        print('')
        print(bcolors.OKGREEN + 'VAT number is valid!' + bcolors.ENDC)
        print('')
        print(bcolors.BOLD + 'Request date: ' + bcolors.ENDC + vat_response['requestDate'].strftime('%d %b %Y'))
        print(bcolors.BOLD + 'VAT number: ' + bcolors.ENDC + vat_response['countryCode'] + ' ' + vat_response['vatNumber'])
        print(bcolors.BOLD + 'Company name: ' + bcolors.ENDC + vat_response['name'])
        print(bcolors.BOLD + 'Address: ' + bcolors.ENDC)
        print(vat_response['address'])
        print('')


def checkvat(countrycode, vat):
    wsdl = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    client = zeep.Client(wsdl=wsdl)
    return client.service.checkVat(countrycode, vat)


main()
