from datetime import date
from django.db import models
import uuid

class Currency(models.Model):
    iso_code = models.CharField(max_length=3, primary_key=True)
    country_of_issue = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.iso_code

class Instrument(models.Model):
    iid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    name= models.CharField(max_length=50)
    ticker= models.CharField(max_length=50)  
    instrument_type= models.CharField(max_length=50)
    start_date=models.DateField(null=True,blank=True) 
    end_date=models.DateField(null=True,blank=True)

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,related_name="instruments")

    def __str__(self):
        return self.ticker

class Company(models.Model):
    cid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    ticker = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=50)
    sector= models.CharField(max_length=50)
    industry= models.CharField(max_length=50)

    def __str__(self):
        return self.name 
    
class Equity(models.Model):
    iid = models.OneToOneField(Instrument, on_delete=models.CASCADE, primary_key=True)
    cid = models.ForeignKey(Company,on_delete=models.CASCADE, related_name="equities")

class FX(models.Model):
    iid = models.OneToOneField(Instrument, on_delete=models.CASCADE,primary_key=True)
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="fx_base")
    quote_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="fx_quote")


class ETF(models.Model):
    # etf_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    iid = models.OneToOneField(Instrument, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f"ETF({self.iid.ticker})"
    
class ETFConstituent(models.Model):
    const_id = models.BigAutoField(primary_key=True)
    etf = models.ForeignKey(ETF, on_delete=models.CASCADE, related_name="constituents")
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE,related_name="included_in_etfs")
    start_date=models.DateField()
    end_date=models.DateField()
    weight = models.DecimalField(max_digits=1,decimal_places=6)
    

class PriceAction(models.Model):
    price_id = models.BigAutoField(primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name="prices")

    price_timestamp=models.DateTimeField(db_index=True)
    price_open =models.DecimalField(max_digits=15,decimal_places=2)
    price_high =models.DecimalField(max_digits=15,decimal_places=2)
    price_low =models.DecimalField(max_digits=15,decimal_places=2)
    price_close=models.DecimalField(max_digits=15,decimal_places=2)
    volume=models.DecimalField(max_digits=15,decimal_places=2,null=True)

class FinancialStatement(models.Model):
    statement_id = models.BigAutoField(primary_key=True)
    cid = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="statements")
    statement_type= models.CharField(max_length=50)
    period_type=models.CharField(max_length=50)
    fiscal_year=models.IntegerField() # does this need more specification?
    statement_date=models.DateField() # does this need more specification?

class FinancialMetric(models.Model):
    metric_id = models.BigAutoField(primary_key=True)
    statement = models.ForeignKey(FinancialStatement,on_delete=models.CASCADE,related_name="metrics")
    cid = models.ForeignKey(Company,on_delete=models.CASCADE, related_name="metrics")
    metric_name = models.CharField(max_length=50)
    metric_value=models.DecimalField(max_digits=15,decimal_places=2)

class CorporateAction(models.Model):
    action_id=models.AutoField(primary_key=True)
    cid = models.ForeignKey(Company,on_delete=models.CASCADE)
    action_date=models.DateField(auto_now_add=True)
    action_type=models.CharField(max_length=50)
    value = models.DecimalField(max_digits=15,decimal_places=2)
    detail=models.CharField(max_length=50)