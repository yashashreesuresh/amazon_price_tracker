import os
import re
import ssl
import smtplib
import scrapy


class TrackerSpider(scrapy.Spider):
    name = 'tracker'
    allowed_domains = ['www.amazon.in']
    start_urls = ['https://www.amazon.in/New-Apple-iPhone-Pro-256GB/dp/B08L5T2XSF']
   
    def clean_text(self, text):
        if text:
            return re.sub(r"\s+", "", text, flags=re.UNICODE)
        
    
    def retrieve_price(self, text):
        if text:
            text = text.split(".")[0]
            return re.sub("[^0-9]", "", text)

    
    def send_email(self, MRP, discounted_price, discount_amount, discount_percentage):
        subject = "Price Drop!"
        body = f"Price has fallen down.\n\nMRP: {MRP}\nDiscounted Price: {discounted_price}\n" \
            f"Discount Amount: {discount_amount}\nDiscount Percentage: {discount_percentage}%\n" \
            f"Check this amazon link: {self.start_urls[0]}"
        message = f"Subject: {subject}\n\n{body}"

        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        server.login(os.environ.get("sender_email"), os.environ.get("password"))
        server.sendmail(os.environ.get("sender_email"), os.environ.get("receiver_email"), message.encode('utf-8'))
        print("Mail sent")


    def parse(self, response):
        stock_unavailable = self.clean_text(response.xpath("//span[@class='a-size-medium a-color-price']/text()").get())
        MRP = self.clean_text(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").get())
        discounted_price = self.clean_text(response.xpath("//span[@id='priceblock_ourprice']/text()").get())
        discount = self.clean_text(response.xpath("//td[@class='a-span12 a-color-price a-size-base priceBlockSavingsString']/text()").get())

        if stock_unavailable:
            yield {
                "stock_availability": "Currently product unavailable",
            }
        else:
            if not discount:
                yield {
                    "stock_availability": "In Stock",
                    "MRP": discounted_price,
                    "discount_percentage": "No discount"
                }
            else:
                discount_amount = self.retrieve_price(discount.split("(")[0])
                discount_percentage = self.retrieve_price(discount.split("(")[1])
                yield {
                    "stock_availability": "In Stock",
                    "MRP": MRP,
                    "discounted_price": discounted_price,
                    "discount_amount": discount_amount,
                    "discount_percentage": discount_percentage
                }
                if int(discount_percentage) >= 0:
                    self.send_email(MRP, discounted_price, discount_amount, discount_percentage)
                