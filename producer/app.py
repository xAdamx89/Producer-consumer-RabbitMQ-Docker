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
def send():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='produkty')
    produkt = request.form.get('produkt')
    if not produkt or produkt.strip() == "":
        print("Wartość produkt jest pusta")
        return redirect(url_for('index'))
    
    channel.basic_publish(exchange='',
                      routing_key='produkty',
                      body=produkt)
    connection.close()

    print("Wysłano do RabbitMQ: ", produkt)
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)