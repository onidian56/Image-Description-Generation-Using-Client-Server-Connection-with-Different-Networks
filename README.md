# Image Description Generation Using Client-Server Connection with Different Networks

## Project Overview
This project implements a distributed system for animal image classification across different networks using standard email protocols (SMTP and POP3) for communication. The system consists of a client that captures images and sends them to a server, which then processes the images using a pre-trained deep learning model to classify animals and generate detailed descriptions. The classification results are sent back to the client, creating a complete automated pipeline.

## Table of Contents
- [Architecture](#architecture)
- [System Workflow](#system-workflow)
- [Components](#components)
- [How It Works](#how-it-works)
- [Setup Instructions](#setup-instructions)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Future Work](#future-work)
- [Contributors](#contributors)

## Architecture

The system follows a client-server architecture where communication happens across different networks through email protocols.

### System Architecture Diagram

```mermaid
graph TD
    subgraph "Client Network"
        A[Client PC] -->|1. Capture Image| B[Client Application]
        B -->|2. Send Image via SMTP| C[Email Server]
        C -->|5. Return Description| B
    end
    
    subgraph "Internet"
        C <-->|3. Email Transfer| D[Email Server]
    end
    
    subgraph "Server Network"
        D -->|4. Fetch Image via POP3| E[Server Application]
        E -->|6. Process Image| F[Animal Classification Model]
        F -->|7. Generate Description| E
        E -->|8. Send Description via SMTP| D
    end
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
```

## System Workflow

### Detailed Process Flow

```mermaid
sequenceDiagram
    participant Client
    participant ClientEmail as Client Email (SMTP)
    participant ServerEmail as Server Email (POP3)
    participant Server
    participant Model as Classification Model
    
    Client->>Client: Capture image with webcam
    Client->>ClientEmail: Package image as email attachment
    ClientEmail->>ServerEmail: Send email with image
    
    loop Check for new emails
        Server->>ServerEmail: Poll for new messages
    end
    
    ServerEmail->>Server: Download image attachment
    Server->>Model: Process image
    Model->>Server: Return classification results
    
    Server->>ServerEmail: Send results via email
    ServerEmail->>ClientEmail: Transfer email with results
    
    loop Check for response
        Client->>ClientEmail: Poll for classification results
    end
    
    ClientEmail->>Client: Deliver animal description
    Client->>Client: Display results to user
```

### Classification Pipeline

```mermaid
flowchart LR
    A[Image Input] --> B[Image Preprocessing]
    B --> C[PyTorch Model]
    C --> D[Feature Extraction]
    D --> E[Classification]
    E --> F[Result Processing]
    F --> G[Generate Description]
    
    style A fill:#f9f,stroke:#333,stroke-width:1px
    style C fill:#bbf,stroke:#333,stroke-width:1px
    style G fill:#bfb,stroke:#333,stroke-width:1px
```

## Components

### Client Side (PC 1)
- Captures images using a webcam or selects existing images
- Packages and sends images via SMTP to a predefined email address
- Periodically checks for response emails containing classification results
- Displays the received animal descriptions to the user

### Server Side (PC 2)
- Continuously monitors a designated email inbox using POP3
- Downloads image attachments from received emails
- Processes images using a pre-trained PyTorch animal classification model
- Generates detailed descriptions including scientific name, common name, characteristics, and habitat
- Sends classification results back to the client via email

### Classification Model
- Pre-trained PyTorch deep learning model for animal classification
- Returns comprehensive information including:
  - Scientific name
  - Common name
  - Description
  - Habitat
  - Conservation status (endangered)
  - Safety information (dangerous/poisonous/venomous)
  - Classification confidence (probability)

### Data Flow Diagram

```mermaid
graph TD
    subgraph Client
        A1[Webcam] -->|Capture| A2[Image File]
        A2 -->|Attach| A3[Email Client]
    end
    
    subgraph Communication
        A3 -->|SMTP| B1[Email Server]
        B1 -->|POP3| C1[Server Email Client]
        C4 -->|SMTP| B2[Email Server]
        B2 -->|POP3| A4[Client Email Reader]
    end
    
    subgraph Server
        C1 -->|Extract| C2[Image Processing]
        C2 -->|Analyze| C3[PyTorch Model]
        C3 -->|Results| C4[Response Generator]
    end
    
    subgraph Response
        A4 -->|Display| A5[Classification Results]
    end
    
    style A1 fill:#f9f,stroke:#333,stroke-width:1px
    style C3 fill:#bbf,stroke:#333,stroke-width:1px
    style A5 fill:#bfb,stroke:#333,stroke-width:1px
```

## How It Works

1. **Image Acquisition**:
   - The client application activates the webcam and captures an image
   - The image is temporarily saved on the client system

2. **Image Transmission**:
   - The client packages the image as an email attachment
   - Email is sent using SMTP protocol to a predefined server email address
   - The email subject includes a timestamp for tracking purposes

3. **Server Processing**:
   - The server continuously checks the designated email inbox using POP3
   - When an email with an image attachment is found, the server downloads it
   - The image is processed through the animal classification model

4. **Classification**:
   - The PyTorch model analyzes the image and classifies the animal
   - A complete description is generated with multiple attributes
   - If the confidence level is below 20%, the system returns "Could not identify"

5. **Result Transmission**:
   - The server packages the classification results in a plain text email
   - The response is sent back to the client's email address

6. **Result Display**:
   - The client checks for and retrieves the response email
   - The classification results are displayed to the user

### Classification Example

When an image of a tiger is sent through the system, the result might look like:

```json
{
  "scientific_name": "panthera-tigris",
  "common_name": "Tiger",
  "description": "The largest of the big cats, recognized by its orange coat with black stripes.",
  "habitat": "Forests, grasslands, and wetlands across Asia",
  "endangered": "endangered",
  "dangerous": "True",
  "poisonous": "False",
  "venomous": "False",
  "probability": 97.79
}
```

## Setup Instructions

### Prerequisites
- Python 3.x
- PyTorch and torchvision
- OpenCV (cv2)
- Pillow (PIL)
- Email accounts for client and server (Gmail recommended)
- App passwords for email accounts (for secure authorization)

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/image-description-generation.git
   cd image-description-generation
   ```

2. Install required dependencies:
   ```
   pip install torch torchvision pillow opencv-python
   ```

3. Set up email credentials:
   - Create two separate Gmail accounts (one for client, one for server)
   - Enable 2-Factor Authentication and generate App Passwords for each
   - Update the email credentials in both `client.py` and `server.py`

4. Download model files:
   - Ensure `animal_image.pth` (model) is available
   - Ensure `animal_image_checkpoint.pth.tar` (checkpoint) is available
   - Ensure `animal_image.json` (classification data) is available

5. Running the system:
   - Start the server on PC 2:
     ```
     python server.py
     ```
   - Start the client on PC 1:
     ```
     python client.py
     ```

### System Structure

```mermaid
classDiagram
    class Client {
        +capture_image()
        +send_email()
        +receive_email()
        +main_loop()
    }
    
    class Server {
        +receive_email()
        +classify_image()
        +send_email()
        +main_loop()
    }
    
    class ClassificationModel {
        +load_model()
        +transform_image()
        +classify_animal_image()
        +generate_description()
    }
    
    Client --> Server: sends image via email
    Server --> ClassificationModel: processes image
    Server --> Client: sends classification results
```

## Features

- **Cross-Network Communication**: Works across different networks without direct connection
- **Real-time Image Classification**: Provides detailed animal descriptions with high accuracy
- **Automated Pipeline**: Fully autonomous system requiring minimal user intervention
- **Universal Accessibility**: Works anywhere with basic internet connectivity
- **Webcam Integration**: Direct image capture through connected camera
- **Comprehensive Classification**: Provides detailed information about identified animals

## Technologies Used

- **Python**: Core programming language
- **PyTorch**: Deep learning framework for image classification
- **OpenCV**: Computer vision library for image capture and processing
- **SMTP/POP3**: Email protocols for cross-network communication
- **PIL (Pillow)**: Python Imaging Library for image handling
- **Gmail**: Email service for message exchange

### Technology Stack Diagram

```mermaid
graph TD
    A[Python Ecosystem] --> B[PyTorch]
    A --> C[OpenCV]
    A --> D[Pillow]
    A --> E[Email Libraries]
    
    subgraph "Client Side"
    C --> F[Image Capture]
    D --> G[Image Processing]
    E --> H[SMTP Client]
    E --> I[POP3 Client]
    end
    
    subgraph "Server Side"
    B --> J[Deep Learning Model]
    E --> K[Email Communication]
    end
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#bbf,stroke:#333,stroke-width:2px
```

## Future Work

- Add encryption and security layers to the data transfer
- Implement more complex models like object detection or scene understanding
- Support multiple clients for collaborative classification systems
- Develop a user interface (UI) to track communication logs and outputs in real-time
- Optimize for better performance and lower latency
- Integrate with cloud services for enhanced scalability

## Contributors
- Prithwish Dey (CSE/22065/919)
- Amit Mandhana (CSE/22014/868)
- Anindya Bhaumik (CSE/22018/872)
- Aditya Paul (CSE/22004/858)
- Chirag Shukla (CSE/22038/892)
- Adrish Roy (CSE/22007/861)
- Akash Chauhan (CSE/22009/863)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
