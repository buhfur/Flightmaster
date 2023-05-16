import scrapy


class GithubLinkSpider(scrapy.Spider):
    name = "github-links"
    start_urls = [
        "https://legacy-wow.com/vanilla-addons/",
    ]

    def parse(self, response):
        for quote in response.css("div.AddonTitleDesc"):
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
            }

        next_page = response.css('li.next a::attr("href")').get() # grabs hrefs from the page ? 
        if next_page is not None:
            print(next_page) # hopefully prints out the page 
            #yield response.follow(next_page, self.parse) # follows the link to the next page? 

