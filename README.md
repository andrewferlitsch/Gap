# epipog-nlp, v1.4
## Natural Language Processing for PDF, TIFF, and camera captured documents.

### Framework

The Epipog NLP framework provides an easy to get started into the world of machine learning for your unstructured data in PDF documents, scanned documents, TIFF facsimiles and camera captured documents. 

  - Automatic OCR of scanned and camera captured images.
  - Automatic Text Extraction from documents.
  - Automatic Syntax Analysis.
  - Programmatic control for data extraction or redaction (de-identification)
  
    - Names, Addresses, Proper Places
    - Social Security Numbers, Data of Birth, Gender
    - Telephone Numbers
    - Numerical Information (e.g., medical, financial, …) and units of measurement.
    - Unit conversion from US Standard to Metric, and vice-versa
    - Unicode character recognition

  - Machine Training of Document and Page Classification.
  
The framework consists of a sequence of Python modules which can be retrofitted into a variety of configurations. The framework is designed to fit seamlessly and scale with an accompanying infrastructure. To achieve this, the design incorporates:

  - Problem and Modular Decomposition utilizing Object Oriented Programming Principles.
  - Isolation of Operations and Parallel Execution utilizing Functional Programming Principles.
  - High Performance utilizing Performance Optimized Python Structures and Libraries.
  - High Reliability and Accuracy using Test Driven Development Methodology.

## Audience

This framework is ideal for any organization planning to do data extraction from their repository of documents into an RDBMS system for CART analysis, linear/logistic regressions or generating word vectors for natural language deep learning (DeepNLP).

## License

The source code is made available under the Creative Commons license: [CC-BY](https://creativecommons.org/licenses/by/4.0/)

## Prerequites

The Epipog framework extensives uses a number of open source applications/modules. The following applications and modules will need to be installed on your computer/laptop:

  1. Artifex's Ghostscript - extracting text from text PDF
  2. ImageMagic's Magick - extracting image from scanned PDF
  3. Google's Tesseract - OCR of scanned/image captured text
  4. NLTK (Natural Language Toolkit) - stemming/lemmatizer/parts of speech annotation
  5. unidecode - romanization of latin character codes

## Installation

#### Ghostscript

1. Download link : https://www.ghostscript.com/download/gsdnld.html
        
    Use the Free Version<br/>

    Example: Ghostscript 9.23 for Windows (64 bit).<br/>

2. Check if path to the program is in your PATH variable. 

    A. Open a command shell.<br/>
    B. Type gswin64c in the command line.<br/>
    C. If not found, add it to your path variable. Ex: C:\Program Files\gs\gs9.23\bin<br/>

#### Magick

1. Download Link: https://www.imagemagick.org/script/download.php

    Use the 8bits per pixel static version (dynamic is for DLL inclusion).<br/>

    Ex. 64bit Windows laptop: ImageMagick-7.0.8-1-Q8-x64-static.exe<br/>

2. Check if path to the program is in your PATH variable.

    A. Open a command shell.<br/>
    B. Type magick in the command line.<br/>
    C. If not found, add it to your path variable. For me, it is: C:\Program Files\ImageMagic-7.0.8-Q8

#### Tesseract

1. Download Link: https://github.com/tesseract-ocr/tesseract/wiki/Downloads

    A. Make sure to add the English Language training data to the tessdata subdirectory where tesseract is installed.

2. Check if path to program is in your PATH variable:

    A. Open a command shell.<br/>
    B. Type tesseract in the command line.<br/>
    C. If not found, add it your path variable. For me, it is C:\Program Files\tesseract-Win64\

3. Install the English Training Data files as: C:\Program Files\tesseract-Win64\tessdata . You can get a copy from my [github account.](tools/tessdata)

#### NLTK

1. Install NLTK using pip:

    pip install nltk
    
    
#### Unidecode

1. Install unidecode using pip:

    pip install unidecode

## Modules

The framework provides the following pipeline of modules to support your data and knowledge extraction from both digital and scanned PDF documents, TIFF facsimiles and image captured documents.

#### SPLITTER

The splitter module is the entry point into the pipeline. It consists of a Document and Page class. The Document class handles the splitting of PDF documents into PDF pages, TIFF facsimiles into TIFF pages, OCR and raw text extraction. PDF splitting and image extraction is handled by the open source Artifex’s Ghostscript ©, and TIFF splitting by open source Image Magic’s Magick ©. OCR is handled by the open source Google’s Tesseract ©. The Document object stores the individual PDF/TIFF/image pages and corresponding raw text and optionally page images (when scanned PDF, TIFF or images) in the specified storage path. The splitting process can be done synchronously or asynchronously, where in the latter case an event handler signals when the splitting/OCR has been completed and the page table is accessible.

For OCR, the resolution of the image extraction is settable, which will affect the quality of the OCR, and corresponding processing time. If the resolution of the original scanned page is lower than the setting, it will be up-sampled, and conversely if it is higher it will be down-sampled.

The Page class handles access to the individual pages, via the page table of the document class. Access is provided to the individual PDF, TIFF or image page, the scanned image (when scanned PDF, TIFF or images), raw text and the Natural Language Processing (NLP) processed tokens (when SYNTAX module is installed).

NLP processing of the raw text is deferred until first access (JIT), and then preserved in memory as long as the corresponding page object is referenced. The NLP processed tokens may be further segmented into regions, consisting of tables, paragraphs, columns, etc. when the SEGMENTATION module is installed.

The document and corresponding pages may be classified (i.e., category of the content) when the CLASSIFICATION module is installed.

#### SYNTAX

The syntax module follows the splitter module in the pipeline. It consists of the Words and Vocabulary classes. The Words class handles natural language processing (NLP) of the extracted text. The NLP processing can be configured for tokenization, stemming, lemmatizing, stop word removal, syntax analysis and word classification, with Unicode support. 

The word classifier recognizes:

  - Syntax Units: Articles, Demonstratives, Prepositions, Pronouns, Conjunctions, Quantifiers, Questions
  - Abbreviations
  - Acronyms
  - Gender (inclusive of Transgender)
  - Date of Birth
  - USA and Canadian Addresses
  - USA and Canadian Telephone Numbers
  - USA Social Security numbers
  - USA and ISO Standard for Dates
  - USA and ISO Standard for Numbers and units of measure. 
  - Geographic Locations
  - Sentiment

Dates, numbers and units of measure can be converted to either USA Standard or ISO Standard.  USA and Canadian postal addresses are converted to the USPO standard for address matching.

Along with the builtin stemmer and lemmatizer, the module can optionally be configured to use the NLTK (open source) stemmers, lemmatizer and parts of speech annotations.


#### SEGMENTATION

-- describe here

## User's Guide

The User's (Programming) Guide can be found [here](specs/users%20guide.docx)

## Releases

-- describe here

## Testing

The Epipog framework is developed using Test Driven Development methodology. The automated unit tests for the framework use pytest, which is a xUnit style form of testing (e.g., jUnit, nUnit, jsUnit, etc). 

#### Installation and Documentation

The pytest application can be installed using pip:

    pip install pytest
    
Online documentation for [pytest](https://docs.pytest.org)

#### Execution
   
The following are the pre-built automated unit tests:
 
    document_test.py    # Tests the Document Class in the Splitter Module
    page_test.py        # Tests the Page Class in the Splitter Module
    words_test.py       # Tests the Word Class in the Syntax Module: 307 tests
    
The automated tests are executed as follows:

    pytest -v document_test.py
    pytest -v page_test.py
    pytest -v words_test.py
    
#### Code Coverage

Information on the percent of code that is covered (and what source lines not covered) by the automated tests is obtained using pytest-cov. This version of pytest is installed using pip:

    pip install pytest-cov
    
Testing with code coverage is executed as follows:

    pytest --cov=words words_test.py
    
        Statements=1037, Missed=68, Percent Covered: 93%

