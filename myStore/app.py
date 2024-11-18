from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

# Define the items available in the store
items = [
    {
        'id': 1,
        'name': 'Hylle 1x1',
        'Size': '1x1',
        'price': "349.90,-",
        'image': 'image1.png'
    },
    {
        'id': 2,
        'name': 'Hylle 1x2',
        'Size': '1x2',
        'price': "379.90,-",
        'image': 'image2.png'
    },
    {
        'id': 3,
        'name': 'Hylle 1x3',
        'Size': '1x3',
        'price': "399.90,-",
        'image': 'image4.png'
    },
    {
        'id': 4,
        'name': 'Hylle 2x2',
        'Size': '2x2',
        'price': "499.90,-",
        'image': 'image3.png'
    },
    {
        'id': 5,
        'name': 'Hylle 2x3',
        'Size': '2x3',
        'price': "599.90,-",
        'image': 'image5.png'
    },
    {
        'id': 6,
        'name': 'Hylle 3x3',
        'Size': '3x3',
        'price': "799.90,-",
        'image': 'image6.png'
    },
]

# Route for the homepage displaying items
@app.route('/')
def index():
    return render_template('index.html', items=items)

# Route to add an item to the cart
@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    # Retrieve the selected item
    selected_item = next((item for item in items if item['id'] == item_id), None)
    if selected_item:
        return render_template('cart.html', item=selected_item)
    else:
        return "Item not found", 404

# Route to handle the checkout process
@app.route('/checkout', methods=['POST'])
def checkout():
    itemSize = request.form.get('item_Size')
    selected_item = next((item for item in items if item['Size'] == itemSize), None)
    if not selected_item:
        return "Item not found", 404
    Size = str(itemSize)
    # Call the external Python script with the NxN variable
    subprocess.run(['python', 'process_order.py', Size])
    return render_template('confirmation.html', variable=Size)

if __name__ == '__main__':
    app.run(debug=True)
