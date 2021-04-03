from bs4 import BeautifulSoup
import requests

source =  requests.get('https://www.cnbctv18.com/healthcare/coronavirus-news-live-updates-india-mumbai-maharashtra-kerala-covid19-vaccine-lockdown-news-3-2-3-8804661.htm')


soup= BeautifulSoup(source,'lxml')

print(soup.prettify())