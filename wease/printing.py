# -*- coding: utf-8 -*-
import datetime
from datetime import date
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
from authentication.models import Account

#Register Fonts
pdfmetrics.registerFont(TTFont('Lato', settings.STATIC_ROOT + '/fonts/Lato/Lato-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Lato-bold', settings.STATIC_ROOT + '/fonts/Lato/Lato-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Lato-light', settings.STATIC_ROOT + '/fonts/Lato/Lato-Light.ttf'))
pdfmetrics.registerFont(TTFont('Lato-lightitalic', settings.STATIC_ROOT + '/fonts/Lato/Lato-Lightitalic.ttf'))
# pdfmetrics.registerFont(TTFont('Arial', settings.STATIC_ROOT + 'fonts/arial.ttf'))
# pdfmetrics.registerFont(TTFont('Arial-Bold', settings.STATIC_ROOT + 'fonts/arialbd.ttf'))

class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    @staticmethod
    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
 
        # Header
        header = Paragraph('WeASe Company', styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
 
        # Footer
        footer = Paragraph('WeASe', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
 
        # Release the canvas
        canvas.restoreState()

    def build_pdf(self, obj):
        users = Account.objects.all()
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch/4,
                                leftMargin=inch/4,
                                topMargin=inch/2,
                                bottomMargin=inch/4,
                                pagesize=self.pagesize)
 
        # Our container for 'Flowable' objects
        elements = []
 
        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='RightAlign', fontName='Lato', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='LeftAlign', fontName='Lato', alignment=TA_LEFT))
        styles.add(ParagraphStyle(name='CenterAlign', fontName='Lato', alignment=TA_CENTER))
        #styles.add(TableStyle(fontName='Lato'))
 
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        staticpath = settings.S3_URL
        logo = ''.join([staticpath, 'images/weaselogo.jpg'])
        img = Image(logo, width=2*inch, height=.5*inch)
        elements.append(img)
        #elements.append(Paragraph('<img src="'+logo+'" height="5"/>', styles['RightAlign']))
        elements.append(Paragraph(obj.order_company.name, styles['LeftAlign']))
        elements.append(Paragraph(obj.order_company.company_address.street_addr1, styles['LeftAlign']))
        elements.append(Paragraph(obj.order_company.company_address.street_addr2, styles['LeftAlign']))
        elements.append(Paragraph(obj.order_company.company_address.city+", "+obj.order_company.company_address.country+" "+obj.order_company.company_address.post_code, styles['LeftAlign']))
        elements.append(Paragraph(obj.order_company.company_address.phone_main, styles['LeftAlign']))
        elements.append(Spacer(1,0.2*inch))
        elements.append(Paragraph('Details', styles['LeftAlign']))
        elements.append(Spacer(1,0.2*inch))
        elements.append(Paragraph(obj.order_created.strftime('%d %b, %Y'), styles['LeftAlign']))        
        elements.append(Paragraph('Created: '+obj.order_created.strftime('%d %b, %Y')+', by '+obj.order_created_by.first_name+' '+obj.order_created_by.last_name, styles['LeftAlign']))        
        elements.append(Paragraph('Request #: '+obj.order_number+'v/'+str(obj.order_version), styles['LeftAlign']))
        elements.append(Paragraph('Reference #: '+obj.reference_number, styles['LeftAlign']))
        elements.append(Spacer(1,0.2*inch))
        elements.append(Paragraph('Delivery Address', styles['LeftAlign']))
        elements.append(Paragraph(obj.delivery_address.addr_location, styles['LeftAlign']))
        elements.append(Paragraph(obj.delivery_address.street_addr1, styles['LeftAlign']))
        elements.append(Paragraph(obj.delivery_address.street_addr2, styles['LeftAlign']))
        elements.append(Paragraph(obj.delivery_address.city+", "+obj.delivery_address.country+" "+obj.delivery_address.post_code, styles['LeftAlign']))
        elements.append(Paragraph(obj.delivery_address.phone_main, styles['LeftAlign']))
        elements.append(Spacer(1,0.2*inch))
        if 'PEN' in obj.order_status:
            for req in obj.req_order.all():
                elements.append(Paragraph(req.item_fam, styles['LeftAlign']))
                elements.append(Paragraph(req.item_subfam, styles['LeftAlign']))
                elements.append(Spacer(1,0.2*inch))
                for item in req.req_product.all():
                    elements.append(Paragraph(item.prod_title, styles['LeftAlign']))
                    elements.append(Paragraph(item.prod_details, styles['LeftAlign']))
                elements.append(Paragraph('Description :', styles['LeftAlign']))
                elements.append(Paragraph('     '+req.item_details, styles['LeftAlign']))
        else:
            # for ofr in obj.offer_order[0]:
            e = ' € '
            euro = e.decode('utf-8')
            if obj.order_status in ['OFR', 'APV', 'REF']:
                ord_type = 'Offer'
            else:
                ord_type = 'Order'
            for ofr in obj.offer_order.all():
                elements.append(Paragraph(ord_type+' Created: '+ofr.offer_created_by.first_name+' '+ofr.offer_created_by.last_name+' on '+ofr.offer_created.strftime('%d %b, %Y'), styles['LeftAlign']))
                elements.append(Paragraph(ofr.offer_domain, styles['LeftAlign']))
                elements.append(Spacer(1,0.2*inch))
                table_data = []
                #table_data.append(['#', 'Item', 'Details', 'Description'])
                for k, item in enumerate(ofr.offer_item.all()):
                    if item.delivery_date and item.date_start and item.date_end:
                        table_data.append(['Item : '+item.item_name, '', 'Delivery Date: '+item.delivery_date.strftime('%d %b, %Y')])
                        table_data.append(['Description: '+item.item_details, 'Start Date: '+item.date_start.strftime('%d %b, %Y'), 'End Date: '+item.date_end.strftime('%d %b, %Y')])
                    elif item.delivery_date and item.date_start and not item.date_end:
                        table_data.append(['Item: '+item.item_name, '', ''])
                        table_data.append(['Description: '+item.item_details, 'Delivery Date: '+item.delivery_date.strftime('%d %b, %Y'), 'Start Date: '+item.date_start.strftime('%d %b, %Y')])
                    elif item.delivery_date and item.date_end and not item.date_start:
                        table_data.append(['Item: '+item.item_name, '', ''])
                        table_data.append(['Description: '+item.item_details, 'Delivery Date: '+item.delivery_date.strftime('%d %b, %Y'), 'End Date: '+item.date_end.strftime('%d %b, %Y')])
                    elif item.delivery_date and not item.date_end and not item.date_start:
                        table_data.append(['Item: '+item.item_name, '', ''])
                        table_data.append(['Description: '+item.item_details, 'Delivery Date: '+item.delivery_date.strftime('%d %b, %Y'), ''])
                    else :
                        table_data.append(['Item: '+item.item_name, '', ''])
                        table_data.append(['Description: '+item.item_details, '', ''])
                    table_data.append(['Quantity: '+str(item.quantity), euro+str(item.price), 'Sub Total: '+euro+str(item.item_sub_total)])
                    elements.append(Spacer(1,0.2*inch))
                    order_table = Table(table_data, colWidths=[doc.width/3.0]*3)
                    order_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
                elements.append(order_table)
                elements.append(Spacer(1,0.2*inch))
                elements.append(Paragraph(ord_type+'Terms :'+ofr.offer_terms, styles['LeftAlign']))
                elements.append(Paragraph(ord_type+' Total: '+euro+ofr.offer_total, styles['RightAlign']))

        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)
 
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
 
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 
    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(200 * mm, 15 * mm + (0.2 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))

