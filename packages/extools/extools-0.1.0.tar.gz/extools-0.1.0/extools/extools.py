from accpac import *

def all_records(datasourceid):
    """Generator that yields all records in a datasource."""
    ds = self.openDataSource(datasourceid)
    ds.recordClear()
    ds.browse("")

    while ds.fetch() == 0:
        yield ds

def _optional_field_exists_in(datasource, field):
    """Check if a record with field = value exists."""
    datasource.recordClear()
    datasource.put("FIELD", field)
    if datasource.read() == 0:
        return True
    return False

def insert_or_update_optional_field(datasourceid, field, value):
    """Check if an optional field exists, if so update, otherwise insert"""
    ofds = self.openDataSource(datasourceid)
    ofds.recordClear()

    if _optional_field_exists_in(ofds, field):
        ofds.put("VALUE", value)
        if ofds.update() != 0:
            return False
    else
        ofds.recordGenerate()
        ofds.put("FIELD")
        ofds.put("VALUE", value)
        if ofds.insert() != 0:
            return False

    return True
