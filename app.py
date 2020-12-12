# Importing the modules

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chat import fetch_reply
import requests
import bs4

# Instantiates the flask app
app = Flask(__name__)


# Creates a route
@app.route("/")
def hello():
    return "Hello, World!"


# Creates a route
@app.route("/sms", methods=['POST'])
def sms_reply():
    # Fetch the incoming message
    msg = request.form.get('Body')
    phone_no = request.form.get('From')

    # Create reply
    resp = MessagingResponse()

    # Scrapes the given Url
    try:

        if msg.lower().startswith('get nolly'):

            cmd = msg.lower().split('get nolly ')[1]
            cmd = {'t': cmd}
            url = 'https://www.thenetnaija.com/search'

            # Requests the web page
            web_page = requests.get(url, params=cmd)
            web_page.raise_for_status()

            # Parses the web page with beautiful soup
            soup = bs4.BeautifulSoup(web_page.text, 'html.parser')
            elements = soup.find_all('h3', class_='result-title')

            for element in elements:
                if element.a.text.startswith('Nollywood Movie: '):
                    if 'Part' in element.a.text:
                        continue

                    url = element.a['href']
                    web_page = requests.get(url)
                    web_page.raise_for_status()
                    soup = bs4.BeautifulSoup(web_page.text, 'html.parser')
                    movie_name = element.a.text
                    movie_detail = soup.find('blockquote', class_='quote-content').text
                    caption = soup.find('div', class_='video-about bbcode-text').p.text

                    try:

                        movie_img_name = soup.find('div', class_='video-series').p.img['alt']
                        movie_img_url = soup.find('p', class_='video-image').img['src']
                        resp.message().media(movie_img_url)

                    except:

                        pass

                    try:

                        downloads = soup.find('div', class_='video-series-latest-episodes with-parts')

                        for i in downloads.find_all('li'):

                            movie_name_part = movie_name + ' - ' + i.text
                            movie_url = i.a['href']
                            web_page1 = requests.get(movie_url)
                            web_page1.raise_for_status()
                            soup1 = bs4.BeautifulSoup(web_page1.text, 'html.parser')

                            for y in soup1.find_all('a', class_='button download'):
                                if y['href'].endswith('mp4'):
                                    continue

                                movie_url2 = y['href']
                                web_page2 = requests.get(movie_url2)
                                web_page2.raise_for_status()
                                soup2 = bs4.BeautifulSoup(web_page2.text, 'html.parser')
                                download_link = soup2.find('a', id='download')['href']
                                downlaod_size = soup2.find('span', id='download-size').text
                                downlaod_size = downlaod_size.split('(')[1]
                                downlaod_size = downlaod_size.split(')')[0]

                            resp.message(
                                movie_name_part + '\n\n' + movie_detail + '\n\n' + caption + '\n' + 'Download link: ' + download_link + ' (' + 'Size: ' + downlaod_size + ')')

                    except:

                        for i in soup.find_all('a', class_='button download'):
                            if i['href'].endswith('mp4'):
                                pass

                            elif i['href'].endswith('download'):

                                movie_url = i['href']
                                web_page1 = requests.get(movie_url)
                                web_page1.raise_for_status()
                                soup1 = bs4.BeautifulSoup(web_page1.text, 'html.parser')
                                movie_url = soup1.find('link', rel='canonical')['href']
                                movie_url = movie_url + '?d=1'
                                download_link = soup1.find('input', value=movie_url)['value']
                                downlaod_size = soup1.find('span', class_='size').text
                                downlaod_size = downlaod_size.split('(')[1]
                                downlaod_size = downlaod_size.split(')')[0]

                                resp.message(
                                    movie_detail + '\n\n' + caption + '\n\n' + 'Download link: ' + download_link + ' (' + 'Size: ' + downlaod_size + ')')

        elif msg.lower().startswith('get'):

            cmd = msg.lower().split('get ')[1]
            m_cmd = {'t': cmd}
            url = 'https://www.thenetnaija.com/search'

            # Requests the web page
            web_page = requests.get(url, params=m_cmd)
            web_page.raise_for_status()

            # Parses the web page with beautiful soup
            soup = bs4.BeautifulSoup(web_page.text, 'html.parser')
            main_element = soup.find('main', class_='search-results-list')
            elements = main_element.find_all('h3', class_='result-title')

            for element in elements:
                if element.a.text.startswith('Movie: '):

                    url = element.a['href']

                    # Requests the web page
                    web_page = requests.get(url)
                    web_page.raise_for_status()
                    soup = bs4.BeautifulSoup(web_page.text, 'html.parser')
                    movie_detail = soup.find('blockquote', class_='quote-content').text
                    caption = soup.find('div', class_='video-about bbcode-text').p.text

                    for i in soup.find_all('a', class_='button download'):
                        if i['href'].endswith('mp4'):
                            pass

                        elif i['href'].endswith('download'):

                            movie_url = i['href']
                            web_page1 = requests.get(movie_url)
                            web_page1.raise_for_status()
                            soup1 = bs4.BeautifulSoup(web_page1.text, 'html.parser')
                            movie_url = soup1.find('link', rel='canonical')['href']
                            movie_url = movie_url + '?d=1'
                            download_link = soup1.find('input', value=movie_url)['value']
                            downlaod_size = soup1.find('span', class_='size').text
                            downlaod_size = downlaod_size.split('(')[1]
                            downlaod_size = downlaod_size.split(')')[0]

                        elif i['href'].endswith('html'):

                            movie_sub_url = i['href']
                            web_page2 = requests.get(movie_sub_url)
                            web_page2.raise_for_status()
                            soup2 = bs4.BeautifulSoup(web_page2.text, 'html.parser')
                            movie_sub_url = soup2.find('link', rel='canonical')['href']
                            movie_sub_url = movie_sub_url + '?d=1'
                            sub_download_link = soup2.find('input', value=movie_sub_url)['value']
                            sub_downlaod_size = soup2.find('span', class_='size').text
                            sub_downlaod_size = sub_downlaod_size.split('(')[1]
                            sub_downlaod_size = sub_downlaod_size.split(')')[0]

                    try:

                        resp.message(
                            movie_detail + '\n' + caption + '\n\n' + 'Download link: ' + download_link + ' (' + 'Size: ' + downlaod_size + ')' + '\n\n' + 'Sub download link: ' + sub_download_link + ' (' + 'Size: ' + sub_downlaod_size + ')')

                    except:

                        resp.message(
                            movie_detail + '\n' + caption + '\n\n' + 'Download link: ' + download_link + '(' + 'Size: ' + downlaod_size + ')')

                    try:

                        movie_img_name = soup.find('div', class_='video-image').p.img['alt']
                        movie_img_url = soup.find('div', class_='video-image').p.img['src']

                        resp.message().media(movie_img_url)

                    except:
                        pass
        else:
            reply = fetch_reply(msg, phone_no)
            resp.message(reply)
            text = 'To request a movie, just use the command _*Get Movie Name*_, to get a nollywood movie use _*Get ' \
                   'Nolly Movie Name*_ '
            resp.message(text)

        if 'message' not in str(resp).lower():
            text = 'I am sorry, something went wrong!' + '\n\n' + 'To request a movie, just use the command _*Get ' \
                                                                  'Movie Name*_, to get a nollywood movie use _*Get ' \
                                                                  'Nolly Movie Name*_ '
            resp.message(text)

    except:
        text = 'I am sorry, something went wrong!' + '\n\n' + 'To request a movie, just use the command _*Get Movie ' \
                                                              'Name*_, to get a nollywood movie use _*Get Nolly Movie' \
                                                              ' Name*_ '
        resp.message(text)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
