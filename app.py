from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET']) #route display home
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) #route display home
@cross_origin()
def index():
    if request.method == "POST":
        try:
            searchString =request.form['content'].replace(" "," ")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html=bs(flipkartPage,"html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(product_link)
            prodRes.encoding = 'utf8'
            prod_html = bs(prodRes.text, 'html.parser')
            print(prod_html)
            commentboxes = prod_html('div', {'class': "_16PBlm"})
            Filename = searchString + ".csv"
            fw = open(Filename, 'w')
            headers = 'Product, Customer, Name, Rating, Heading, Comment \n'
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    name=commentbox.div.div.find_all('p',{'class':'_2sc7ZR _2V5EHH'})[0].text
                except:
                    name='No Name'

                try:
                    rating=commentbox.div.div.div.div.text
                except:
                    rating = 'No rating'

                try:
                    commentHead=commentbox.div.div.div.p.text
                except:
                    commentHead= 'No Comment Head'

                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ", e)
                mydict={'Product':searchString,'Name':name,'Rating':rating,'CommentHead':commentHead,'Comment':custComment}
                reviews.append(mydict)
            return render_template("results.html",reviews=reviews[0:len(reviews)-1])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return render_template('index.html')




if __name__== '__main__':
    app.run(host='127.0.0.1',port=8001, debug=True)
    #app.run(debug=True)

