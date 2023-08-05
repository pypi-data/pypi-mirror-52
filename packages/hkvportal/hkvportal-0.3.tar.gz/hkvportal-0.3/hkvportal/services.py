# coding: utf-8
################################
#### Author: Mattijn van Hoek ##
####  While working for HKV   ##
####     Date 2017-2019       ##
####     Version: 0.4         ##
################################
import zeep
import pandas as pd
import io
import json
import requests
import urllib.parse


class Service(object):
    """
    mangrove service to create/update databases, set and get entries.
    """

    def __init__(self, dataservice, uid=None):
        """
        set URL for dataservice to be used
        
        Parameters
        ----------
        dataservice: str
            URL of dataservice instance (eg. 'http://85.17.82.66/dataservices/')   
        uid: str
            User Identification ID. Request by IT               
        """
        self.setDataservice(dataservice)
    
    class errors(object):
        """
        error class with different errors to provide for fewsPi
        """

        def nosetDataservice():
            raise AttributeError(
                "dataservice not known. set first using function setDataservice()"
            )

        def inputDataType():
            raise AttributeError(
                "input type of data is not recognized. Choose between type str, io.StringIO or io.BytesIO"
            )
            
    def serializeData(self, data):
        if isinstance(data, str):
            data = data.encode()
        elif isinstance(data, io.StringIO):
            data = data.getvalue().encode()
        elif isinstance(data, io.BytesIO):
            data = data.getvalue()
        elif isinstance(data, bytes):
            pass
        else:
            self.errors.inputDataType()
            
        return data

    def setDataservice(self, dataservice, dump=False):
        """
        function to set URL for dataservice to be used in other functions
        
        Parameters
        ----------
        dataservice: str
            URL of dataservice instance (eg. 'http://85.17.82.66/dataservices/')
        """
        setattr(Service, "dataservice", dataservice)
        wsdl = urllib.parse.urljoin(
            self.dataservice, "data.asmx?WSDL"
        )
        self.client = zeep.Client(wsdl=wsdl)
        if dump == False:
            return print(
                "Dataservice is recognized.",
                self.dataservice,
                "will be used as portal",
            )
        if dump == True:
            return self.client.wsdl.dump()

    def createDatabase(self, database):
        """
        Create database
        
        Parameters
        ----------
        database: str
            name of database instance (eg. 'Myanmar')        
        """
        if not hasattr(self, "dataservice"):
            self.errors.nosetDataservice()

        url = urllib.parse.urljoin(
            self.dataservice,
            "database.asmx/create?database=" + database,
        )
        r = requests.get(url)
        return r.json()

    def listDatabase(self, database):
        """
        Check database info
        
        Parameters
        ----------
        database: str
            name of database instance (eg. 'Myanmar')        
        """
        if not hasattr(self, "dataservice"):
            self.errors.nosetDataservice()
        url = urllib.parse.urljoin(
            self.dataservice,
            "data.asmx/list?database=" + database,
        )
        r = requests.get(url)
        return r.json()

    def setEntryDatabase(
        self, database, key, data, description=""
    ):
        """
        Set/create/insert new entry in database
        
        Parameters
        ----------
        database: str
            name of database instance (eg. 'Myanmar') 
        key: str
            key to identify datarecord in the database (eg. 'parameter|location|unit')
        data: obj
            object to store in the datarecord (eg. JSON object)
        description: str
            description of the datarecord (default = '')
        """
        
        data = self.serializeData(data)

        if not hasattr(self, "dataservice"):
            self.errors.nosetDataservice()

        # Set data using create datarecord

        zeep_out = self.client.service.createbytes(
            database=database,
            key=key,
            description=description,
            data=data,
        )
        url = urllib.parse.urljoin(
            self.dataservice,
            "data.ashx?database="
            + database
            + "&key="
            + key
            + "&contentType=SET_BY_USER",
        )
        print("available at {}".format(url))
        return json.loads(zeep_out)

    def updateEntryDatabase(
        self, database, key, data, description=""
    ):
        """
        Update existing  entry in database
        
        Parameters
        ----------
        database: str
            name of database instance (eg. 'Myanmar') 
        key: str
            key to identify datarecord in the database (eg. 'parameter|location|unit')
        data: obj
            object to store in the datarecord (eg. JSON object)
        description: str
            description of the datarecord (default = '')
        """
        
        data = self.serializeData(data)
        
        if not hasattr(self, "dataservice"):
            self.errors.nosetDataservice()

        # Set data using updatebytes function
        zeep_out = self.client.service.updatebytes(
            database=database,
            key=key,
            description=description,
            data=data,
        )
        return json.loads(zeep_out)

    def getEntryDatabase(
        self, database, key, content_type="application/json"
    ):
        """
        Get entry after create/insert
        
        Parameters
        ----------
        database: str
            name of database instance (eg. 'Myanmar') 
        key: str
            key to identify datarecord in the database (eg. 'parameter|location|unit')
        content_type: str
            set the contentType to make the browser render the output correctly
            csv : application/csv
            json : application/json
            html : text/html
        """
        if not hasattr(self, "dataservice"):
            self.errors.nosetDataservice()
        url = urllib.parse.urljoin(
            self.dataservice,
            "data.ashx?database="
            + database
            + "&key="
            + key
            + "&contentType="
            + content_type,
        )
        print(url)
        
        if "json" in content_type:
            r = requests.get(url)
            output = pd.read_json(r.content.decode())            
        elif "html" in content_type:
            from IPython.display import IFrame
            output = IFrame(url, width='100%', height=350)
        elif "csv" in content_type:
            r = requests.get(url)
            output = pd.read_csv(io.StringIO(r.content.decode("utf-8")))
        elif "png" in content_type:
            from PIL import Image               
            from IPython.display import display
            r = requests.get(url)
            img = Image.open(io.BytesIO(r.content))
            output = display(img)
        elif "svg" in content_type:
            from IPython.display import SVG, display
            r = requests.get(url)
            output = display(SVG(r.content.decode()))
        elif "xml" in content_type:
            from .untangle import parse_raw
            r = requests.get(url)
            output = parse_raw(r.content.decode())            
        else:
            r = requests.get(url)
            try:
                output = r.content.decode()
            except UnicodeDecodeError:
                import chardet
                output = chardet.detect(r.content)

        return output

    def deleteEntryDatabase(self, database, key):
        """
        Delete entry from database
        
        Parameters
        ----------
        database: str
            name of database instance (eg. 'Myanmar') 
        key: str
            key to identify datarecord in the database (eg. 'parameter|location|unit')       
        """
        # delete data from database
        if not hasattr(self, "dataservice"):
            self.errors.nosetDataservice()
        url = urllib.parse.urljoin(
            self.dataservice,
            "data.asmx/delete?database="
            + database
            + "&key="
            + key,
        )
        r = requests.get(url)
        return r.json()
