from selenium import webdriver
import json
import requests
import operator

driver = webdriver.Chrome(
    'C:\\Users\Alicja\AppData\Local\Programs\Python\Python37\selenium\webdriver\chromedriver')
driver.get('https://bitbay.net/pl/tabela-oplat')

withdrawal = driver.find_elements_by_xpath('//*[@id="wyplaty"]/ul[1]')
content = "".join([element.text for element in withdrawal])
array_withdrawal = content.split('\n')
driver.quit()

# z tablicy jednoelementowej tworzymy tablicę dwuelementową
array_withdrawal_split = []
for a in array_withdrawal:
    one_row = a.split(': ')
    array_withdrawal_split.append(one_row)

# wyciągamy z tablicy lista_wyplaty_split pierwszy element w każdym wierszu, uzyskując skróty nazw krypto
name_crypto = []
for i in range(len(array_withdrawal_split)):
    for j in range(len(array_withdrawal_split[i])):
        if j == 0:
            name_crypto.append(array_withdrawal_split[i][0])

#wyciągamy z tablicy lista_wyplaty_split drugi element w każdym wierszu, uzyskując wartość opłat
currency = []
for i in range(len(array_withdrawal_split)):
    for j in range(len(array_withdrawal_split[i])):
        if j == 1:
            currency.append(array_withdrawal_split[i][1])

# usuwamy nawiasy okrągłe, znajdujące się w elemencie tablicy name_crypto
for i in range(len(name_crypto)):
    first = name_crypto[i].find('(')
    last = name_crypto[i].find(')')
    if (first >= 0 and last >= 0):
        found_character = name_crypto[i]
        found_character = found_character[(first+1):last]
        name_crypto[i] = found_character

# tworzymy słownik wypłaty z nową nazwą krypto,czyli bez nawiasów ()
def connect_two_array(first_array, second_array):
    dictionary_connect = {}
    for do_name in range(len(first_array)):
        for do_currency in range(len(second_array)):
            if(do_name == do_currency):
                assign_name = first_array[do_name]
                assign_value_this = float(second_array[do_currency])
                dictionary_connect[assign_name] = assign_value_this
    return dictionary_connect

dictionary_name_currency = connect_two_array(name_crypto, currency)

# fukncja, która pobiera ostatnią cenę z BitBaya danej kryptowaluty
def last_price_Bitbay(crypto_list, kind_of_currency):
    last_price_array = {}
    for crypto_key in crypto_list:
        response = requests.get("https://bitbay.net/API/Public/" + crypto_key + kind_of_currency + "/ticker.json")
        todos = json.loads(response.text)
        for key, value in todos.items():
            if key == 'last':
                last_price_crypto = value
                last_price_array[crypto_key] = last_price_crypto
            if key == 'code':
                print('Kryptowaluta ' + crypto_key + ' nie została znaleziona w walucie ' + kind_of_currency)
    return last_price_array

dictionary_usd = last_price_Bitbay(name_crypto, 'USD')
dictionary_pln = last_price_Bitbay(name_crypto, 'PLN')


# funkcja, która mnoży wartości z dwóch słowników
def cost_withdrawal(dictionary):
    dictionary_cost_withdrawal= {}
    for key_one, value_one in dictionary_name_currency.items():
        for key_two, value_two in dictionary.items():
            if (key_one == key_two):
                dictionary_cost_withdrawal[key_two] = value_one * value_two
    return dictionary_cost_withdrawal

dictionary_usd_cost_withdrawal = cost_withdrawal(dictionary_usd)
dictionary_pln_cost_withdrawal = cost_withdrawal(dictionary_pln)

# print('\n')
# print('Poniżej koszt wyplaty USD:')
# print(slownik_usd_koszt_wyplaty)
#
# print('\n')
# print('Poniżej koszt wyplaty PLN:')
# print(slownik_pln_koszt_wyplaty)

# funkcja,która sortuje slownik po wartości i wartość ustawia na 4 miejsca po przecinku
def sorting(dictionary_costs):
    sorted_d = sorted(dictionary_costs.items(), key=operator.itemgetter(1))
    sorted_dictionary = []
    for i in sorted_d:
        sorted_dictionary.append(list(i))
    for y in range(len(sorted_dictionary)):
        for z in range(len(sorted_dictionary[y])):
            if (z==1):
                sorted_dictionary[y][z] = round(sorted_dictionary[y][z],4)
    return sorted_dictionary

sorted_dictionary_usd = sorting(dictionary_usd_cost_withdrawal)
sorted_dictionary_pln = sorting(dictionary_pln_cost_withdrawal)


print('Lista od najtańszych wypłat w walucie USD')
for f in range(len(sorted_dictionary_usd)):
    for r in range(len(sorted_dictionary_usd[f])):
        if (r==0):
            print('Wypłata: ' + sorted_dictionary_usd[f][0] + ' kosztuje ' + str(sorted_dictionary_usd[f][1]) + ' USD.')


print('\n'+'Lista od najtańszych wypłat w walucie PLN')
for b in range(len(sorted_dictionary_pln)):
    for r in range(len(sorted_dictionary_pln[b])):
        if (r==0):
            print('Wypłata: ' + sorted_dictionary_pln[b][0] + ' kosztuje ' + str(sorted_dictionary_pln[b][1]) + ' ZŁ.')


