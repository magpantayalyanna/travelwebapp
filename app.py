from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load resorts data
with open('resorts.json', encoding='utf-8') as f:
    resort_data = json.load(f)

BOOKING_FILE = os.path.join(os.path.dirname(__file__), 'bookingDetails.json')

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_city = None
    selected_resort = None
    resort_info = None
    message = None

    name = ''
    contact = ''
    date = ''

    if request.method == 'POST':
        action = request.form.get('action')
        selected_city = request.form.get('city')
        selected_resort = request.form.get('resort')
        name = request.form.get('name', '')
        contact = request.form.get('contact', '')
        date = request.form.get('date', '')

        if action == 'Book Now':
            if all([name, contact, date, selected_city, selected_resort]):
                resort_info = resort_data[selected_city][selected_resort]

                booking = {
                    "name": name,
                    "contact": contact,
                    "date": date,
                    "place": selected_city,
                    "resort": selected_resort,
                    "description": resort_info["desc"],
                    "price": resort_info["price"]
                }

                try:
                    if os.path.exists(BOOKING_FILE):
                        with open(BOOKING_FILE, 'r', encoding='utf-8') as f:
                            bookings = json.load(f)
                    else:
                        bookings = []
                except:
                    bookings = []

                bookings.append(booking)

                try:
                    with open(BOOKING_FILE, 'w', encoding='utf-8') as f:
                        json.dump(bookings, f, indent=4, ensure_ascii=False)
                    message = f"Thank you, {name}! Your booking for {selected_resort} on {date} has been received! 🌴"
                    name = ''
                    contact = ''
                    date = ''
                except:
                    message = "Sorry, there was a problem saving your booking."

            else:
                message = "Please fill out all fields before booking."

        elif selected_city and selected_resort:
            resort_info = resort_data[selected_city][selected_resort]

    return render_template(
        'index.html',
        cities=resort_data,
        selected_city=selected_city,
        selected_resort=selected_resort,
        resort_info=resort_info,
        message=message,
        name=name,
        contact=contact,
        date=date
    )

if __name__ == '__main__':
    app.run(debug=True)
