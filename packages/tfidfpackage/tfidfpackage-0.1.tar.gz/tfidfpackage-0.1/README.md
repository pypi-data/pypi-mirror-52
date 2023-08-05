# term_frequency
Term frequency–inverse document frequency
 To install package on Windows, install the following:

       install Python
       install Pip
       Install VirtualEnv

Next, create a folder on your desktop named PDFKeywords.

Open your Command Prompt and navigate to your PDFKeywords folder then enter:
       "pip install virtualenv"

In your Command Prompt navigate to your PDFKeywords on your desktop to launch:
        cd PDFKeywords

 Within your PDFKeywords folder create  a new virtualenv named env:
        virtualenv env

 Activate your virtualenv:
        on Windows, virtualenv creates a batch file called:
            "\env\Scripts\activate.bat"

        To activate virtualenv on Windows, activate script is in the Scripts folder :

            \env\Scripts\activate

Now the env will appear to the denoting your virtualenv is activate.
install the package

        pip install tfidfpackage


Ensure pip, setuptools, and wheel are up to date:

        python -m pip install --upgrade pip setuptools wheel

Note: The package will be installed into the env/Lib/site_packages.


Now run the following command :
        pip install -i https://test.pypi.org/simple tfidfpackage

Run the Python interpreter (make sure you’re still in your virtualenv):
        python PdfReader.py
