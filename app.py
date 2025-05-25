from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)
app.secret_key = 'secret-key'

# Load resorts data once at startup
with open('resorts.json', encoding='utf-8') as f:
    resorts_data = json.load(f)

BOOKINGS_FILE = 'bookingsDetails.json'

def save_booking(data):
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            try:
                bookings = json.load(f)
            except json.JSONDecodeError:
                bookings = []
    else:
        bookings = []

    bookings.append(data)

    with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(bookings, f, indent=4, ensure_ascii=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    name = contact = date = ''
    selected_city = None
    selected_resort = None
    resort_info = None
    message = None

    if request.method == 'POST':
        name = request.form.get('name', '')
        contact = request.form.get('contact', '')
        date = request.form.get('date', '')
        selected_city = request.form.get('city', None)
        selected_resort = request.form.get('resort', None)
        action = request.form.get('action', None)

        if action == 'Book Now':
            if not all([name, contact, date, selected_city, selected_resort]):
                message = "Please fill out all fields to book."
            else:
                booking_data = {
                    "name": name,
                    "contact": contact,
                    "date": date,
                    "city": selected_city,
                    "resort": selected_resort,
                    "resort_desc": resorts_data[selected_city][selected_resort]['desc'],
                    "resort_price": resorts_data[selected_city][selected_resort]['price']
                }
                save_booking(booking_data)
                message = f"Thank you {name}, your booking for {selected_resort} in {selected_city} on {date} has been received!"

        if selected_city and selected_resort:
            resort_info = resorts_data[selected_city][selected_resort]

    cities = list(resorts_data.keys())

    return render_template('index.html',
                           name=name,
                           contact=contact,
                           date=date,
                           cities=cities,
                           resorts=resorts_data,
                           selected_city=selected_city,
                           selected_resort=selected_resort,
                           resort_info=resort_info,
                           message=message)


if __name__ == '__main__':
    app.run(debug=True)
