from flask import Flask, render_template, request, redirect, url_for
import pika

app = Flask(__name__)

credentials = pika.PlainCredentials('myuser', 'mypassword')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='produkty')

@app.route("/")
def  index():
    return render_template("index.html", arg="To jest argument producenta")

@app.route("/send", methods=["POST"])
@app.route("/send", methods=["POST"])
def send():
    produkt = request.form.get("produkt")
    if not produkt:
        return redirect("/")

    # Tworzymy nowe połączenie i kanał tylko do wysyłki
    credentials = pika.PlainCredentials('myuser', 'mypassword')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='produkty', durable=True)  # upewnij się, że kolejka istnieje

    channel.basic_publish(exchange='',
                          routing_key='produkty',
                          body=produkt)
    connection.close()

    return redirect("/")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)