# DelvInDocs.AI

DelvInDocs.AI🤖 is a generative AI tool designed to enhance the understandability of extensive documentation. Utilizing Langchain, OpenAI GPT, and Deeplake Vector, this tool intelligently scrapes information from provided base URLs and their child links. Users can ask questions and receive tailored code snippets and cohesive responses across various libraries (e.g., React, Node.js, Tailwind CSS, MongoDB). This streamlines the process of finding relevant documentation and saves valuable development time.

## Demo
![Demo of DelvInDocs.AI](assets/demo3.gif)

## Features

- **Documentation Scraping:** Automatically scrapes content from base URLs and their child links.
- **Integrated Code Snippets:** Provides cohesive code snippets and responses across multiple libraries.
- **Contex Continuity:** Remebers previous 3 conversation exhanges to maintain conversation continuity for follow up questions
- **User-Friendly Interface:** Simplifies the search for relevant documentation, making it accessible and easy to use.
- **Time-Saving:** Reduces development time by quickly delivering the information needed.

## Architecture
![Architecture](assets/architecture.png)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

Follow these steps to set up the project locally:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**1. Clone the repository:**
```bash
    git clone https://github.com/hrithikkoduri/DelvInDocs.AI.git
    cd DelvInDocs.AI
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**2. Create a virtual environment (optional but recommended):**
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**3. Install the required dependencies:**
```bash
    pip install -r requirements.txt
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**4. Setup Activeloop:**
    
Activeloop provides vector databse to storage embeddings from the data gathered. This will be retrieved by the underlying LLM (in this case GPT-4o) to retrieve relevant information for user queries.

>Create your ActiveLoop account by going tothis link : https://app.activeloop.ai/

Create an **ActiveLoop Token** and paste it securely in a file, this will be useful to connect your app with the databse.

Further you need to create an **organization** (a project like structure where all you dataset will be store) on activeloop and copy the name of the organization you created

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**5. Create OpenAI Key:**

>Go to this link https://openai.com/index/openai-api/

To access the Embeddings and GPT model in the app, you'll need to add some OpenAI credits. For personal use, it doesn't require much—you can start with as little as $5-$10, which should be enough to last 2-3 months depending on your usage.

Sign up and create your **OpenAI API Key**. Copy the api key and store it securely.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**6. Setup environment variables and Deeplake :**
    
Open the .env file replace the respective place holders with your API keys
    
.env
```bash
    ACTIVELOOP_TOKEN="<YOUR_ACTIVELOOP_TOKEN>"
    OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
```

Open vectordb.py script and replace the organization name placeholder with the one you created and the dataset name placeholder with the name of the deeplake dataset you want to create.
    
**Note:** You only need to create the organization on ActiveLoop, the dataset will be created at the runtime with the name you provided on it own.

vectordb.py
```bash
    self.activeloop_org = "<YOUR_ACTIVELOOP_ORGANISATION NAME" # replace with your ActiveLoop organisation name
    self.activeloop_dataset = "<DATASET_NAME>" # replace with your ActiveLoop dataset name you want to be created
```

## Uasge
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**1. Launch the application:**
```bash
    streamlit run main.py
```  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**2. Input the base URLs:** Enter the base URLs of the documentation you want to scrape.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**3. Ask questions:** Inquire about specific information or request code snippets related to the documentation.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**4. Receive tailored responses:** Get cohesive code snippets and relevant answers based on your queries.



## Contributing
Contributions are welcome! To contribute to the project, please follow these steps:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**1. Fork the repository.**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**2. Create a new branch:**
```bash
    git checkout -b feature-branch
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**3. Make your changes and commit them:**
```bash
    git commit -m 'Add new feature'
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**4. Push to the branch:**
```bash
    git push origin feature-branch
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**5. Open a pull request.**

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Acknowledgments
- [Langchain](https://www.langchain.com/) for the framework to manage the AI pipeline.
- [OpenAI](https://openai.com/) GPT for providing the language model.
- [Activeloop Deep Lake](https://activeloop.ai/) for the vector database used in the project.
- Special thanks to all contributors and users for their support and feedback.
