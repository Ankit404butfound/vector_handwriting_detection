import tkinter as tk
import numpy as np
import psycopg2
from PIL import Image, ImageTk, ImageDraw

conn = psycopg2.connect("postgresql://user:password@database-1.*************.rds.amazonaws.com:5432/database")
cur = conn.cursor()

def get_canvas_data(canvas):
    # Create a blank image with white background
    image = Image.new("L", (256, 256), color=255)
    draw = ImageDraw.Draw(image)
    
    # Iterate through all objects on the canvas
    for item in canvas.find_all():
        # Get the coordinates of the current object
        x1, y1, x2, y2 = canvas.coords(item)
        # Draw the object on the image
        draw.ellipse([x1-2, y1-2, x2+2, y2+2], fill=0)

    # Convert to NumPy array
    # Resizing the image to 64x64
    image = image.resize((64, 64))
    # image.show()
    canvas_array = np.array(image)
    return canvas_array.flatten()

def save_data():
    # Get the canvas data
    canvas_data = get_canvas_data(canvas)
    print(len(canvas_data))
    # Clear canvas
    canvas.delete("all")
    # Get the value from the input box
    input_value = input_box.get()
    # Print the canvas data and input box value
    cur.execute(f"INSERT INTO datasets (value, embedding) VALUES ('{input_value}', '{canvas_data.tolist()}')")
    conn.commit()


def predict():
    # Get the canvas data
    canvas_data = get_canvas_data(canvas)
    print(len(canvas_data))
    # Print the canvas data and input box value
    # canvas.delete("all")
    cur.execute(f"SELECT value FROM datasets ORDER BY embedding <-> '{canvas_data.tolist()}' LIMIT 5")
    value = cur.fetchall()
    print(value)
    # Set the input box value
    input_box.delete(0, "end")
    input_box.insert(0, value[0][0])
    
    

def draw(event):
    x, y = event.x, event.y
    canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")

# Create main window
root = tk.Tk()
root.title("Canvas Drawing Example")

# Create canvas
canvas = tk.Canvas(root, width=256, height=256, bg="white")
canvas.pack()

# Bind left-click event to draw function
canvas.bind("<B1-Motion>", draw)

# Input box
input_box = tk.Entry(root)
input_box.pack()

# Button
# button = tk.Button(root, text="Save Data", command=save_data)
# button.pack()

button = tk.Button(root, text="Predict", command=predict)
button.pack()

button = tk.Button(root, text="Clear", command=lambda: canvas.delete("all"))
button.pack()


# Run the Tkinter event loop
root.mainloop()
