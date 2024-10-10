# DelvInDocs.AI🤖

DelvInDocs.AI is a generative AI tool designed to enhance the understandability of extensive documentation. Utilizing Langchain, OpenAI GPT, and Deeplake Vector, this tool intelligently scrapes information from provided base URLs and their child links. Users can ask questions and receive tailored code snippets and cohesive responses across various libraries (e.g., React, Node.js, Tailwind CSS, MongoDB). This streamlines the process of finding relevant documentation and saves valuable development time.

## Features

- **Documentation Scraping:** Automatically scrapes content from base URLs and their child links.
- **Integrated Code Snippets:** Provides cohesive code snippets and responses across multiple libraries.
- **User-Friendly Interface:** Simplifies the search for relevant documentation, making it accessible and easy to use.
- **Time-Saving:** Reduces development time by quickly delivering the information needed.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Key Management](#api-key-management)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hrithikkoduri/DelvInDocs.AI.git
   cd DelvInDocs.AI

2. **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt

## Uasge

1. **Launch the application:**
    ```bash
    python app.py  # Replace with your main script

2. **Input the base URLs:** Enter the base URLs of the documentation you want to scrape.

3. **Ask questions:** Inquire about specific information or request code snippets related to the documentation.

4. **Receive tailored responses:** Get cohesive code snippets and relevant answers based on your queries.

## Configuration

Before running the application, you may need to configure certain settings, such as:

Base URLs: Input the URLs of the documentation you want to scrape.
Query Parameters: Customize how the application processes and retrieves information based on your needs.

## API Key Management
To ensure your API keys are secure:

Store API keys securely: Use environment variables or a .env file to manage your API keys.

Do not include API keys in your code: Ensure that your API keys are excluded from version control by adding them to your .gitignore file.

## Contributing
Contributions are welcome! To contribute to the project, please follow these steps:

1. **Fork the repository.**

2. **Create a new branch:**
    ```bash
    git checkout -b feature-branch

3. **Make your changes and commit them:**
    ```bash
    git commit -m 'Add new feature'

4. **Push to the branch:**
    ```bash
    git push origin feature-branch

5. **Open a pull request.**

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Langchain for the framework to manage the AI pipeline.
- OpenAI GPT for providing the language model.
- Deeplake for the vector database used in the project.
- Special thanks to all contributors and users for their support and feedback.
