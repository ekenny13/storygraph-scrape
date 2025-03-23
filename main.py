from googlesearch import search
from googlesearch import lucky
import requests
from bs4 import BeautifulSoup
import json


def get_book_review_links(title:str, author:str):

    query_str = '{0} - {1} reviews'.format(title, author)
    links = []
    for j in search(query_str, tld="co.in", num=10, stop=10, pause=2):
        links.append(j)

    print(links)

# add in to look for reviews
def get_storygraph_rating_url(title:str, author:str):
    query_str = '{0} - {1} storygraph'.format(title, author)
    links = []
    for j in search(query_str, tld="co.in", num=10, stop=10, pause=2):
        links.append(j)
    print(links)

    sg_review_hit = [url for url in links if "app.thestorygraph.com/books" in url]
    try:
        sg_review_url = sg_review_hit[0]
        print(sg_review_url)
    except IndexError:
        print('book review not hit')
        sg_review_try = [url for url in links if "app.thestorygraph.com/book_reviews" in url]
        for x in sg_review_try:
            print(x.split('/')[-1])
    return sg_review_url

def parse_storygraph_ratings(review_url:str):
    sg_identifier = review_url.split('/')[-1]
    try:
        num_reviews = souped_review_txt.find('h3').find('a').get_text()
        print(num_reviews)
    except AttributeError:
        print('could not find h3/a header')
        try:
            num_reviews = souped_review_txt.find('a', class_="inverse-link underline").get_text()
            print(num_reviews)
        except  AttributeError:
            print('not found')

    avg_rating = souped_review_txt.find('span', class_="average-star-rating").get_text()
    avg_rating = avg_rating.strip()
    num_reviews = num_reviews.strip()
    print(sg_identifier)
    print(avg_rating)
    print(num_reviews)

def get_mood_reviews():
    emot_dict = {}

    for emot_item in souped_review_txt.find_all('p', class_='text-blackish dark:text-white'):
        mood_label = emot_item.find('span', class_='font-medium')
        percentage_text = mood_label.find_next_sibling(string=True).strip() if mood_label else ''

        if mood_label and percentage_text:
            mood = mood_label.text
            percent = int(percentage_text.replace('%', '').replace(':', '').strip())
            emot_dict[mood] = percent

    return emot_dict

def get_pace_reviews():
    paces_dict = {}
    paces_portion = souped_review_txt.find('div', class_='w-full max-w-xl').find_all('span', class_='sr-only')
    for x in paces_portion:
        line = str(x.get_text())
        paces_dict[line.split()[4]] = line.split()[0]

    return paces_dict

def parse_review_questions():
    questions = souped_review_txt.find_all('p', class_='review-character-question')
    responses = souped_review_txt.find_all('span', class_='review-response-summary')
    question_dictionary = {}
    for question, response in zip(questions, responses):
        question_text = question.get_text(strip=True)
        response_text = response.get_text(strip=True)
        question_dictionary.update({question_text : response_text})

    print('plot or character driven')
    plot = question_dictionary.get('Plot- or character-driven?')
    plot_res = parse_sg_question(plot)
    print(plot_res)

    print('strong character development')
    development = question_dictionary.get('Strong character development?')
    dev_res = parse_sg_question(development)
    print(dev_res)

    print('loveable characters')
    loveable = question_dictionary.get('Loveable characters?')
    loveable_res = parse_sg_question(loveable)
    print(loveable_res)

    print('diverse cast of characters')
    diverse = question_dictionary.get('Diverse cast of characters?')
    diverse_res = parse_sg_question(diverse)
    print(diverse_res)

    print('flaws of main character a main focus')
    flaws = question_dictionary.get('Flaws of characters a main focus?')
    flaws_res = parse_sg_question(flaws)
    print(flaws_res)

def parse_sg_question(answer_set:str):
    results_dictionary = {}
    answers = answer_set.split('|')
    for x in answers:
        results_dictionary.update({x.split(':')[0] : x.split(':')[1]})
    return results_dictionary

def parse_rating():
    rating = souped_review_txt.find('span', class_='average-star-rating')
    rt = rating.get_text().strip()
    return rt

def soupify_storygraph_page(url:str):
    page = requests.get(url)
    txt = page.text
    soup = BeautifulSoup(txt, 'html.parser')
    return soup

def get_book_tags():
    base_page = requests.get(base_url)
    base_txt = page.text


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    title = 'Careless People'
    author = 'Sarah Wynn-Williams'
    title = 'The Bean Trees'
    author = 'Barbara Kingsolver'
    get_book_review_links(title, author)
    sg_result = get_storygraph_rating_url(title, author)
    print(sg_result)
    souped_base_txt = soupify_storygraph_page(sg_result)
    comm_review_url = sg_result + '/community_reviews'
    souped_review_txt = soupify_storygraph_page(comm_review_url)
    parse_storygraph_ratings(comm_review_url)
    moods = get_mood_reviews()
    print(moods)
    paces = get_pace_reviews()
    print(paces)
    #parse_review_questions()
    # rating = parse_rating()
