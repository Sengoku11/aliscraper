import requests
from bs4 import BeautifulSoup


class AliPage:
    def __init__(self, URL):
        self.URL = URL

        error = self.validation()
        if error:
            self.title = None
            self.price = None
            self.sale = None

        else:
            self.format_url()
            self.get_soup()
            self.title = self.get_title()
            self.price, self.sale = self.get_price()
            self.print_product()

    def __str__(self):
        return str(self.title)

    def format_url(self):
        if "//m." in self.URL:
            self.URL = self.URL.replace("//m.", "//")
        
        if "//www.aliexpress.com" in self.URL:
            self.URL = self.URL.replace("//www.aliexpress.com", "//ru.aliexpress.com")

    def validation(self):
        if 'aliexpress.com/' not in self.URL:
            print('wrong URL -- ', self.URL)
            return True
        return False

    def get_soup(self):
        page = requests.get(self.URL)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        self.soup = BeautifulSoup(self.soup.prettify(), 'html.parser')

    def get_title(self):
        self.title = self.soup.find("title").get_text().strip()
        return self.title

    def get_price(self):
        # Price is hidden in <script>
        scripts_list = self.soup.find_all('script')
        # To search the price concatinate all <scripts> into one string
        scripts_string = ''
        for i in scripts_list:
            scripts_string += str(i)

        # Now check if there is SALE'S price
        if scripts_string.find('formatedActivityPrice') != -1:

            price_index = scripts_string.find('formatedActivityPrice')

            # Get and clean price
            # Code below is true for scraping from Russian IP
            self.price = int(scripts_string[price_index:price_index +
                                            100].split("\":\"")[1].split(",")[0].replace('\xa0', ''))

            return self.price, True

        elif scripts_string.find('formatedPrice') != -1:

            price_index = scripts_string.find('formatedPrice')

            # Get and clean price. Code below is true for scraping from Russian IP
            self.price = int(scripts_string[price_index:price_index +
                                            100].split("\":\"")[1].split(",")[0].replace('\xa0', ''))

            return self.price, False

        # If there is no price in <script> then -> link was from TMALL. Price there stores in html id=""
        else:
            # Check for SALE'S price
            if self.soup.find(id="j-sku-discount-price") != None:
                self.price = int(
                    self.soup.find(id="j-sku-discount-price").get_text().strip().replace('\xa0', ''))

                return self.price, True

            else:
                self.price = int(
                    self.soup.find(id="j-sku-price").get_text().strip().replace('\xa0', ''))

                return self.price, False

    def print_product(self):
        print("\n\nProduct name: {title}".format(title=self.title))

        if self.sale:
            print("Price: {price} roubles. SALE!".format(price=self.price))
        else:
            print("Price: {price} roubles.".format(price=self.price))

        self.wanted_price = 200
        print("You want for {wanted_price} roubles.".format(
            wanted_price=self.wanted_price))

        if(self.price > self.wanted_price):
            print('match!\n\n')


# test_obj = AliPage('https://www.aliexpress.com/item/32231073816.html?spm=a2g01.12602323.fdpcl001.1.3446753f4nXa4c&gps-id=5589723&scm=1007.23880.125255.0&scm_id=1007.23880.125255.0&scm-url=1007.23880.125255.0&pvid=7453c2f')
# print(test_obj)

# test_obj = AliPage('https://m.ru.aliexpress.com/item/32682406509.html?trace=wwwdetail2mobilesitedetail&scm=1007.23534.123999.0&pvid=352e7150-ed71-4654-9adc-bc12982a1af1&rmsg=do_not_replacement&dp=13d5ddafb1ec2a960c6ac888f8a87eba&af=496392&cv=47843&afref=&mall_affr=pr3&aff_platform=aaf&cpt=1569181332466&sk=VnYZvQVf&aff_trace_key=145a7c50a025486a891ab33265a1e978-1569181332466-05972-VnYZvQVf&terminal_id=9b0b835d653e4f43bab42b6100a23477')
# print(test_obj)
