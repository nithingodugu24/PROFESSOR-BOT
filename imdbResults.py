import requests

def get_imdb_data(user_text):
    base_url = "https://v3.sg.media-imdb.com/suggestion/titles/x/"
    url = f"{base_url}{user_text}.json"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        shows = data.get("d", [])

        for show,i in enumerate(shows):
            print(show,i)
            # Here, you can store or process the information as needed

    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")

# Example usage
user_text = "rangasth"
get_imdb_data(user_text)
