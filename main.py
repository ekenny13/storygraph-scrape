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
    return sg_review_hit[0]

def parse_storygraph_ratings(sg_address:str):
    print(sg_address)
    sg_identifier = sg_address.split('/')[-1]
    num_reviews = soup_txt.find('h3').find('a').get_text()
    avg_rating = soup_txt.find('span', class_="average-star-rating").get_text()
    avg_rating = avg_rating.strip()
    num_reviews = num_reviews.strip()
    print(sg_identifier)
    print(avg_rating)
    print(num_reviews)

def get_mood_reviews():
    emot_dict = {}
    mood_label = soup_txt.find("div", class_ = 'moods-list-reviews').find_all("span", class_ ='md:mr-1')
    percentages = soup_txt.find("div", class_='moods-list-reviews').find_all("span", class_='percentage')

    for mood, percent in zip(mood_label, percentages):
        mood_text = mood.get_text(strip=True)
        percent_text = percent.get_text(strip=True)
        emot_dict.update({mood_text: percent_text})

    return emot_dict

def get_pace_reviews():
    paces_dict = {}
    pace_labels = soup_txt.find('div', class_='paces-reviews').find_all('span', class_='md:mr-1')
    percentages = soup_txt.find('div', class_='paces-reviews').find_all('span', class_='percentage')

    for pace, percent in zip(pace_labels, percentages):
        pace_text = pace.get_text(strip=True)
        percent_text = percent.get_text(strip=True)
        paces_dict.update({pace_text: percent_text})

    return paces_dict

def parse_review_questions():
    questions = soup_txt.find_all('p', class_='review-character-question')
    responses = soup_txt.find_all('span', class_='review-response-summary')
    question_dictionary = {}
    for question, response in zip(questions, responses):
        question_text = question.get_text(strip=True)
        response_text = response.get_text(strip=True)
        question_dictionary.update({question_text : response_text})

    plot = question_dictionary.get('Plot- or character-driven?')
    plot_res = parse_sg_question(plot)
    print(plot_res)

    development = question_dictionary.get('Strong character development?')
    dev_res = parse_sg_question(development)
    print(dev_res)

    loveable = question_dictionary.get('Loveable characters?')
    loveable_res = parse_sg_question(loveable)
    print(loveable_res)

    diverse = question_dictionary.get('Diverse cast of characters?')
    diverse_res = parse_sg_question(diverse)
    print(diverse_res)

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
    rating = soup_txt.find('span', class_='average-star-rating')
    rt = rating.get_text().strip()
    return rt

def soupify_storygraph_page(url:str):
    print(url + '/community_reviews' )
    comm_review_url = url + '/community_reviews'
    page = requests.get(comm_review_url)
    txt = page.text
    soup = BeautifulSoup(txt, 'html.parser')
    return soup

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    title = 'The Bean Trees'
    author = 'Barbara Kingsolver'
    get_book_review_links(title, author)
    sg_result = get_storygraph_rating_url(title, author)
    soup_txt = soupify_storygraph_page(sg_result)
    parse_storygraph_ratings(sg_result)
    moods = get_mood_reviews()
    paces = get_pace_reviews()
    parse_review_questions()
    rating = parse_rating()

    print(moods)
    print(paces)

    #query = "The Seven Husbands of Evelyn Hugo - Taylor Jenkins Reid storygraph book review"
    #links = []
    #for j in search(query, tld="co.in", num=10, stop=10, pause=2):
       # links.append(j)
       # print(j)

    #print(links)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
