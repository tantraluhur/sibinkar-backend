from abc import ABC

from commons.middlewares.exception import BadRequestException

class ImportDataService(ABC):
    
    @classmethod
    def import_data(cls, file, jenis) :

        if(jenis == None) :
            raise BadRequestException("Please insert type of data (subdit, subsatker, pangkat, staffing status)")

        if(file.content_type != "text/csv") :
            raise BadRequestException("Please insert csv file.")
        
    
    @classmethod
    def import_data_subit(file) :
        pass

    @classmethod
    def import_data_subsatker(file) :
        pass

    @classmethod
    def import_data_pangkat(file) :
        pass

    @classmethod
    def import_data_staffing_status(file) :
        pass