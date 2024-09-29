import scrapy

class NomeDaClasseSpider(scrapy.Spider):
    
    name = 'coletardados'
    
    def start_requests(self):
        urls = ['https://www.goodreads.com/quotes?page=1']
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
            
    def parse(self,response):
        for elemento in response.xpath("//div[@class='quoteDetails']"):
            yield {
                'citacao': elemento.xpath(".//div[@class='quoteText']/text()").get(),
                'autor': elemento.xpath(".//span[@class='authorOrTitle']/text()").get(),
                'tags': elemento.xpath(".//div[@class='greyText smallText left']/a/text()").getall()
            }
        try:
            numero_proxima_pagina = response.xpath("//a[@class='next_page']/@href").get().split('=')[1]
            print('#'*20)
            print(numero_proxima_pagina)
            print('#'*20)
            if numero_proxima_pagina is not None:
                link_proxima_pagina = f'https://www.goodreads.com/quotes?page={numero_proxima_pagina}'
                print('#'*20)
                print(link_proxima_pagina)
                print('#'*20)
                yield scrapy.Request(url=link_proxima_pagina, callback=self.parse)
        except:
            print('Chegamos na ultima página')