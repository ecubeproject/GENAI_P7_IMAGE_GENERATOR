from tkinter import *
from PIL import Image, ImageTk
import io
import requests
from openai import OpenAI
import config
import logging
import httpx

# Initialize the OpenAI client
client = OpenAI(api_key=config.API_KEY, timeout=httpx.Timeout(120, read=120, write=20.0, connect=10.0))

logging.basicConfig(level=logging.DEBUG)


def generate_and_display_image():
    user_prompt = text_input.get("1.0", "end-1c")  # Get user input from the textbox
    response = client.images.generate(
        model="dall-e-3",
        prompt=user_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    image_response = requests.get(image_url)
    image_data = Image.open(io.BytesIO(image_response.content))
    image_data.thumbnail((500, 500))  # Resize the image to fit the display area
    img = ImageTk.PhotoImage(image_data)

    # Display the image
    image_label.configure(image=img)
    image_label.image = img  # Keep a reference so it's not garbage collected


# Set up the GUI
root = Tk()
root.title("DALL-E Image Generator")

# Create a textbox for user input
text_input = Text(root, height=10, width=50)
text_input.pack(side=LEFT, fill=BOTH, expand=True)

# Create a frame on the right to hold the image and button
right_frame = Frame(root)
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

# Button to generate the image
generate_button = Button(right_frame, text="Generate Image", command=generate_and_display_image)
generate_button.pack(pady=20)

# Label to display the image
image_label = Label(right_frame)
image_label.pack(pady=20)

root.mainloop()
