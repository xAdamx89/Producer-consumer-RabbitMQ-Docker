from flask import Flask, render_template
import pika
import threading

app = Flask(__name__)

messages = []

credentials = pika.PlainCredentials('myuser', 'mypassword')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='produkty')

def  start_consumer():

    def callback(ch, method, properties, body):
        message = body.decode()
        print("[x] Received:", message)

        # Liczymy litery (case-insensitive)
        counts = {}
        for c in message.lower():
            if c.isalpha():  # ignorujemy cyfry, spacje i znaki specjalne
                counts[c] = counts.get(c, 0) + 1

        # Tworzymy string w formacie: r=1, a=1, b=2,...
        letter_count_str = ", ".join(f"{k}={v}" for k, v in counts.items())
        print(f"{message} {letter_count_str}")

        # Zachowujemy do listy do wyświetlenia w Flask
        messages.append(f"{message} → {letter_count_str}")
        if len(messages) > 10:
            messages.pop(0)

    channel.basic_consume(queue='produkty',
                          on_message_callback=callback,
                          auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()



threading.Thread(target=start_consumer, daemon=True).start()

@app.route("/", methods=['GET'])
def  index():
    return render_template("index.html", messages=messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=False)

