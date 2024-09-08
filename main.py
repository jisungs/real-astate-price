from flask import Flask, render_template, request, redirect,url_for

from get_real_price import sigungu_code , search_apt_price


app = Flask(__name__)

@app.route('/', methods = ["GET","POST"])
def index():
    if request.method == "POST":
        data = request.form.to_dict()
        main_addr = data['address'].split()
        if main_addr:        
            code = sigungu_code(main_addr)
            result = search_apt_price('아파트',code,'202401','202408')
            
            table_html = result.to_html(classes='table table-striped', index=False)

            return render_template('index.html', table_html=table_html)


        

    return render_template("index.html")


if __name__=='__main__':
    app.run(debug=True, port=5002)