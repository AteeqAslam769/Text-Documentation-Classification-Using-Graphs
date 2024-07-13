import requests
from bs4 import BeautifulSoup


Science=["https://educatoral.com/wordpress/2024/02/23/school-ai-is-absolutely-amazing-rises-to-top-of-my-list/",
         "https://www.savvas.com/resource-center/blogs-and-podcasts/fresh-ideas-for-teaching/science/2023/earth-day-changing-how-we-look-at-and-use-plastics",
         "https://www.savvas.com/resource-center/blogs-and-podcasts/fresh-ideas-for-teaching/science/2022/biology-a-science-that-keeps-changing",
         "https://www.savvas.com/resource-center/blogs-and-podcasts/fresh-ideas-for-teaching/multi-discipline/2021/4-inspiring-stem-fair-talks-to-use-In-your-classroom",
         "https://www.learningscientists.org/blog/2024/4/11-1",
         "https://www.learningscientists.org/blog/2024/2/15-1",
         "https://www.learningscientists.org/blog/2023/1/26-1",
         "https://www.learningscientists.org/blog/2022/10/20-1",
         "https://www.learningscientists.org/blog/2022/7/21/digest-164",
         "https://www.iflscience.com/tombaugh-regio-simulations-explain-plutos-mysterious-heart-and-gravity-anomaly-73833",
         "https://www.iflscience.com/fools-gold-may-actually-be-more-valuable-than-we-realized-73822",
         "https://www.iflscience.com/first-supernova-in-galaxy-22-million-light-years-away-snapped-by-amateur-astronomers-73816",
         "https://www.iflscience.com/nasa-seeks-ideas-for-faster-and-cheaper-mars-sample-return-amid-delays-73823",
         "https://www.iflscience.com/worlds-4th-global-coral-bleaching-event-confirmed-and-it-could-be-the-worst-yet-73828",
         "https://www.iflscience.com/one-of-the-rarest-minerals-on-earth-runs-through-this-derbyshire-hillside-73741"
         ]

def clean_text(text):
    # Define a translation table to remove punctuation
    translator = str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~’–')
    # Remove punctuation and convert to lowercase
    cleaned_text = text.translate(translator).lower()
    return cleaned_text

def get_website_content():
    i=1
    for url in Science:
        # Send an HTTP GET request to the URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
        response = requests.get(url, headers=headers)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the HTML content using Beautiful Soup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style tags from the HTML
            for tag in soup(['script', 'style']):
                tag.extract()
            total=""
            word_count = 0
            # Check paragraph and heading tags for <a> and <img> tags
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                if tag.find('a'):
                    tag.a.decompose()
                if tag.find('img'):  # Remove <a> tags
                    tag.img.decompose()  # Remove <img> tags

                # Get text from the tag and append to the total content
                text_content = tag.get_text(strip=True)
                words = text_content.split()
                if word_count + len(words) <= 500:
                    total += text_content + " "
                    word_count += len(words)
                else:
                    remaining_words = 500 - word_count
                    total += " ".join(words[:remaining_words]) + " "
                    break  # Stop processing further tags

            with open(f'./ScienceAndEducation/blog{i}.txt', 'w', encoding='utf-8') as file:
                        file.write(clean_text(total))
            i=i+1
            print("Content extracted and saved to 'HealthAndFitness' folder.")
        else:
            print(f"Error: Failed to fetch content from {url}. Status code: {response.status_code}")

# Example usage
get_website_content()
