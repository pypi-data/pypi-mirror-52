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

    def __init__(self, dataservice, uid):
        """
        set URL for dataservice to be used
        
        Parameters
        ----------
        dataservice: str
            URL of dataservice instance (eg. 'https://tsws.hkvservices.nl/mangrove.ws/')   
        uid: str
            User Identification ID. Request by IT               
        """
        
        self.dataservice(dataservice)
        self.uid = uid
    
    class errors(object):
        """
        error class with different errors to provide for fewsPi
        """

        def noset_dataservice():
            raise AttributeError(
                "dataservice not known. set first using function setDataservice()"
            )
            
        def database_not_exist():
            raise AttributeError(
                "used database does not exist"
            )

        def key_not_exist():
            raise AttributeError(
                "used key does not exist in database"
            )            

        def input_data_type():
            raise AttributeError(
                "input type of data is not recognized. Choose between type str, io.StringIO or io.BytesIO"
            )
        
    def get_url(self, database, key, content_type='SET_BY_USER'):        
        url = urllib.parse.urljoin(
            self._dataservice,
            "?function=dataportal.db.getdata&parameters={{database:'{}',key:'{}'}}&contentType={}".format(database, key, content_type)
        )
        print("entry available at:\n{}".format(url))
        return url
            
    def serialize_data(self, data):
        if isinstance(data, str):
            data = data.encode()
        elif isinstance(data, io.StringIO):
            data = data.getvalue().encode()
        elif isinstance(data, io.BytesIO):
            data = data.getvalue()
        elif isinstance(data, bytes):
            pass
        else:
            self.errors.input_data_type()
            
        return data

    def dataservice(self, dataservice, dump=False):
        """
        function to set URL for dataservice to be used in other functions
        
        Parameters
        ----------
        dataservice: str
            URL of dataservice instance (eg. 'https://tsws.hkvservices.nl/mangrove.ws/')
        """
        self._dataservice = urllib.parse.urljoin(dataservice, "data.ashx")
        self._call = urllib.parse.urljoin(dataservice, "entry.asmx/Call?")
        self._wsdl = urllib.parse.urljoin(dataservice, "entry.asmx?WSDL")
        settings = zeep.Settings(strict=False, raw_response=True)
        
        self.client = zeep.Client(wsdl=self._wsdl, settings=settings)
        if dump == False:
            return print(
                "Dataservice is recognized.",
                self._wsdl,
                "will be used as portal",
            )
        if dump == True:
            return self.client.wsdl.dump()

    def create_database(self, database):
        """
        Create database
        
        Parameters
        ----------
        database: str
            name of database instance (eg. 'Myanmar')        
        """
        if not hasattr(self, "dataservice"):
            self.errors.nosetDataservice()

        parameters = {
            "uid": self.uid,
            "database":database}
        payload = {'function':'dataportal.db.createdatabase','parameters':json.dumps(parameters)}
        r = requests.get(self._call, payload)            
            
        return r.json()

    def info(self, database):
        """
        Check database info
        
        Parameters
        ----------
        database: str
            name of database instance (eg. 'Myanmar')        
        """
        if not hasattr(self, "dataservice"):
            self.errors.noset_dataservice()

        parameters = {"database":database}
        payload = {'function':'dataportal.db.getinfo','parameters':json.dumps(parameters)}
        r = requests.get(self._call, payload)

        return r.json()

    def new_entry(self, database, key, data, description="", info_db=False):
        """
        Set/create/insert a NEW entry in database. 
        This does not overwrite, or update existing entries.
        Use update_entry for updating existing entries
        
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
        info_db: boolean
            if True also output debug information from the database
        """
        
        data = self.serialize_data(data)

        if not hasattr(self, "dataservice"):
            self.errors.noset_dataservice()

        parameters = {
            "uid":self.uid,
            "database":database,
            "key":key,
            "description":description}

        zeep_out = self.client.service.CallBytes(function="dataportal.db.createentry", parameters=json.dumps(parameters), bytes=data)
        self.get_url(database, key)

        if info_db:
            return json.loads(zeep_out.text)

    def update_entry(self, database, key, data, description="", info_db=False):
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
        info_db: boolean
            if True also output debug information from the database            
        """
        
        data = self.serialize_data(data)
        
        if not hasattr(self, "dataservice"):
            self.errors.noset_dataservice()

        parameters = {
            "uid": self.uid,
            "database":database,
            "key":key,
            "description":description}

        zeep_out = self.client.service.CallBytes(function="dataportal.db.UpdateEntry", parameters=json.dumps(parameters), bytes=data)
        self.get_url(database, key)
        
        if info_db:
            return json.loads(zeep_out.text)

    def get_entry(
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
            self.errors.noset_dataservice()
        url = self.get_url(database, key, content_type)
        
        r = requests.get(url)
        # check for errors
        if r.text == 'database does not exists':
            self.errors.database_not_exist()
        elif r.text == 'Object reference not set to an instance of an object.':
            self.errors.key_not_exist()
        
        # parse input dta
        if "json" in content_type:
            output = pd.read_json(r.content.decode())            
        elif "html" in content_type:
            from IPython.display import IFrame
            output = IFrame(url, width='100%', height=350)
        elif "csv" in content_type:
            output = pd.read_csv(io.StringIO(r.content.decode("utf-8")))
        elif "png" in content_type:
            from PIL import Image               
            from IPython.display import display
            img = Image.open(io.BytesIO(r.content))
            output = display(img)
        elif "svg" in content_type:
            from IPython.display import SVG, display
            output = display(SVG(r.content.decode()))
        elif "xml" in content_type:
            from .untangle import parse_raw
            output = parse_raw(r.content.decode())            
        else:
            try:
                output = r.content.decode()
            except UnicodeDecodeError:
                import chardet
                output = chardet.detect(r.content)

        return output

    def delete_entry(self, database, key):
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
        parameters = {
            "uid": self.uid,
            "database":database, 
            "key":key}

        payload = {'function':'dataportal.db.DeleteEntry','parameters':json.dumps(parameters)}
        r = requests.get(self._call, payload)        
        
        return r.json()
