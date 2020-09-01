from bs4 import BeautifulSoup
from collections import namedtuple
import datetime
import os


SRC_DIR = '.'
TEMPLATES_DIR = 'templates'

ARTICLE_CARD = """
<div class="card row">
    <div class="col card-body">
        <a href="{article_link}" class="article-card link">
            <h3 class="card-title">{title}</h3>
        </a>
        <div class="card-text">
            <ul class="taglist">
              {tags}
            </ul>
            <p><b>Published Date:</b> <time datetime="{date}">{readable_date}</time></p>
            <p>{summary}</p>
        </div>
    </div>
</div>
"""

TAGS_PAGE = """
<div class="container mt-4">
    <h2>Tags</h2>
    <ul class="alltags">
        {tags}
    </ul>
</div>
"""

Article = namedtuple('Article', ['title', 'date', 'tags', 'summary', 'path'])


def parse_article(article_path):
  with open(article_path, 'r') as f:
    article_html = f.read()

  path = '/articles/{}'.format(article_path.split('/')[-1])

  soup = BeautifulSoup(article_html, 'html.parser')
  article_soup = soup.find('div', attrs={'class': 'article'})
  assert article_soup, "Failed to find the article class"

  title = article_soup.find('h2')
  assert(title)
  title = title.get_text()

  taglist = article_soup.find(attrs={'class': 'taglist'})
  tags = []
  for tag in taglist.find_all('li'):
    tags.append(tag.get_text().strip())

  date_str = article_soup.find('time').attrs.get('datetime', '')
  assert(date_str)
  year, month, day = map(int, date_str.split('-'))
  date = datetime.date(year, month, day)

  summary = article_soup.find(attrs={'class': 'summary'})
  for tag in summary.find_all(attrs={'class': 'reference'}):
    tag.decompose()

  return Article(title, date, tags, summary, path)


def read_articles():
  article_names = os.listdir(f'{SRC_DIR}/articles')
  article_paths = [os.path.join(os.path.abspath('.'), f'{SRC_DIR}/articles',
      name) for name in article_names if name.endswith('.html')]
  return sorted(list(map(parse_article, article_paths)), key=lambda x: x.date)


def build_card(article):
  tags = BeautifulSoup('', 'html.parser')
  for i, tag in enumerate(article.tags):
    soup = BeautifulSoup(f'<li><a href="#">{tag}</a></li>', 'html.parser')
    tags.insert(i, soup)

  card = ARTICLE_CARD.format(title=article.title, tags=tags.prettify(),
      date=article.date.strftime('%Y-%m-%d'), readable_date=article.date.strftime('%B %d, %Y'),
      summary=article.summary.prettify(), article_link=article.path)
  return BeautifulSoup(card, 'html.parser')


def build_cards(articles):
  built = BeautifulSoup('<div class="container"></div>', 'html.parser')
  container = built.contents[0]

  for i, article in enumerate(articles):
    container.insert(i, build_card(article))

  return built


def write(html, file_path):
  with open(f'{TEMPLATES_DIR}/head.html', 'r') as f:
    head = f.read()

  with open(f'{TEMPLATES_DIR}/tail.html', 'r') as f:
    tail = f.read()

  full_html = BeautifulSoup(head + html + tail, 'html.parser')
  with open(file_path, 'w') as f:
    f.write(full_html.prettify())


def build_tag_page(tag, articles):
  cards = build_cards(articles)
  container = cards.find('div', attrs={'class': 'container'})
  tag_heading = BeautifulSoup(f'<h2 class="tag mt-4">Tag: {tag}</h2>', 'html.parser')
  container.insert(0, tag_heading)
  write(cards.prettify(), f'{SRC_DIR}/tag/{tag.lower()}.html')


def build_tags_pages(articles):
  all_tags = {}
  for article in articles:
    for tag in article.tags:
      all_tags.setdefault(tag.lower(), ([], []))
      all_tags[tag.lower()][0].append(tag)
      all_tags[tag.lower()][1].append(article)

  for tag, (representations, articles) in all_tags.items():
    if len(set(representations)) > 1:
      print("WARNING: There are multiple representations for tag {}: {}".format(tag, ", ".join(representations)))

    build_tag_page(representations[0], articles)

  lower_tags = list(all_tags.keys())
  lower_tags.sort(key=lambda x: len(all_tags[x][1]))

  tags = BeautifulSoup('', 'html.parser')
  for i, tag in enumerate(lower_tags):
    rep = all_tags[tag][0][0]
    count = len(all_tags[tag][1])
    soup = BeautifulSoup(f'<li><a href="/tag/{tag}.html">{rep} ({count})</a></li>', 'html.parser')
    tags.insert(i, soup)

  write(TAGS_PAGE.format(tags=tags.prettify()), f'{SRC_DIR}/tags.html')


def build_home_page(articles):
  cards = build_cards(articles)
  first_card = cards.find('div', attrs={'class': 'card'})
  first_card.attrs['class'].append('mt-4')
  write(cards.prettify(), f'{SRC_DIR}/index.html')


def update_dates_in_articles(articles):
  for article in articles:
    article_file_name = article.path.split('/')[-1]
    article_file_path = f'{SRC_DIR}/articles/{article_file_name}'

    with open(article_file_path, 'r') as f:
      soup = BeautifulSoup(f.read(), 'html.parser')

    for date_tag in soup.find_all('time'):
      date_str = date_tag.attrs.get('datetime', '')
      assert(date_str)
      year, month, day = map(int, date_str.split('-'))
      date = datetime.date(year, month, day)

      date_tag.clear()
      date_tag.insert(0, date.strftime('%B %d, %Y'))

    with open(article_file_path, 'w') as f:
      f.write(soup.prettify())


def main():
  articles = read_articles()
  build_home_page(articles)
  build_tags_pages(articles)
  update_dates_in_articles(articles)


if __name__ == '__main__':
  main()

