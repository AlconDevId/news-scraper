# ============================================
# Web Scraper - Tech News
# Author: Rizky Maulana (Alcon Dev)
# Description: Scrapes top articles from
#              Hacker News and saves to CSV
# ============================================

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_hackernews():
    url = "https://news.ycombinator.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("🔍 Scraping Hacker News...")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    rows = soup.find_all("tr", class_="athing")
    for row in rows:
        title_cell = row.find("span", class_="titleline")
        if not title_cell:
            continue

        link_tag = title_cell.find("a")
        if not link_tag:
            continue

        title = link_tag.get_text(strip=True)
        link  = link_tag.get("href", "")

        # Score & author are in the next <tr>
        subtext = row.find_next_sibling("tr")
        score = author = "N/A"
        if subtext:
            score_tag  = subtext.find("span", class_="score")
            author_tag = subtext.find("a",    class_="hnuser")
            if score_tag:  score  = score_tag.get_text(strip=True)
            if author_tag: author = author_tag.get_text(strip=True)

        articles.append({
            "title":      title,
            "link":       link,
            "score":      score,
            "author":     author,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return articles


def save_to_csv(articles, filename="tech_news.csv"):
    if not articles:
        print("❌ No data to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["title", "link", "score", "author", "scraped_at"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(articles)

    print(f"✅ Saved {len(articles)} articles → '{filename}'")


def main():
    articles = scrape_hackernews()

    if articles:
        print(f"\n📰 Found {len(articles)} articles:\n")
        for i, a in enumerate(articles[:5], 1):
            print(f"{i}. {a['title'][:75]}")
            print(f"   ⭐ {a['score']}  |  👤 {a['author']}")
            print(f"   🔗 {a['link'][:65]}\n")
        save_to_csv(articles)
    else:
        print("❌ No articles found.")


if __name__ == "__main__":
    main()
