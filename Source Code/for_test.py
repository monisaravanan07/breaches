def DomainRegLen(self):
    try:
        expiration_date = self.whois_response.expiration_date
        creation_date = self.whois_response.creation_date
        try:
            if(len(expiration_date)):
                expiration_date = expiration_date[0]
        except:
            pass
        try:
            if(len(creation_date)):
                creation_date = creation_date[0]
        except:
            pass

        age = (expiration_date.year-creation_date.year)*12+ (expiration_date.month-creation_date.month)
        print(age   )
        if age >=12:
            return 1
        return -1
    except:
        return -1

DomainRegLen('https://www.google.com/search?q=flower+images&rlz=1C1RXQR_enIN1031IN1033&oq=flow&aqs=chrome.1.69i57j0i433i512l2j0i131i433i512j0i512j0i131i433i512j0i433j0i512j46i199i433i465i512j0i433.2610j0j7&sourceid=chrome&ie=UTF-8')