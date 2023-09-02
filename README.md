# BizCardX: Extracting Business Card Data with OCR

**Introduction**

BizCardX is a Streamlit application that effortlessly streamlines business card data extraction through advanced OCR technology. Users can easily upload card images to retrieve essential details, including company names, cardholder names, contact information, and more. With a strong focus on data security and user authentication, BizCardX ensures secure data storage and offers streamlined management via the user-friendly Streamlit UI. Experience an efficient, secure, and user-friendly solution for managing business card information effortlessly with BizCardX.

**Table of Contents**

1. Key Technologies and Skills
2. Installation
3. Usage
4. Features
5. Contributing
6. License
7. Contact

**Key Technologies and Skills**

- OCR (Optical Character Recognition)
- Data Extraction
- Python
- Streamlit (GUI development)
- PostgreSQL (Database management)


**Installation**

To run this project, you need to install the following packages:

```python
pip install easyocr
pip install Pillow
pip install numpy
pip install pandas
pip install pymongo
pip install psycopg2
pip install streamlit
pip install streamlit_option_menu
```

**Usage**

To use this project, follow these steps:

1. Clone the repository: ```git clone https://github.com/gopiashokan/BizCardX-Extracting-Business-Card-Data-with-OCR.git```
2. Install the required packages: ```pip install -r requirements.txt```
3. Run the Streamlit app: ```streamlit run app.py```
4. Access the app in your browser at ```http://localhost:8501```

**Features**

BizCardX offers a range of powerful features to streamline the extraction and management of business card information with a strong emphasis on data protection.

**Business Card Data Extraction**

- **Effortless Extraction**: Easily extract information from business cards by uploading an image, thanks to BizCardX's integration with the easyOCR library.
```
Encountering errors while extracting image data using EasyOCR in local IDEs led to the adoption of 
Google Colab for this process
```

- **Structured Presentation**: The extracted data is elegantly presented alongside the uploaded image, ensuring a clear and organized overview.

- **Comprehensive Information**: Extracted details include the company name, cardholder name, designation, contact information, and address.

- **User-Friendly GUI**: Navigate and interact with the user-friendly graphical interface for a seamless experience.

**Data Storage and Authentication**

- **Secure Authentication**: Safeguard your data with user authentication, ensuring that only authorized users can access and manage it.

- **Data Verification**: Review and confirm the extracted data before it's securely stored in the database. Make necessary changes with confidence.

**Data Management and Editing**

- **Credential Verification**: To edit database records, verify your credentials (username and password) for added security.

- **Effortless Editing**: Easily modify your data as needed, and watch as the changes are automatically updated in the database.

**Secure Data Deletion**

- **Protected Data**: Ensure the safety of your data with strong user authentication, preventing unauthorized access or deletion.

- **Credentials Check**: When initiating data deletion, BizCardX verifies your username and password, displaying a list of associated records.

BizCardX emphasizes data protection, providing secure and user-friendly tools for managing your business card information.


**Contributing**

Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to submit a pull request.

**License**

This project is licensed under the MIT License. Please review the LICENSE file for more details.

**Contact**

📧 Email: gopiashokankiot@gmail.com 

🌐 LinkedIn: [linkedin.com/in/gopiashokan](https://www.linkedin.com/in/gopiashokan)

For any further questions or inquiries, feel free to reach out. We are happy to assist you with any queries.
