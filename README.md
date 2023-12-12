##### ** Assignment-5-Information-Retrieval-from-Real-Data

# Apple Health Data Analysis Using Resting Heart Rate

## Team Members

- **Hannah DeSoto**
  - Email: hdesoto@westmont.edu

- **Michelle Jee**
  - Email: mjee@westmont.edu

  
##  **Introduction**

Our Python script aims to analyze health data exported from Apple Health using the resting heart rate metric. It performs data extraction from an XML file, processes the data, calculates the monthly average resting heart rate, and forecasts the next 24 months using ARIMA (AutoRegressive Integrated Moving Average) time series forecasting.


## **Installation** 

Make sure these packages are installed below: 

Prerequisites
Python 3.x
Required Python packages: xml.etree.ElementTree, pandas, statsmodels, matplotlib

## **Usage**
    - Ensure that the required Python packages are enstalled by running 
    - Modify the script's main section with your specified paths:
      
   xml_file_path = '/path/to/your/health/data.xml' 
      
   output_file = '/path/to/your/output/original_data.csv'
   
   forecast_file = '/path/to/your/output/forecast_data.csv'
    - Run the script
      python3 HDRestingHeartRateAnalyzer.py


## **Code Structure**

XMLDataExtractor Class

This class works to extract the relevant health data from an XML file exported 
from Apple Health. It initializes dictionaries for different health metrics and 
uses the method 'extract_data' to parse the XML file and store the data in these 
dictionaries. 

RestingHeartRateAnalyzer Class

Using an instance of 'XMLDataExtractor', this class process the extracted data and 
converts it into a pandas DataFrame. Then, it calculates the monthly average 
resting heart rate, and provides methods to visualize and forecast the data. 

## **Licensing Information**

MIT License

Copyright (c) 2023 hdesoto2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## **Sources Cited**

#### ChatGPT Citation:
    - OpenAI. "ChatGPT - OpenAI's Language Model." OpenAI, https://www.openai.com/.
    - Prompt: What are some ways to process XML files
      - DOM (Document Object Model, ET.parsing)
      - SAX (Simple API for XML)
      - lxml (Python Library)
      - XPath (XML Path Language)
      - XSLT (XML Stylesheet Language Transformations)
#### Python Library: 
    - Link: https://docs.python.org/3/library/xml.etree.elementtree.html
    - Understanding how to use ET.parse()
    - The different features of Element Tree
#### ARIMA: 
    - Link: https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/
    - Plotting graphs for forecasting
    - Finding the monthly average for the data




## How to Contribute

If you're interested in contributing to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.
4. Ensure your code passes any existing tests.


## Contact Information
For any inquiries or collaboration opportunities, please reach out to:

- **Hannah DeSoto**
  - Email: hdesoto@westmont.edu

- **Michelle Jee**
  - Email: mjee@westmont.edu

### Thank you for your interest in our project!
