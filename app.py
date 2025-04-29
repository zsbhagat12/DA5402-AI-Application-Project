from flask import Flask, render_template, request, jsonify
# from prediction_service import prediction
import os

# webapp_root = "webapp"

static_dir = os.path.join("static")
template_dir = os.path.join("templates")

app = Flask(__name__, static_folder=static_dir,template_folder=template_dir)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        try:
            if request.form:    #if request is coming from the webapp
                dict_req = dict(request.form)
                response = prediction.form_response(dict_req)
                return render_template("index.html", response=response)
            
            elif request.json:  #if request is from any api testing app (postman)
                response = prediction.api_response(request.json)
                return jsonify(response)

        except Exception as e:
            print(e)
            error = {error:e}
            return render_template("404.html", error=error)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)