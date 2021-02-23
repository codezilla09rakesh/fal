import math, random

class OTP:
    # function to generate OTP
    def generateOTP(self):
        digits = "0123456789"
        OTP = ""
        # Here we generate 6 digit otp
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP