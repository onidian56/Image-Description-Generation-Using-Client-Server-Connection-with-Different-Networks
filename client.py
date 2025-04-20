import smtplib
import os
from email.message import EmailMessage
from email.parser import BytesParser
from datetime import datetime
from PIL import Image, ImageDraw
import poplib
import cv2


def create_image(image_path):
    image = Image.new('RGB', (100, 100), color='blue')
    draw = ImageDraw.Draw(image)
    draw.text((10, 40), "Test Image", fill='white')
    image.save(image_path)


def send_email(subject, body, to_email, from_email, password, image_path=None):
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(body)

    # Attach the image
    if image_path:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            img_name = os.path.basename(image_path)
            msg.add_attachment(img_data, maintype='image', subtype='png', filename=img_name)

    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)
    print("Image is sent successfully to server.")




def receive_email(username, password, save_dir, subject_filter=None):
    # Connect to the server
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user(username)
    pop_conn.pass_(password)

    message_count = len(pop_conn.list()[1])

    if message_count > 0:
        for i in range(message_count):
            # Retrieve each message
            response, lines, octets = pop_conn.retr(i + 1)

            # Join the lines and parse the email
            message_bytes = b'\r\n'.join(lines)
            message = BytesParser().parsebytes(message_bytes)

            # Filter based on subject if needed
            if subject_filter and subject_filter.lower() not in message['subject'].lower():
                continue

            # Check if the email is multipart
            if message.is_multipart():
                for part in message.get_payload():
                    if part.get_content_type() == 'text/plain' and not part.get_content_disposition():
                        # Decode and print the text content
                        text_content = part.get_payload(decode=True).decode(part.get_content_charset())
                        print("Generated Description from server:")
                        print(text_content)
                        return 'stop'
            else:
                if message.get_content_type() == 'text/plain':
                    text_content = message.get_payload(decode=True).decode(message.get_content_charset())
                    print("Generated Description from server:")
                    print(text_content)
                    return 'stop'


    # Quit the connection
    pop_conn.quit()



if __name__ == "__main__":
    sender_email = "rpi2pc@gmail.com"
    receiver_email = "sender2receiver24@gmail.com"
    app_password = "eiyu ulww ysxx mkzv"

    while True:
        input("Press Enter to send a new image to server...")

        # image_path = f"./img1.png"
        img=cv2.VideoCapture(0)
        ret, frame = img.read()

        cv2.imshow("Captured Image", frame)
        cv2.imwrite("./captured_image.jpg", frame)
        print('Image is captured successfully.')

        # Send email with the image
        send_email(
            subject=f"Query from Client- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            body="Please find the attached image.",
            to_email=receiver_email,
            from_email=sender_email,
            password=app_password,
            image_path='./captured_image.jpg'
        )

        # Print the server response (Generated Image)
        print('Waiting for server response...')
        while(True):
            val=receive_email("rpi2pc@gmail.com","eiyu ulww ysxx mkzv","./")
            if val=='stop':
                break







