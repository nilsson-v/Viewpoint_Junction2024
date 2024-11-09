import requests

url1 = "http://127.0.0.1:8080/embed_text"
url2 = "http://127.0.0.1:8080/add_article"
url3 = "http://127.0.0.1:8080/similarity_search_article"
url4 = "http://127.0.0.1:8080/generate_text"

data1 = {"text": "Test input for embedding"}

data2 = {
    "topic": "Sisäministerin tehtävän jakautuminen ja poliittinen jatkuvuus",
    "statements": "Ministerin henkilökohtaiset syyt eivät saa vaikuttaa hallituksen toimintaan | Tyttären sairastuminen oli hyvä syy väliaikaiselle ministerinvaihdolle | Liikenne- ja viestintäministeri Lulu Ranne pystyi hoitamaan sisäministerin tehtävää hyvin väliaikaisesti",
    "article": "Mari Rantanen palaa sis\u00e4ministeriksi Perussuomalaisten kansanedustaja Mari Rantanen palaa t\u00e4n\u00e4\u00e4n sis\u00e4ministerin teht\u00e4v\u00e4\u00e4n. Rantanen j\u00e4i teht\u00e4v\u00e4st\u00e4 v\u00e4liaikaisesti sivuun elokuun lopulla tytt\u00e4rens\u00e4 sairastumisen vuoksi. Silloin h\u00e4n arvioi, ett\u00e4 voisi palata ministeriksi vasta vuodenvaihteen paikkeilla. Vakavasti sairaana ollut tyt\u00e4r on kuitenkin toipunut ennakoitua nopeammin. Perussuomalaisten Lulu Ranne on t\u00e4ll\u00e4 v\u00e4lin hoitanut sis\u00e4ministerin teht\u00e4v\u00e4\u00e4 liikenne- ja viestint\u00e4ministerin pestins\u00e4 ohella."
    }

data3 = {
    "topic": "Sisäministerin kahvihetki venyi liian pitkäksi, politiikka jatkui siitä huolimatta",
    }

data4 = {"text": "What is the best way to drink coffee?"}

try:
    response = requests.post(url4, json=data4)
    response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
    print("\n\n\n\n")
    print(response.json())
    print("\n\n\n\n")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except ValueError:
    print("Response was not JSON:", response.text)
