import requests
from bs4 import BeautifulSoup

def get_html(url: str, file_name: str):
    """Получение HTML-структуры страницы и сохранение в файл."""
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    # Сохраняем HTML в файл
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(response.text)
    return response.text

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Извлечение заголовка вакансии
    title_element = soup.find("h1", {"data-qa": "vacancy-title"})
    title = title_element.text.strip() if title_element else "Заголовок не найден"

    # Извлечение зарплаты
    salary_element = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"})
    salary = salary_element.text.strip() if salary_element else "Зарплата не указана"

    # Извлечение опыта работы
    experience_element = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience_element.text.strip() if experience_element else "Опыт не указан"

    # Извлечение типа занятости и режима работы
    employment_mode_element = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode_element.text.strip() if employment_mode_element else "Не указано"

    # Извлечение компании
    company_element = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company_element.text.strip() if company_element else "Компания не указана"

    # Извлечение местоположения
    location_element = soup.find("p", {"data-qa": "vacancy-view-location"})
    location = location_element.text.strip() if location_element else "Местоположение не указано"

    # Извлечение описания вакансии
    description_element = soup.find("div", {"data-qa": "vacancy-description"})
    description = description_element.text.strip() if description_element else "Описание не указано"

    # Извлечение ключевых навыков
    skills_elements = soup.find_all("div", {"class": "magritte-tag__label___YHV-o_3-0-3"})
    skills = [skill.text.strip() for skill in skills_elements] if skills_elements else ["Навыки не указаны"]

    # Формирование строки в формате Markdown
    markdown = f"""
# {title}

**Компания:** {company}  
**Зарплата:** {salary}  
**Опыт работы:** {experience}  
**Тип занятости и режим работы:** {employment_mode}  
**Местоположение:** {location}  

## Описание вакансии
{description}

## Ключевые навыки
- {'\n- '.join(skills)}
"""

    return markdown.strip()

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение основных данных кандидата
    name_element = soup.find('h2', {'data-qa': 'bloko-header-1'})
    name = name_element.text.strip() if name_element else "Имя не указано"

    gender_age_element = soup.find('p')
    gender_age = gender_age_element.text.strip() if gender_age_element else "Пол/возраст не указаны"

    location_element = soup.find('span', {'data-qa': 'resume-personal-address'})
    location = location_element.text.strip() if location_element else "Местоположение не указано"

    job_title_element = soup.find('span', {'data-qa': 'resume-block-title-position'})
    job_title = job_title_element.text.strip() if job_title_element else "Должность не указана"

    job_status_element = soup.find('span', {'data-qa': 'job-search-status'})
    job_status = job_status_element.text.strip() if job_status_element else "Статус не указан"

    # Извлечение опыта работы
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experience_items = experience_section.find_all('div', class_='resume-block-item-gap') if experience_section else []
    experiences = []
    for item in experience_items:
        period_element = item.find('div', class_='bloko-column_s-2')
        duration_element = item.find('div', class_='bloko-text')
        period = period_element.text.strip() if period_element else "Период не указан"
        duration = duration_element.text.strip() if duration_element else "Длительность не указана"
        period = period.replace(duration, f" ({duration})")

        company_element = item.find('div', class_='bloko-text_strong')
        company = company_element.text.strip() if company_element else "Компания не указана"

        position_element = item.find('div', {'data-qa': 'resume-block-experience-position'})
        position = position_element.text.strip() if position_element else "Позиция не указана"

        description_element = item.find('div', {'data-qa': 'resume-block-experience-description'})
        description = description_element.text.strip() if description_element else "Описание отсутствует"

        experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")

    # Извлечение ключевых навыков
    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})] if skills_section else ["Навыки не указаны"]

    # Формирование строки в формате Markdown
    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    for exp in experiences:
        markdown += exp + "\n"
    markdown += "## Ключевые навыки\n\n"
    markdown += ', '.join(skills) + "\n"

    return markdown

def get_candidate_info(url: str):
    html = get_html(url, "candidate.html")
    return extract_candidate_data(html)

def get_job_description(url: str):
    html = get_html(url, "vacancy.html")
    return extract_vacancy_data(html)
