from flask import Flask, render_template
import pika
import threading

app = Flask(__name__)

messages = []

def  start_consumer():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='produkty')

    def callback(ch, method, properties, body):
        message = body.decode()
        print("[x] Received:", message)
        messages.append(message)
        if len(messages) > 10:
            messages.pop(0)

    channel.basic_consume(queue='produkty',
                          auto_ack=True,
                          on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()



threading.Thread(target=start_consumer, daemon=True).start()

@app.route("/", methods=['GET'])
def  index():
    return render_template("index.html", messages=messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=False)

