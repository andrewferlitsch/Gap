# epipog-nlp
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
  4. NLTK (Natural Language Toolkit)

## Installation

[Ghostscript](ghostscript.md)

[Magick](magick.md)

[Tesseract](tesseract.md)

[NLTK](nltk.md)

## Modules

-- describe here

### SPLITTER


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

### SYNTAX

-- describe here

### SEGMENTATION

-- describe here

## User's Guide

-- describe here

## Releases

-- describe here
