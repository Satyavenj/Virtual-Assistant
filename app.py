from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"   # Required for session management


# ---------- INDEX (Redirect to Login) ----------
@app.route("/")
def index():
    return redirect(url_for("login"))


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            error = "⚠️ Please enter a username."
        else:
            session["username"] = username
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


# ---------- HOME ----------
@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", username=session["username"])

# ---------- ASSISTANT ----------

@app.route("/assistant", methods=["GET", "POST"])
def assistant():
    if "username" not in session:
        return redirect(url_for("login"))

    reply = None
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if message:
            if message.lower() == "hi":
                reply = "Hello Reethika! 👋 How can I help you today?"
            elif message.lower() == "how are you":
                reply = "I am doing great! Thanks for asking 🌸"
            else:
                reply = f"You said: {message}"

    return render_template("assistant.html", username=session["username"], reply=reply)



# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(debug=True)
