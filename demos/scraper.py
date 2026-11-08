from bs4 import BeautifulSoup as BS
def main():
    with open("page_code.html", "r") as f:
        html = f.read()
    soup = BS(html, "html.parser") # pass it the content
    panel = soup.select_one(".newsLineupContainer-qVPFg") # select the first div with class panel
    new_element = panel.select('span')
    print(len(new_element))
    for e in new_element:
        print(e.text)


if __name__ == "__main__":
    main()
    
    
    
    