from bs4 import BeautifulSoup
import requests
import re
#local -> {bairro}-recife-pe-brasil
#preço -> de-500-a-{valor}-aluguel

translate = {"Graças":"gracas", "Boa Viagem":"boa-viagem", "Várzea":"varzea"}

def return_page(bairro:str, valor:str):
    url = "https://quintoandar.com.br/alugar/imovel/"
    response = requests.get(url+f"{bairro}-recife-pe-brasil/"+f"de-500-a-{valor}-aluguel")

    return response.text

#def get_page_properties(page):
def regexSearch(pattern, page) -> str:
    try:
        result = re.search(pattern, page).group(1)
    except:
        result = ''
    return result

def page_2_result(page: str):
    soup = BeautifulSoup(page, 'html.parser')
    results = []

    divs = soup.find_all('div')
    for card in divs:
        if card.has_attr('data-testid'):
            if card['data-testid'] == 'house-card-details':
                cardText = str(card)
                address = regexSearch(
                    'data-testid="house-card-address">'+'(.+?)'+'</p>', cardText)
                region = regexSearch(
                    'data-testid="house-card-region">'+'(.+?)'+'</p>', cardText)
                region = region.split(',')
                if(len(region) > 1):
                    bairro = region[0].strip()
                    cidade = region[1].strip()
                else:
                    bairro = ""
                    cidade = ""
                for tag in card:
                    if tag.has_attr('data-testid'):
                        if tag['data-testid'] == 'house-card-area':
                            area = tag.text.strip()
                        if tag['data-testid'] == 'house-card-bedrooms':
                            bedrooms = tag.text.strip()
                parent = str(card.parent)
                rent = regexSearch(
                    '<strong>Total'+'(.+?)'+'</strong>', parent).replace('R$', '').strip()
                rent = rent.split(".")
                rent = "".join(rent)
                imageUrl = regexSearch('" src="(.+?)" ', parent)
                imageAlt = regexSearch('<img alt="(.+?)" ', parent)
                results.append({'address': address, 'bairro':bairro,'cidade':cidade,
                               'area': area, 'bedrooms': bedrooms, 'rent': rent, "imageAlt":imageAlt, "imageUrl": "https://www.quintoandar.com.br" + imageUrl})
    return results

def treat_data(datas:list,bairro:str):
    treated_data = []
    sum1 = 0
    for data in datas:
        if(data['bairro'] in translate):
            if(translate[data['bairro']] == bairro):
                sum1 += int(data['rent'])
                treated_data.append({
                    "imageUrl": f"{data['imageUrl']}",
                    "imageAlt": f"{data['imageAlt']}",
                    "tag1": f"{data['bedrooms']}",
                    "tag2": f"{data['area']}",
                    "isLowPrice": True,
                    "title": f"{data['address']}",
                    "formattedPrice": "R$"+f"{data['rent']}",
                    "reviewCount": 0,
                    "rating": 0,
                    "bairro":data['bairro'],
                    "cidade":data['cidade']
                })
    mean = sum1//len(treated_data)
    return {"apts":treated_data, "mean":"R$"+str(mean)}

def get_home_data(bairro:str, preco:str):
    if(bairro in translate):
        translated_bairro = translate[bairro]
        page = return_page(translated_bairro, preco)
        result = page_2_result(page)
        return treat_data(result,translated_bairro)
    else:
        return {}