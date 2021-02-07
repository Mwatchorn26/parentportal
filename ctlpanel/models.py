from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    is_child = models.BooleanField()
    #pwd = models.Password()
    email = models.EmailField()

    #def __str__(self):
    #    return self.name

class Device(models.Model):
    mac = models.CharField(max_length=17,verbose_name='MAC Address')
    ip = models.CharField(max_length=15,verbose_name='IP Address')
    hostname  = models.CharField(max_length=100,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    redirected = models.BooleanField(verbose_name='Controlled Right Now')
    RED    ='10'
    ORANGE ='5'
    YELLOW ='1'
    GREEN  ='0'
    LEVELS=[
            (RED,'Red - No Internet Access'),
            (ORANGE,'Orange - Some Content Blocked'),
            (YELLOW,'Yellow - Adult Content Blocked'),
            (GREEN,'Green - No Content Blocked'),
            ]
    control_level = models.CharField(max_length=2, choices=LEVELS, default=GREEN,)

    #def __str__(self):
    #    return self.hostname


class ManufacturerByMac(models.Model):
    mac = models.CharField(max_length=17,verbose_name='MAC Address')
    common_name = models.CharField(max_length=100, verbose_name="Manufacturer's Common Name")
    full_name = models.CharField(max_length=100, verbose_name="Manufacturer's Full Name")

    #def __str__(self):
    #    return self.common_name + " (" + mac + ")"

class SourceCategory(models.Model): #Streaming Media
    name = models.CharField(max_length=50, unique=True)
    
    #Games (AmongUs, Minecraft)
    #Streaming Media (Netflix, Hulu, Disney+, YouTube)
    #SocialMedia (TikTok, Facebook, Instagram, Twitter)
    #Adult Content(Porn Sites)
    #Illegal Downloading Sites
    #Educational (Google Classroom)
    #Conferencing (Zoom, WebEx, MS Teams, Google Meets)

    #def __str__(self):
    #    return self.name

class Source(models.Model): #Netflix
    domain = models.CharField(max_length=100)   #TikTok, Twitter, 
    port = models.PositiveIntegerField() #, max_value=65535)    #(Minecraft, AmongUs)
    category = models.ForeignKey(SourceCategory, on_delete=models.CASCADE) #Games, Social Media, Conferencing

    #def __str__(self):
    #    return self.category + " " + self.domain

class SourceSubdomain(models.Model):   # netflix.com
    source = models.ForeignKey(Source, on_delete=models.CASCADE) #source is Netflix
    subdomain = models.CharField(max_length=100) # subdomain searched in DNS query

    #def __str__(self):
    #    return self.subdomain

class DnsRecord(models.Model):      # netflix.com with ip address
    source_subdomain = models.ForeignKey(SourceSubdomain,on_delete=models.CASCADE)
    #name = models.CharField(max_length=100, verbose_name='DNS Name')
    ip = models.GenericIPAddressField('IP Address')
    date = models.DateTimeField()
    ttl = models.IntegerField()

    #def __str__(self):
    #    return self.source_subdomain.subdomain + " :\t" + self.ip

class SourceFilter(models.Model):
    categories=models.ManyToManyField(SourceCategory, blank=True)
    sources=models.ManyToManyField(Source, blank=True)
    

class Rule(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.CharField(max_length=13)
    source_filter = models.ManyToManyField(SourceFilter,blank=True)
    is_currently_active = models.BooleanField()
    is_enabled = models.BooleanField()
    DROP ='drop_'
    BLOCK='block'
    ALLOW='allow'
    ACTION_CHOICES=(
        (DROP,'Drop'),
        (BLOCK,'Block'),
        (ALLOW,'Allow'),
        )
    action = models.CharField(max_length=5, choices=ACTION_CHOICES, default=BLOCK,)
    
    #def daysOfWeekInText(self):
    #    days=""
    #    if len(self.days_of_week)>1:

    #        # weekdays as a tuple
    #        weekDays = ("Mon","Tues","Wed","Thur","Fri","Sat","Sun")
    #        array_of_days = [weekDays[x] for x in days_of_week.split(',')] 
    #        
    #        #array_of_days=[]
    #        #if '0' in self.days_of_week:
    #        #    array_of_days.append('Mon')
    #        #if '1' in self.days_of_week:
    #        #    array_of_days.append('Tues')
    #        #if '2' in self.days_of_week:
    #        #    array_of_days.append('Wed')
    #        #if '3' in self.days_of_week:
    #        #    array_of_days.append('Thur')
    #        #if '4' in self.days_of_week:
    #        #    array_of_days.append('Fri')
    #        #if '5' in self.days_of_week:
    #        #    array_of_days.append('Sat')
    #        #if '6' in self.days_of_week:
    #        #    array_of_days.append('Sun')
    #        days = ','.join(array_of_days)
    #    return days

    #def __str__(self):
    #    returnString = self.user.name
    #    
    #    returnString += " Starts at: " + self.start_time

    #    returnString += " Ends at: " + self.end_time

    #    returnString += " (" + self.daysOfWeekInText() + ") "

    #    returnString+= " Is"
    #    if self.is_enabled!=True:
    #        returnString= " NOT"
    #    returnString =  " enabled."
    #    
    #    returnString+= " Is"
    #    if self.is_currently_active!=True:
    #        returnString= " NOT"
    #    returnString =  " active right now."
    #    
    #    returnString += " " + self.action
    #    return self.user.name + " " + self.action

class NetworkInfo(models.Model):
    gateway = models.GenericIPAddressField('Gateway IP Address')
    active_interface = models.CharField(max_length=50)
    mywirelessIP = models.GenericIPAddressField('Wireless IP Address')
    mywiredIP = models.GenericIPAddressField('Wired IP Address')

