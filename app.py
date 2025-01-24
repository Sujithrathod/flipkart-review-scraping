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
        # try:
            content = request.form["input"].replace(" ","")
            iphone_url = "https://www.flipkart.com/search?q=" +content
            uclient = requests.get(iphone_url,"html.parser")
            flipkart_bs = bs(uclient.text,"html.parser")
            bigbox = flipkart_bs.findAll("div",{"class":"cPHDOP col-12-12"})
            if (len(bigbox) > 2):
                del bigbox[0:2]
            if not bigbox:
                return "No products found."
            reviews_with_index = []
            for j in range(0,len(bigbox)):
                try:
        # Validate structure before accessing
                    if bigbox[j].div and bigbox[j].div.div and bigbox[j].div.div.a:
                        last = bigbox[j].div.div.a["href"]
                    else:
                        print(f"Skipping item at index {j}: Structure does not match.")
                        continue
                except AttributeError as e:
                    print(f"AttributeError at index {j}: {e}")
                    continue
                link = "https://www.flipkart.com"+last
                productreq = requests.get(link)
                phone_page = productreq.text
                phone_page_bs = bs(phone_page,"html.parser")
                review_box = phone_page_bs.findAll("div",{"class":"col EPCmJX"})
                print(len(review_box))
                product_list = phone_page_bs.findAll("div",{"class":"C7fEHH"})
                if product_list:
                    product = product_list[0].div.text
                else:
                    product = "Unknown product"
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
                    
                    mydict = {"Product": content, "Name": name, "Rating": rating, "CommentHead": commentHead[1:],
                                "Comment": comment}
                    if mydict["Name"] == "" or mydict["Rating"] == "" or mydict["Comment"] == "":
                        continue
                    reviews.append(mydict)
                print(reviews)
                reviews_with_index.append({"j": product, "reviews": reviews})
                review_box = []
                print(reviews_with_index)
            return render_template('result.html', reviews_with_index=reviews_with_index)
        # except Exception as e:
        #     print('The Exception message is: ',e)
        #     return 'something is wrong'
    else:
        return render_template('index.html')

if(__name__ == "__main__"):
    app.run(host="127.0.0.1",port=5000)
    