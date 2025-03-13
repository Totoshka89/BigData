import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import datetime
import json


class Company:
    def __init__(self, name, ticker, price_rub, PE, year_stonks, year_result_percent):
        self.name = name
        self.ticker = ticker
        self.price_rub = price_rub
        self.PE = PE
        self.year_stonks = year_stonks
        self.year_result_percent = year_result_percent


def fetch(url, headers):
    """Выполняет HTTP-запрос и возвращает текст ответа."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверяем статус ответа
    return response.text


def get_usd_to_rub_rate():
    """Получает текущий курс доллара к рублю с сайта Центробанка РФ."""
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime('%d/%m/%Y')
    cb_url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}'
    cb_response = fetch(cb_url, headers={})

    # Парсинг XML
    cb_xml = ET.fromstring(cb_response)

    # Поиск элемента с USD
    for valute in cb_xml.findall('Valute'):
        char_code = valute.find('CharCode').text
        if char_code == 'USD':
            return float(valute.find('Value').text.replace(',', '.'))
    return None


def parse_company_data(link, headers, usd_to_rub, year_stonks):
    """Парсит данные о компании."""
    company_url = f'https://markets.businessinsider.com{link}'
    company_response = fetch(company_url, headers=headers)
    company_soup = BeautifulSoup(company_response, 'html.parser')

    # Название компании
    name_element = company_soup.find('span', class_='price-section__label')
    name = name_element.text.strip() if name_element else None

    # Код компании (ticker)
    price_row = company_soup.find('h1', class_='price-section__identifiers')
    price_span = price_row.find('span', class_='price-section__category') if price_row else None
    ticker = price_span.find('span').text[2:] if price_span else None

    # Текущая цена акции
    price_element = company_soup.find('span', class_='price-section__current-value')
    price_usd = float(price_element.text.replace(',', '')) if price_element else None
    price_rub = round(price_usd * usd_to_rub, 2) if price_usd else None

    # P/E компании
    snapshots = company_soup.find_all('div', class_='snapshot__data-item padding-right--zero')
    PE_snapshot = snapshots[14].get_text(strip=True) if len(snapshots) > 14 else None

    # Очистка значения PE от лишних символов
    if PE_snapshot and PE_snapshot != '-':
        PE = ''.join(filter(lambda x: x.isdigit() or x == '.', PE_snapshot))
        PE = float(PE) if PE else None
    else:
        PE = None

    # 52 Week Low и High
    week_low_element = company_soup.find('div', class_='snapshot__data-item snapshot__data-item--small')
    year_week_low = week_low_element.get_text(strip=True)
    week_low = year_week_low[:-8]

    week_high_element = company_soup.find('div', class_='snapshot__data-item snapshot__data-item--small snapshot__data-item--right')
    year_week_high = week_high_element.get_text(strip=True)
    week_high = year_week_high[:-9]

    # Потенциальная прибыль (year_result_percent)
    if week_low and week_high:
        year_result_percent = round((1 - (float(week_low) / float(week_high))) * 100, 2)
    else:
        year_result_percent = None

    return Company(
        name=name,
        ticker=ticker,
        price_rub=price_rub,
        PE=PE,
        year_stonks=year_stonks,  # Передаем значение из таблицы
        year_result_percent=year_result_percent
    )


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    usd_to_rub = get_usd_to_rub_rate()
    if not usd_to_rub:
        print("Не удалось получить курс доллара к рублю.")
        return

    companies = []

    for i in range(1, 3):  # Парсим первые 2 страницы
        url = f'https://markets.businessinsider.com/index/components/s&p_500?p={i}'
        response = fetch(url, headers=headers)
        soup = BeautifulSoup(response, 'html.parser')

        # Получаем таблицу компаний
        companies_table = soup.find('tbody', class_='table__tbody')
        if not companies_table:
            print(f"Не удалось найти таблицу компаний на странице {i}.")
            continue

        # Парсим строки таблицы
        for tr in companies_table.find_all('tr'):
            # Ссылка на страницу компании
            link_element = tr.find('a')
            if not link_element or 'href' not in link_element.attrs:
                continue

            link = link_element['href']

            # Годовой рост/падение (1 Year)
            year_stonks_element = tr.find_all('td')[7]  # 8-й столбец (индекс 7)
            if year_stonks_element:
                year_stonks_text = year_stonks_element.text.strip()  # Получаем текст из ячейки
                year_stonks_value = year_stonks_text.split('\n')[1]  # Берем второе значение (после \n)
                year_stonks = float(
                    year_stonks_value.replace('%', '')) if year_stonks_value and year_stonks_value != '-' else None
            else:
                year_stonks = None

            try:
                # Парсим данные компании
                company = parse_company_data(link, headers, usd_to_rub, year_stonks)
                if company.name and company.ticker:  # Проверяем, что данные корректны
                    companies.append(company)
            except Exception as e:
                print(f"Ошибка при парсинге компании {link}: {e}")

    # Отладочная информация
    print(f"Собрано компаний: {len(companies)}")

    # Сортировки
    top_price = sorted(companies, key=lambda x: x.price_rub if x.price_rub is not None else 0, reverse=True)[:10]
    top_pe = sorted([c for c in companies if c.PE is not None], key=lambda x: x.PE)[:10]
    top_growth = sorted([c for c in companies if c.year_stonks is not None], key=lambda x: x.year_stonks, reverse=True)[:10]
    top_profit = sorted([c for c in companies if c.year_result_percent is not None], key=lambda x: x.year_result_percent, reverse=True)[:10]

    # Сохранение в JSON
    def create_json(data, key):
        attr_map = {
            "price": "price_rub",
            "P/E": "PE",
            "growth": "year_stonks",
            "potential profit": "year_result_percent"
        }
        return [
            {
                "code": item.ticker,
                "name": item.name,
                key: getattr(item, attr_map[key])
            } for item in data
        ]

    try:
        with open('top_price.json', 'w') as f:
            json.dump(create_json(top_price, "price"), f, indent=2)
        print("Файл top_price.json создан.")
    except Exception as e:
        print(f"Ошибка при создании top_price.json: {e}")

    try:
        with open('top_pe.json', 'w') as f:
            json.dump(create_json(top_pe, "P/E"), f, indent=2)
        print("Файл top_pe.json создан.")
    except Exception as e:
        print(f"Ошибка при создании top_pe.json: {e}")

    try:
        with open('top_growth.json', 'w') as f:
            json.dump(create_json(top_growth, "growth"), f, indent=2)
        print("Файл top_growth.json создан.")
    except Exception as e:
        print(f"Ошибка при создании top_growth.json: {e}")

    try:
        with open('top_profit.json', 'w') as f:
            json.dump(create_json(top_profit, "potential profit"), f, indent=2)
        print("Файл top_profit.json создан.")
    except Exception as e:
        print(f"Ошибка при создании top_profit.json: {e}")


if __name__ == '__main__':
    main()