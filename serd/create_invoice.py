#!/usr/bin/env python3
from datetime import date, datetime, timedelta
from calendar import monthrange
from dateutil.rrule import rrule, MONTHLY

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, TableColumnProperties
from odf.table import Table, TableColumn, TableRow, TableCell
from io import BytesIO
from .utils.db import get_persons, get_departing_stays, get_arriving_stays,  get_stays
from serd.models import Hotel

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def create_ods( begin:date, end:date ):

    assert(begin.day == 1)
    assert(end.day == 1)
    assert(begin.year == end.year)

    textdoc = OpenDocumentSpreadsheet()
    # Create a style for the table content. One we can modify
    # later in the spreadsheet.
    tablecontents = Style(name="Large number", family="table-cell")
    tablecontents.addElement(TextProperties(fontfamily="Arial", fontsize="15pt"))
    textdoc.styles.addElement(tablecontents)

    # Create automatic styles for the column widths.
    widewidth = Style(name="co1", family="table-column")
    widewidth.addElement(TableColumnProperties(columnwidth="2.8cm", breakbefore="auto"))
    textdoc.automaticstyles.addElement(widewidth)
    


    # Create automatic style for the price cells.
    
    hotels = Hotel.objects.all()
    months = [dt.strftime("%m")
          for dt in rrule(MONTHLY, dtstart=begin,
                          until=end)]
    days = {}
    for month in months:
        
        lastday = monthrange(begin.year, int(month))[1]
        days[month] = lastday

    for hotel in hotels:
    
        table = Table(name=hotel.name)
        for month in months:
            table.addElement(TableColumn(stylename=widewidth, defaultcellstylename="ce1"))
            table.addElement(TableColumn(stylename=widewidth, defaultcellstylename="ce1"))
            table.addElement(TableColumn(stylename=widewidth, defaultcellstylename="ce1"))
            table.addElement(TableColumn(stylename=widewidth, defaultcellstylename="ce1"))
            table.addElement(TableColumn(stylename=widewidth, defaultcellstylename="ce1"))
            
    # Create a row (same as <tr> in HTML)
        tr = TableRow()
        table.addElement(tr)
        for month in months:
            cell = TableCell(valuetype="string",  stringvalue=str(month))
            tr.addElement(cell)
            cell = TableCell(valuetype="string",  stringvalue="")
            tr.addElement(cell)
            cell = TableCell(valuetype="string",  stringvalue="")
            tr.addElement(cell)
            cell = TableCell(valuetype="string",  stringvalue="")
            tr.addElement(cell)
            cell = TableCell(valuetype="string",  stringvalue="")
            tr.addElement(cell)
        tr = TableRow()
        table.addElement(tr)
        for month in months:
            cell = TableCell(valuetype="string",  stringvalue="Tag")
            tr.addElement(cell)
            cell = TableCell(valuetype="string",  stringvalue="Anreisen")
            tr.addElement(cell)
            cell = TableCell(valuetype="string",  stringvalue="Bestand")
            tr.addElement(cell)
            cell = TableCell(valuetype="string",  stringvalue="Abreisen")
            tr.addElement(cell)
            cell = TableCell(valuetype="string",  stringvalue="")
            tr.addElement(cell)
        
        for i in range(1, 32):
            tr = TableRow()
            table.addElement(tr)
            for month in months:
                if i <= days[month]:
                    day = datetime(begin.year, int(month), i)
                    cell = TableCell(valuetype="string", stringvalue= str(i)+".")
                    tr.addElement(cell)
                    arrivals = get_arriving_stays(hotel,day)
                    cell = TableCell(valuetype="string", stringvalue= str(get_persons(arrivals)))
                    tr.addElement(cell)
                    current = get_stays(hotel, day)
                    cell = TableCell(valuetype="string", stringvalue= str(get_persons(current)))
                    tr.addElement(cell)
                    departing = get_departing_stays(hotel, day)
                    cell = TableCell(valuetype="string", stringvalue= str(get_persons(departing)))
                    tr.addElement(cell)
                else:
                    cell = TableCell(valuetype="string", stringvalue= "")    
                    tr.addElement(cell)
                    cell = TableCell(valuetype="string", stringvalue= "")
                    tr.addElement(cell)
                    cell = TableCell(valuetype="string", stringvalue= "")
                    tr.addElement(cell)
                    cell = TableCell(valuetype="string", stringvalue= "")
                    tr.addElement(cell)
                cell = TableCell(valuetype="string", stringvalue= "")
                tr.addElement(cell)
        for i in range(4):
            tr = TableRow()
            table.addElement(tr)
        for day in daterange(begin, end):
            arriving = get_arriving_stays(hotel, day)
            for stay in arriving:
                tr = TableRow()
                table.addElement(tr)
                cell = TableCell(valuetype="string", stringvalue = str(stay.arrival_date))
                tr.addElement(cell)
                cell = TableCell(valuetype="string", stringvalue= str(stay.departure_date))
                tr.addElement(cell)
                cell = TableCell(valuetype="string", stringvalue= stay.request.given_name +" "+ stay.request.last_name)
                tr.addElement(cell)
                




        textdoc.spreadsheet.addElement(table)
    io = BytesIO()
    textdoc.write(io)
    return io




            
            

