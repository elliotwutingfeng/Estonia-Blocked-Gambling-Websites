# Estonia Blocked Gambling Websites

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

[![GitHub license](https://img.shields.io/badge/LICENSE-BSD--3--CLAUSE-GREEN?style=for-the-badge)](LICENSE)
[![scraper](https://img.shields.io/github/actions/workflow/status/elliotwutingfeng/Estonia-Blocked-Gambling-Websites/scraper.yml?branch=main&label=SCRAPER&style=for-the-badge)](https://github.com/elliotwutingfeng/Estonia-Blocked-Gambling-Websites/actions/workflows/scraper.yml)
<img src="https://tokei-rs.onrender.com/b1/github/elliotwutingfeng/Estonia-Blocked-Gambling-Websites?label=Total%20Blocklist%20URLS&style=for-the-badge" alt="Total Blocklist URLs"/>

The Estonian Tax and Customs Board blocks access to the [websites of gambling operators](https://www.emta.ee/ariklient/registreerimine-ettevotlus/hasartmangukorraldajale/blokeeritud-hasartmangu) whose services are available in Estonia but who do not have the required activity and organization license to operate in Estonia.

This repository provides the URLs of these websites as a machine-readable `.txt` blocklist compatible with firewall applications like [Pi-hole](https://pi-hole.net) and [pfBlockerNG](https://docs.netgate.com/pfsense/en/latest/packages/pfblocker.html).

The URLs in this blocklist are compiled by the **Estonian Tax and Customs Board**.

**Disclaimer:** _This project is not sponsored, endorsed, or otherwise affiliated with the Estonian Tax and Customs Board._

## Blocklist download

| File | Download |
|:-:|:-:|
| blocklist.txt | [:floppy_disk:](blocklist.txt?raw=true) |
| blocklist_ABP.txt | [:floppy_disk:](blocklist_ABP.txt?raw=true) |
| blocklist_UBO.txt | [:floppy_disk:](blocklist_UBO.txt?raw=true) |
| blocklist_UBL.txt | [:floppy_disk:](blocklist_UBL.txt?raw=true) |

## Requirements

-   Python 3.9

## Setup instructions

`git clone` and `cd` into the project directory, then run the following

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 scraper.py
```

&nbsp;

<sup>These files are provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, arising from, out of or in connection with the files or the use of the files.</sup>

<sub>Any and all trademarks are the property of their respective owners.</sub>
