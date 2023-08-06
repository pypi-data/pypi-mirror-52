class WeatherDetails:
    def __init__(self,city,queryType,date):
        self.city = city
        self.queryType = queryType
        self.year = date['year']
        self.month = date['month']
        self.date = date['date']
        # Get City Details
        url = "https://api.weather.com/v3/location/search?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&language=en-IN&locationType=locale&query="+city
        cityDetails = requests.get(url)
        # Convert json object to dicitonary
        cityDetailsDatastore = json.loads(cityDetails.text)
        self.cityNameInWebsite=cityDetailsDatastore['location']['address'][0]
        self.cityIDInWebsite=cityDetailsDatastore['location']['placeId'][0]
        # print(self.cityNameInWebsite)
        # print(self.cityIDInWebsite)
        # Get latitude and longitude
        latitudeAndLongitudeURL="https://api.weather.com/v3/location/point?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&language=en-IN&placeid="+self.cityIDInWebsite
        self.cityLocationDetails = requests.get(latitudeAndLongitudeURL)
        # convert city location details to python dictionary 
        self.cityLocationDetailsDatastore=json.loads(self.cityLocationDetails.text)
        self.cityLatitude = format(round(self.cityLocationDetailsDatastore["location"]["latitude"],2),'0.2f')
        self.cityLongitude = format(round(self.cityLocationDetailsDatastore["location"]["longitude"],2),'0.2f')
        # print("Latitude: " + self.cityLatitude)
        # print("Longitude: " + self.cityLongitude)
        # self.driverCodeBasedOnQuerySelector()
        

    def driverCodeBasedOnQuerySelector(self):
        if self.queryType == None:
            # print("======================================================")
            try:
                res = self.dailyData()
                return res
            except:
                # print("ERROR: Kindly provide proper inputs")
                error = 'ERROR: Kindly provide proper inputs'
                return error
        elif self.queryType == 'daily-data':
            # print("======================================================")
            try:
                res=self.dailyData()
                return res
            except:
                # print("ERROR: Kindly provide proper inputs")
                error = 'ERROR: Kindly provide proper inputs'
                return error
        elif self.queryType == 'ten-days-data':
            # print("======================================================")
            try:
                res = self.tenDayData()
                return res
            except:
                # print("ERROR: Kindly provide proper inputs")
                error = 'ERROR: Kindly provide proper inputs'
                return error
        elif self.queryType == 'particular-date-data':
            # print("======================================================")
            try:
                res = self.pastDateData()
                return res
            except:
                # print("ERROR: Kindly provide proper inputs")
                error = 'ERROR: Kindly provide proper inputs'
                return error
        elif self.queryType == 'hourly-data':
            # print("======================================================")
            try:
                res = self.hourlyDetailsData()
                return res
            except:
                # print("ERROR: Kindly provide proper inputs")
                error = 'ERROR: Kindly provide proper inputs'
                return error
        elif self.queryType == 'monthly-data':
            # print("======================================================")
            try:
                res = self.monthDetailsData()
                return res
            except:
                # print("ERROR: Kindly provide proper inputs")
                error = 'ERROR: Kindly provide proper inputs'
                return error

    def tenDayData(self):
        cityLatitude = self.cityLatitude
        cityLongitude = self.cityLongitude
        tenDayDataURL="https://api.weather.com/v2/turbo/vt1dailyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode="+cityLatitude+"%2C"+cityLongitude+"&language=en-IN&units=m"
        weatherDetails = requests.get(tenDayDataURL)
        # # print(weatherDetails.text)
        weatherDetails = json.loads(weatherDetails.text)
        # # print(weatherDetails)
        weatherDetails['city']=self.cityNameInWebsite
        weatherDetails['longitude']=cityLongitude
        weatherDetails['latitude']=cityLatitude
        weatherDetails['weather.comCityCode']=self.cityIDInWebsite
        weatherDetails = json.dumps(weatherDetails)
        # print(weatherDetails)
        return weatherDetails

    def dailyData(self):
        cityLatitude = self.cityLatitude
        cityLongitude = self.cityLongitude
        # Get Weather details:
        weatherDetailsURL = "https://api.weather.com/v2/turbo/vt1observation?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode="+cityLatitude+"%2C"+cityLongitude+"&language=en-IN&units=m"
        weatherDetails = requests.get(weatherDetailsURL)
        # # print(weatherDetails.text)
        weatherDetails = json.loads(weatherDetails.text)
        weatherDetails['city']=self.cityNameInWebsite
        weatherDetails['longitude']=cityLongitude
        weatherDetails['latitude']=cityLatitude
        weatherDetails['weather.comCityCode']=self.cityIDInWebsite
        # # print(weatherDetails)
        weatherDetails = json.dumps(weatherDetails)
        # print(weatherDetails)
        return weatherDetails

    def pastDateData(self):
        date = self.year+self.month+self.date 
        cityLatitude = self.cityLatitude
        cityLongitude = self.cityLongitude
        pastDateURL = "https://dsx.weather.com/wxd/v2/PastObsAvg/en_IN/"+str(date)+"/35/"+cityLatitude+","+cityLongitude+"?api=7bb1c920-7027-4289-9c96-ae5e263980bc"
        # # print(pastDateURL)
        weatherDetails = requests.get(pastDateURL)
        # # print(weatherDetails.text)
        weatherDetails = json.loads(weatherDetails.text)
        weatherDetailsRequired = weatherDetails[0]
        weatherDetailsRequired['city']=self.cityNameInWebsite
        weatherDetailsRequired['longitude']=cityLongitude
        weatherDetailsRequired['latitude']=cityLatitude
        weatherDetailsRequired['weather.comCityCode']=self.cityIDInWebsite
        # # print(weatherDetails)
        weatherDetails = json.dumps(weatherDetailsRequired)
        # print(weatherDetails)
        return weatherDetails

    def hourlyDetailsData(self):
        cityLatitude = self.cityLatitude
        cityLongitude = self.cityLongitude
        hourlyDetailsURL="https://api.weather.com/v2/turbo/vt1hourlyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode="+cityLatitude+"%2C"+cityLongitude+"&language=en-IN&units=m"
        weatherDetails = requests.get(hourlyDetailsURL)
        # # print(weatherDetails.text)
        weatherDetails = json.loads(weatherDetails.text)
        weatherDetails['city']=self.cityNameInWebsite
        weatherDetails['longitude']=cityLongitude
        weatherDetails['latitude']=cityLatitude
        weatherDetails['weather.comCityCode']=self.cityIDInWebsite
        # # print(weatherDetails)
        weatherDetails = json.dumps(weatherDetails)
        # print(weatherDetails)
        return weatherDetails

    def monthDetailsData(self):
        cityLatitude = self.cityLatitude
        cityLongitude = self.cityLongitude
        today = date.today()
        ddStart=today.strftime("%d")
        mmStart=today.strftime("%m")
        dateStart = mmStart+ddStart
        # print('DateStart: ' + dateStart)

        ddEnd = ddStart
        mmStart = int(mmStart)
        mmEnd = mmStart + 1
        if mmEnd < 10:
            mmEnd = '0'+str(mmEnd)
        else:
            mmEnd = str(mmEnd)
        dateEnd = mmEnd+ddEnd
        # print("DateEnd: " + dateEnd)
        monthDetailsURL="https://api.weather.com/v1/geocode/"+ cityLatitude +"/" + cityLongitude +"/almanac/daily.json?apiKey=d522aa97197fd864d36b418f39ebb323&end="+dateEnd+"&start="+dateStart+"&units=m"
        weatherDetails = requests.get(monthDetailsURL)
        weatherDetails = json.loads(weatherDetails.text)
        weatherDetails['city']=self.cityNameInWebsite
        weatherDetails['longitude']=cityLongitude
        weatherDetails['latitude']=cityLatitude
        weatherDetails['weather.comCityCode']=self.cityIDInWebsite
        # # print(weatherDetails)
        weatherDetails = json.dumps(weatherDetails)
        # print(weatherDetails)
        return weatherDetails

