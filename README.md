# FHUI Scraper

Scrapes article metadata from all 13 journals under the Universitas Indonesia Faculty of Law on Digital Commons (bepress/Elsevier).

## Journals

| Code | Name |
|------|------|
| dharmasisya | Dharmasisya FHUI |
| iclr | Indonesia Criminal Law Review |
| ilrev | Indonesia Law Review |
| ijel | Indonesian Journal of Environmental Law |
| ijil | Indonesian Journal of International Law |
| notary | Indonesian Notary |
| jils | Journal of Islamic Law Studies |
| jpils | Journal of Private International Law Studies |
| jhp | Jurnal Hukum & Pembangunan |
| jurnalkonsdem | Jurnal Konstitusi & Demokrasi |
| lexpatri | Lex Patrimonium |
| telj | Technology and Economics Law Journal |
| ijsls | The Indonesian Journal of Socio-Legal Studies |

## Usage

```bash
# All journals
scrapy crawl faculty_law -o articles.json

# Single journal
scrapy crawl faculty_law -a journal_codes=ijil -o ijil.json

# Multiple journals
scrapy crawl faculty_law -a journal_codes=ijil,ilrev -o subset.json

# Test (limit article per issue)
scrapy crawl faculty_law -a journal_codes=ijil -a max_articles=2 -o test.json
```

## Output

JSON Lines — one object per article with fields:

`title`, `authors`, `institutions`, `volume`, `issue`, `year`, `doi`, `abstract`, `keywords`, `pdf_url`, `article_url`, `journal`, `journal_code`, `journal_url`, `issn`, `online_date`, `article_id`, `issue_url`

## Caching

HTTP cache is enabled (24h TTL). Cached pages stored in `httpcache/`. To bypass:

```bash
scrapy crawl faculty_law -s HTTPCACHE_ENABLED=False -o fresh.json
```
