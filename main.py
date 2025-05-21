from bs4 import BeautifulSoup
import requests
import json

vacancy='it'
region='ulan-ude'
area=1118

base_url = f'https://hh.ru/search/vacancy?text= {vacancy}&area={area}'
    
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36'
}

response = requests.get(base_url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
    
pagination_links = soup.find_all('a', class_='magritte-number-pages-action___e3ozw_4-0-44')
page_numbers = [int(link.get_text(strip=True)) for link in pagination_links if link.get_text(strip=True).isdigit()]
max_page = max(page_numbers) if page_numbers else 1

vacancies = []
    
for page in range(max_page):
    url = f'{base_url}&page={page}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
        
    vacancy_cards = soup.find_all('div', class_='magritte-redesign')
        
    for card in vacancy_cards:
            title_tag = card.find('span', {'data-qa': 'serp-item__title-text'})
            title = title_tag.get_text(strip=True) if title_tag else "Не указана"

            company_tag = card.find('span', {'data-qa': 'vacancy-serp__vacancy-employer-text'})
            company = company_tag.get_text(strip=True) if company_tag else "Не указана"
                
            salary_tag = card.find('span', class_='magritte-text___pbpft_3-0-33 magritte-text_style-primary___AQ7MW_3-0-33 magritte-text_typography-label-1-regular___pi3R-_3-0-33')
            salary = salary_tag.get_text(strip=True) if salary_tag else "Не указана"      
                
            experience_tag = card.find('span', {'data-qa': 'vacancy-serp__vacancy-experience'})
            experience = experience_tag.get_text(strip=True) if experience_tag else "Не указан"
                
            address_tag = card.find('span', {'data-qa': 'vacancy-serp__vacancy-address'})
            address = address_tag.get_text(strip=True) if address_tag else "Не указан"
        
            link_tag = card.find('a', {'data-qa': 'serp-item__title'})
            link = link_tag['href'] if link_tag else "#"
                
            vacancies.append({
                'title': title,
                'company': company,
                'salary': salary,
                'experience': experience,
                'address': address,
                'link': link
            })
            

for i, vacancy in enumerate(vacancies, 1):
    print(f"\n{'='*50}")
    print(f"Вакансия #{i}")
    print(f"Должность: {vacancy['title']}")
    print(f"Компания: {vacancy['company']}")
    print(f"Зарплата: {vacancy['salary']}")
    print(f"Опыт: {vacancy['experience']}")
    print(f"Адрес: {vacancy['address']}")
    print(f"Ссылка: {vacancy['link']}")
print(f"\nВсего найдено вакансий: {len(vacancies)}")

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)
