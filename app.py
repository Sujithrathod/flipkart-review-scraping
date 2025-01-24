from flask import Flask,request,jsonify,render_template
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/review",methods=["POST"])
def reviews():
    if (request.method == "POST"):
        try:
            content = request.form["input"].replace(" ","")
            iphone_url = "https://www.flipkart.com/search?q=" +content
            uclient = requests.get(iphone_url,"html.parser")
            flipkart_bs = bs(uclient.text,"html.parser")
            bigbox = flipkart_bs.findAll("div",{"class":"cPHDOP col-12-12"})
            del bigbox[0:3]
            last = bigbox[0].div.div.a["href"]
            link = "https://www.flipkart.com"+last
            productreq = requests.get(link)
            phone_page = productreq.text
            phone_page_bs = bs(phone_page,"html.parser")
            review_box = phone_page_bs.findAll("div",{"class":"col EPCmJX"})
            print(len(review_box))
            reviews = []
            
            for i in review_box:
                try:
                    name = i.findAll("div",{"class":"row gHqwa8"})[0].div.p.text
                except:
                    name = "no name"
                    
                try:
                    rating = i.div.div.text
                except:
                    rating = "Np rating"
                    
                try:
                    commentHead = i.div.text
                except:
                    commentHead = "no comment head"
                
                try:
                    ch =i.findAll("div",{"class":"row"})
                    comment = ch[1].div.div.div.text
                except:
                    comment = "no comment"
                
                mydict = {"Product": content, "Name": name, "Rating": rating, "CommentHead": commentHead,
                            "Comment": comment}
                reviews.append(mydict)
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    else:
        return render_template('index.html')

if(__name__ == "__main__"):
    app.run(host="127.0.0.1",port=5000)
    