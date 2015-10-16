# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_unicode
from authentication.models import Account, Company, Address
from django.core.files.storage import default_storage
from time import time
from wease import settings

def get_upload_file_name(instance, filename):
    return settings.UPLOAD_FILE_PATTERN % (str(time()).replace('.','_'), filename)

class Good(models.Model):
	domain = models.CharField(max_length=50, null=True, blank=True)
	family = models.CharField(max_length=50, null=True, blank=True)
	subfamily = models.CharField(max_length=50, null=True, blank=True)

	def __unicode__(self):
		return smart_unicode("domain: %s, family: %s, subfamily: %s" % (self.domain, self.family, self.subfamily))


class Detail(models.Model):
	good = models.ForeignKey(Good, related_name='good_detail')
	good_info = models.CharField(max_length=200, null=True, blank=True)	
	good_description = models.CharField(max_length=250, null=True, blank=True)


	def __unicode__(self):
		return smart_unicode("%s, # %s" % (self.good, self.id))	


class Order(models.Model):
    WAITING_REQUEST = 'WRQ'
    PENDING = 'PEN'
    OFFER = 'OFR'
    VALIDATED = 'VAL'
    REFUSED = 'REF'
    APPROVED = 'APV'
    COMPLETED = 'COM'
    INVOICED = 'INV'
    CANCELED = 'CAN' 
    ARCHIVED = 'ARC'   
    REQUEST_SUBMITTED = 'RSB'
    APPROVE_REQUEST = 'APR'
    APPROVE_OFFER = 'APO'
    APPROVAL_NEEDED = 'APN'
    OFFER_SUBMITTED = 'OSB'
    NOT_APPROVED = 'NAP'
    RETURNED = 'RET'
    IN_PROGRESS = 'INP'
    BACKORDER = 'BOR'

    ORDER_STATUS = (
        (WAITING_REQUEST, 'Demandes en attente'),
        (PENDING, 'Demandes à traiter'),
        (OFFER, 'Offre disponible'),
        (VALIDATED, 'Commande à traiter'),
        (REFUSED, 'Refusé'),
        (APPROVED, 'Approuvé'),
        (COMPLETED, 'Completed'),
        (INVOICED, 'Invoiced'),
        (CANCELED, 'Annulé'), 
        (ARCHIVED, 'Archived'),       
        (REQUEST_SUBMITTED, 'Request Submitted'),
        (APPROVAL_NEEDED, 'Approval Needed'),
        (OFFER_SUBMITTED, 'Optiz Offer Submitted'),
        (NOT_APPROVED, 'Not Approved'),
        (RETURNED, 'Returned'),
        (IN_PROGRESS, 'In Progress'),
        (BACKORDER, 'Backorder'),
    )
    OPTIZ_STATUS = ( 
        (WAITING_REQUEST, 'Demande en attente'),
        (PENDING, 'Demande à traiter'),
        (OFFER, 'Offre disponible'),
        (VALIDATED, 'Commande à traiter'),
        (REFUSED, 'Refusé'),
        (APPROVED, 'Approuvé'),
        (COMPLETED, 'Commandes à facturer'),
        (INVOICED, 'Invoiced'),
        (CANCELED, 'Annulé'),
        (ARCHIVED, 'Archived'),             
        (OFFER_SUBMITTED, 'Offer Submitted'),
        (NOT_APPROVED, 'Not Approved'),
        (RETURNED, 'Returned'),
        (IN_PROGRESS, 'In Progress'),
        (BACKORDER, 'Backorder'),
    )
    COMP_STATUS = (
        (WAITING_REQUEST, 'Demande en attente'),
        (PENDING, 'Demande en cours de traitement'),
        (OFFER, 'Offre disponible'),
        (VALIDATED, 'Commande validée'),
        (REFUSED, 'Refusé'),
        (APPROVED, 'Approuvé'),
        (COMPLETED, 'Commande finalisée'),
        (INVOICED, 'Invoiced'),
        (CANCELED, 'Annulé'),  
        (ARCHIVED, 'Archived'),  
        (REQUEST_SUBMITTED, 'Request Submitted'),
        (APPROVE_REQUEST, 'Request Approved'),
        (APPROVAL_NEEDED, 'Approval Needed'),
        (APPROVE_OFFER, 'Offer Approved'),
        (NOT_APPROVED, 'Not Approved'),
        (RETURNED, 'Returned'),
    )
    order_company = models.ForeignKey(Company, null=True, blank=True, related_name='order_company')    
    order_draft = models.BooleanField(default=False)
    order_number = models.CharField(max_length=50, null=True, blank=True)
    order_version = models.SmallIntegerField(null=True, blank=True)
    offer_version = models.SmallIntegerField(null=True, blank=True, default=00)
    order_offer = models.BooleanField(default=False)
    reference_number = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    order_total = models.CharField(max_length=50, null=True, blank=True)
    delivery_address = models.ForeignKey(Address, null=True, blank=True, related_name='company_address')
    order_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    order_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_created_user', null=True, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_modified_by', null=True, blank=True)
    modified_by_date = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)
    order_status = models.CharField(max_length=3, choices=ORDER_STATUS, default=WAITING_REQUEST)
    order_status_change_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_status_changed_by', null=True, blank=True)
    order_status_change_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    company_approval_status = models.CharField(max_length=3, choices=COMP_STATUS, default=PENDING)    
    company_approval_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_approved_by', null=True, blank=True)
    company_approval_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    optiz_status = models.CharField(max_length=3, choices=OPTIZ_STATUS, default=PENDING)
    optiz_status_change_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='optiz_approved_by', null=True, blank=True)
    optiz_status_change_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def __unicode__(self):
        return smart_unicode("%s" % (self.id))

class ReqItem(models.Model):
    order = models.ForeignKey(Order, related_name='req_order')
    good = models.ForeignKey(Good, related_name='req_good')
    req_domain = models.CharField(max_length=250, null=True, blank=True)
    item_fam = models.CharField(max_length=250, null=True, blank=True)
    item_subfam = models.CharField(max_length=250, null=True, blank=True)
    item_details = models.TextField(null=True, blank=True) 
    req_item_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    req_item_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='req_item_modified_user', null=True, blank=True)
    req_item_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    req_item_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='req_item_created_user', null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.order.order_number)

    def get_order_num(self):
        return self.order.order_number

    def get_order_company(self):
        return self.order.order_company

class ReqProduct(models.Model):
    req_item = models.ForeignKey(ReqItem, related_name='req_product')   
    prod_fam = models.CharField(max_length=250, null=True, blank=True)
    prod_subfam = models.CharField(max_length=250, null=True, blank=True)    
    prod_title = models.CharField(max_length=250, null=True, blank=True)
    prod_details = models.CharField(max_length=250, null=True, blank=True, default='NONE')
    prod_description = models.CharField(max_length=250, null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.req_item)

class ReqFile(models.Model):
    req_item = models.ForeignKey(ReqItem, related_name='req_item_file', blank=True, null=True)
    file_created = models.DateTimeField(auto_now=True)
    req_file = models.FileField(upload_to=get_upload_file_name, null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.req_item)   

class Offer(models.Model):
    REFUSED = 'REF'
    APPROVED = 'APV'
    WAITING_APPROVAL = 'WAP'
    OFFER_STATUS = ( 
        (REFUSED, 'Refusé'),
        (APPROVED, 'Approuvé'),
        (WAITING_APPROVAL, 'Waiting Approval'),
    )
    order = models.ForeignKey(Order, related_name='offer_order')
    offer_version = models.SmallIntegerField(null=True, blank=True)
    offer_domain = models.CharField(max_length=250, null=True, blank=True)
    offer_total = models.CharField(max_length=50, null=True, blank=True)
    offer_terms = models.TextField(null=True, blank=True)
    offer_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='offer_created_by')
    offer_created = models.DateTimeField(auto_now_add=True)
    offer_approval_status = models.CharField(max_length=3, choices=OFFER_STATUS, default=WAITING_APPROVAL)
    offer_approval_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='offer_updated_by')
    offer_approval = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    class Meta:
        ordering = ['-offer_created']

    def __unicode__(self):
        return smart_unicode(self.order.order_number)

    def get_order_num(self):
        return self.order.order_number

    def get_order_company(self):
        return self.order.order_company

class OfferItem(models.Model):
    offer = models.ForeignKey(Offer, related_name='offer_item')
    item_name = models.CharField(max_length=250, null=True, blank=True)
    item_details = models.TextField(null=True, blank=True)      
    price = models.CharField(max_length=50, null=True, blank=True)
    item_sub_total = models.CharField(max_length=50, null=True, blank=True)
    frequency = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.SmallIntegerField(null=True, blank=True)
    delivery_date = models.DateTimeField(max_length=50, null=True, blank=True)
    date_start = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    date_end = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.offer)
    
class Comment(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wease_user', unique=False)
    order = models.ForeignKey(Order, related_name='order_comment')
    created_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    
    def __unicode__(self):
        return smart_unicode(self.created_date)
