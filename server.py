import poplib
from email.parser import BytesParser
from email.policy import default
import os
from classifyAnimalImage import *
from email.message import EmailMessage
import smtplib

def send_email(subject, to_email, from_email, password, response):
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(response)

    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)

    print("Generated description is sent successfully to client.")


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

            message_bytes = b'\r\n'.join(lines)
            message = BytesParser(policy=default).parsebytes(message_bytes)

            # Filter based on subject if needed
            if subject_filter and subject_filter.lower() not in message['subject'].lower():
                continue

            # Iterate over email parts
            found_image = False
            for part in message.iter_parts():
                if part.get_content_maintype() == 'multipart':
                    continue

                if part.get_content_disposition() == 'attachment' and part.get_content_maintype() == 'image':
                    found_image = True
                    # Get the image content
                    img_data = part.get_payload(decode=True)
                    filename = part.get_filename()
                    file_path = os.path.join(save_dir, filename)

                    # Ensure the directory exists
                    os.makedirs(save_dir, exist_ok=True)

                    # Save the image file
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
                    # print(f'Image saved as {file_path}')
                    
            if found_image:
                print("Image is received from client")
                pred=classify_animal_image(file_path)
                print(pred)
                send_email('Response','rpi2pc@gmail.com','sender2receiver24@gmail.com','lexu gfpk jcih xzww',str(pred))
                break

        if not found_image:
            print("No image attachment found.")

    # Quit the connection
    pop_conn.quit()


username = "sender2receiver24@gmail.com"
password = "lexu gfpk jcih xzww"
save_dir = "./"

while True:
    receive_email(username, password, save_dir)





