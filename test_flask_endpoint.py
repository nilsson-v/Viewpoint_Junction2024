import requests
import json

url1 = "http://127.0.0.1:8080/embed_text"
url2 = "http://127.0.0.1:8080/add_article"
url3 = "http://127.0.0.1:8080/similarity_search_article"
url4 = "http://127.0.0.1:8080/generate_text"
url5 = "http://127.0.0.1:8080/get_articles"

url6 = "https://flaskapi-529120302078.europe-north1.run.app/get_articles_test"
url7 = "https://flaskapi-529120302078.europe-north1.run.app/generate_text"

url10 = "https://flaskapi-529120302078.europe-north1.run.app/embed_text"

data1 = {"text": "Test input for embedding"}

data2 = {
    "topic": "Sisäministerin tehtävän jakautuminen ja poliittinen jatkuvuus",
    "statements": "Ministerin henkilökohtaiset syyt eivät saa vaikuttaa hallituksen toimintaan | Tyttären sairastuminen oli hyvä syy väliaikaiselle ministerinvaihdolle | Liikenne- ja viestintäministeri Lulu Ranne pystyi hoitamaan sisäministerin tehtävää hyvin väliaikaisesti",
    "article": "Mari Rantanen palaa sis\u00e4ministeriksi Perussuomalaisten kansanedustaja Mari Rantanen palaa t\u00e4n\u00e4\u00e4n sis\u00e4ministerin teht\u00e4v\u00e4\u00e4n. Rantanen j\u00e4i teht\u00e4v\u00e4st\u00e4 v\u00e4liaikaisesti sivuun elokuun lopulla tytt\u00e4rens\u00e4 sairastumisen vuoksi. Silloin h\u00e4n arvioi, ett\u00e4 voisi palata ministeriksi vasta vuodenvaihteen paikkeilla. Vakavasti sairaana ollut tyt\u00e4r on kuitenkin toipunut ennakoitua nopeammin. Perussuomalaisten Lulu Ranne on t\u00e4ll\u00e4 v\u00e4lin hoitanut sis\u00e4ministerin teht\u00e4v\u00e4\u00e4 liikenne- ja viestint\u00e4ministerin pestins\u00e4 ohella."
    }

data3 = {
    "topic": "US and Ukraine",
    }

data4 = {"text": "US and Ukraine"}

headers = {
    'Content-Type': 'application/json',
}

url77 = "http://127.0.0.1:8080/process_user_viewpoint"
data5 =  {
      "title": "The Growing Impact of Social Media on Political Polarization",
      "date": "2024-11-09",
      "content": "The rapid rise of social media as a primary source of information has contributed significantly to increasing political polarization globally. A recent study by the Pew Research Center shows that 70% of Americans believe political polarization has worsened in the past five years. Social media platforms, with their algorithm-driven feeds, tend to amplify extreme views, leading to more entrenched political divisions. In Finland, political polarization has also risen by 30% in the last decade, partly due to social media's role in shaping public opinion. This growing divide in political ideologies raises concerns about the future of democratic processes and public discourse.",
      "source": "Pew Research Center, 2024"
    }

url55 = "http://127.0.0.1:8080/get_opinions"

url777 = "http://127.0.0.1:8080/search_articles"

try:
    response = requests.post(url777, headers=headers, data=json.dumps(data4))
    #response = requests.get(url5)
    response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
    print("\n\n\n\n")
    print(response.json())
    print("\n\n\n\n")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except ValueError:
    print("Response was not JSON:", response.text)
