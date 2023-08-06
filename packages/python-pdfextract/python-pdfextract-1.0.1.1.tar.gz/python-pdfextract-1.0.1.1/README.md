# python-pdfextract


A python wrapper for [pdf-extract](https://github.com/bitextor/pdf-extract), a Java library for HTML extraction from PDF documents.

## Configuration


Dependencies:

 * jpype
 * chardet

The pdf-extract jar files will get fetched and included automatically when building the package.

## Installation

Checkout the code:

	git clone https://github.com/misja/python-pdfextract.git
	cd python-pdfextract


**virtualenv**

	virtualenv env
	source env/bin/activate
    pip install -r requirements.txt
	python setup.py install
	

**Fedora**

    sudo dnf install -y python2-jpype
    sudo python setup.py install


## Usage


Be sure to have set `JAVA_HOME` properly since `jpype` depends on this setting.

    from pdfextract.extract import Extractor
    extractor = Extractor(pdf=your_pdf_data)

Then, to extract relevant content:

    extracted_html = extractor.extract()



