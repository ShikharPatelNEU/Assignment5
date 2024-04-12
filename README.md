# Assignment5
Development of a Structured Database and Text Extraction System for Finance Professional Development Resources

## Live application Links
[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)]( https://codelabs-preview.appspot.com/?file_id=11RAbeC36bhyxd02Jn-SgXHzEH83_TUOGNOXyD155i3I#0)
[![workflow_architecture](https://img.shields.io/badge/workflow_architecture-FC6600?style=for-the-badge&logo=jupyter&logoColor=white)](https://colab.research.google.com/drive/15hzHqTEWEA3mODdOzBBs7hKNeoz7Bj7d#scrollTo=yO3GCFVqjeoF)
[![knowledge_summaries](https://img.shields.io/badge/knowledge_summaries-FC6600?style=for-the-badge&logo=jupyter&logoColor=white)](https://colab.research.google.com/drive/1z_bdJxOZ216nw997gTckQT6ZLWcJr4jP?usp=sharing)
[![Generate_Q&A](https://img.shields.io/badge/Generate_Q&A-FC6600?style=for-the-badge&logo=jupyter&logoColor=white)](https://colab.research.google.com/drive/1fSoI3f0jRflBNtc3EdGbU76-oyPbj3-A?usp=sharing)


## Problem Statement
*You are an enterprise experimenting with the use of Models as a service APIs to build intelligent applications for knowledge retrieval and Q/A tasks*

## Project Goals
*In enterprises, there are often use cases where information needs to be curated from
multiple sources.While no single solution can meet the requirement, experiments need
to be done to check which approach bodes well for the use case. We will do 4
experiments to see if the results can actually be operationalized in the enterprise.*

## Technologies Used
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Beautiful Soup](https://img.shields.io/badge/beautiful_soup-109989?style=for-the-badge&logo=beautiful_soup&logoColor=white)](https://pypi.org/project/beautifulsoup4/)
[![Selenium](https://img.shields.io/badge/Selenium-39e75f?style=for-the-badge&logo=selenium&logoColor=blue)](https://www.selenium.dev/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-fa722a?style=for-the-badge&logo=python&logoColor=white)](https://docs.streamlit.io/)
[![Pinecone](https://img.shields.io/badge/Pinecone-1c1c1c?style=for-the-badge&logo=pine&logoColor=white)](https://www.pinecone.io/?utm_term=pinecone%20database&utm_campaign=Brand+-+US/Canada&utm_source=adwords&utm_medium=ppc&hsa_acc=3111363649&hsa_cam=21023369441&hsa_grp=167470667468&hsa_ad=690982708943&hsa_src=g&hsa_tgt=kwd-1627713670725&hsa_kw=pinecone%20database&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=CjwKCAjwt-OwBhBnEiwAgwzrUqWwAX2KRT_VT2YCfNeJGp1uNdvpuljxFcbGdjYs1NQJbTj5vkk1OhoCTw8QAvD_BwE)
[![Open_AI](https://img.shields.io/badge/OpenAI-1c1c1c?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)



## Data Sources
*The data source is the [CFA Institute's Refresher Readings](https://www.cfainstitute.org/membership/professional-development/refresher-readings/#sort=%40refreadingcurriculumyear%20descending)* and the provided PDF files.

## Architecture Workflow
![Workflow](https://github.com/BigDataIA-Spring2024-Sec1-Team5/Assignment5/blob/main/Images/architecture.png)

## Pre requisites
*Installed Libraries of Python, Pinecone, OpenAI, Langchain, Streamlit. <br>
Existing accounts of Pinecone and OpenAI with their keys*

## References
https://www.cfainstitute.org/membership/professional-development/refresher-readings/overview-equity-portfolio-management<br>
https://www.cfainstitute.org/membership/professional-development/refresher-readings/industry-company-analysis<br>
https://www.cfainstitute.org/membership/professional-development/refresher-readings/2018/discounted-dividend-valuation<br>
https://medium.com/muthoni-wanyoike/implementing-text-summarization-using-openais-gpt-3-api-dcd6be4f6933<br>
https://us-east-2.console.aws.amazon.com/s3/get-started?region=us-east-2&bucketType=general&region=us-east-2<br>
https://github.com/openai/openai-cookbook/tree/main/examples/vector_databases<br>

## Learning Outcomes
*Through this project, we will leverage Pinecone and OpenAI api’s for:<br>*
*1. Creating knowledge summaries using OpenAI’s GPT*<br>
*2. Generating a knowledge base (Q/A) providing context*<br>
*3. Using a vector database to find and answer questions.*<br>
*4. Use the knowledge summaries from 1 to answer questions.*<br>

## Team Information and Contribution 

Name | Contribution %| Contributions |
--- |--- | --- |
Aditya Kanala, Shubh Patel | 66% | Scraping, OpenAI & Pinecone|
Shikhar Patel | 34% | Streamlit|
