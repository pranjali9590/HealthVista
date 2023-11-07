from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Doctor, Patient, Prescription, passwordHasher, emailHasher
from django.db.models import Count, Q

# Create your views here.

def index(request):
    
    response = render(request,"healthcentre/index.html")
    return responseHeadersModifier(response)

def index1(request):

    response = render(request,"healthcentre/index1.html")
    return responseHeadersModifier(response)

def article(request):

    response = render(request,"healthcentre/article.html")
    return responseHeadersModifier(response)

def article_1(request):

    response = render(request,"healthcentre/article_1.html")
    return responseHeadersModifier(response)

def article_2(request):
   
    response = render(request,"healthcentre/article_2.html")
    return responseHeadersModifier(response)

def article_homepage(request):
   
    response = render(request,"healthcentre/article_homepage.html")
    return responseHeadersModifier(response)

def bmi(request):
    
    response = render(request,"healthcentre/bmi.html")
    return responseHeadersModifier(response)

def trys(request):
   
    response = render(request,"healthcentre/trys.html")
    return responseHeadersModifier(response)

def try1(request):
    
    response = render(request,"healthcentre/try1.html")
    return responseHeadersModifier(response)

def ov(request):
    
    response = render(request,"healthcentre/ov.html")
    return responseHeadersModifier(response)

def arti(request):
   
    response = render(request,"healthcentre/arti.html")
    return responseHeadersModifier(response)

def sp(request):
    
    response = render(request,"healthcentre/sp.html")
    return responseHeadersModifier(response)

def comm(request):
    
    response = render(request,"healthcentre/comm.html")
    return responseHeadersModifier(response)

def rem(request):
   
    response = render(request,"healthcentre/rem.html")
    return responseHeadersModifier(response)

def water(request):
    
    response = render(request,"healthcentre/water.html")
    return responseHeadersModifier(response)


def vegan(request):
    
    response = render(request,"healthcentre/vegan.html")
    return responseHeadersModifier(response)

def gluten(request):
    
    response = render(request,"healthcentre/gluten.html")
    return responseHeadersModifier(response)


def np1(request):
    
    response = render(request,"healthcentre/next-period-calculator.html")
    return responseHeadersModifier(response)

def mg(request):
   
    response = render(request,"healthcentre/memory-game.html")
    return responseHeadersModifier(response)

def main(request):
   
    response = render(request,"healthcentre/main.html")
    return responseHeadersModifier(response)


def register(request):
    
    if request.method == "GET":

        response =  render(request,"healthcentre/registrationPortal.html")
        return responseHeadersModifier(response)

    elif request.method == "POST":

        userFirstName = request.POST["userFirstName"]
        userLastName = request.POST["userLastName"]
        userEmail = request.POST["userEmail"]
        userRollNo = request.POST["userRollNo"]
        userAddress = request.POST["userAddress"]
        userContactNo = request.POST["userContactNo"]
        userPassword = request.POST["userPassword"]
        userConfirmPassword = request.POST["userConfirmPassword"]

        if userPassword == userConfirmPassword:

            name = userFirstName + " " + userLastName

            passwordHash = passwordHasher(userPassword)

            emailHash = emailHasher(userEmail)

            patient = Patient(name = name,rollNumber = userRollNo, email = userEmail, passwordHash = passwordHash, address = userAddress, contactNumber = userContactNo, emailHash = emailHash )
            patient.save()

            context = {
                "message":"User Registration Successful. Please Login."
            }

            response = render(request, "healthcentre/registrationPortal.html",context)
            return responseHeadersModifier(response)

        else:
            context = {
                "message":"Passwords do not match.Please register again."
            }

            response = render(request,"healthcentre/registrationPortal.html",context)
            return responseHeadersModifier(response)

    else:

        response = render(request,"healthcentre/registrationPortal.html")
        return responseHeadersModifier(response)


def doctors(request):
   
    context = {
        "doctors" : Doctor.objects.all()
    }

    response = render(request,"healthcentre/doctors.html",context)
    return responseHeadersModifier(response)


def login(request):
    
    request = requestSessionInitializedChecker(request)

    # If the request method is post
    if request.method == "GET":
        try:

            # If the user is already logged in inside of his sessions, and is a doctor, then no authentication required
            if request.session['isLoggedIn'] and request.session['isDoctor']:

                # Accessing the doctor user and all his/her records
                doctor = Doctor.objects.get(emailHash = request.session['userEmail'])
                records = doctor.doctorRecords.all()

                # Getting the count of the new prescriptions pending
                numberNewPendingPrescriptions = doctor.doctorRecords.aggregate(newPendingPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = False) ) ))['newPendingPrescriptions']

                # Storing the same inside the session variables
                request.session['numberNewPrescriptions'] = numberNewPendingPrescriptions

                # Storing the required information inside the context variable
                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp')
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"healthcentre/userDoctorProfilePortal.html", context)
                return responseHeadersModifier(response)

            # If the user is already logged in inside of his sessions, and is a patient, then no authentication required
            elif request.session['isLoggedIn'] and (not request.session['isDoctor']):

                # Accessing the patient user and all his/her records
                patient = Patient.objects.get(emailHash = request.session['userEmail'])
                records = patient.patientRecords.all()

                # Getting the count of the new prescriptions pending
                numberNewPrescriptions = patient.patientRecords.aggregate(newCompletedPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = True) ) ) )['newCompletedPrescriptions']

                # Storing the same inside the session variables
                request.session['numberNewPrescriptions'] = numberNewPrescriptions

                # Updating the completed records
                for record in records:
                    if record.isCompleted:
                        record.isNew = False
                        record.save()

                # Storing the required information inside the context variable
                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp')
                    }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"healthcentre/userPatientProfilePortal.html", context)
                return responseHeadersModifier(response)

            else:
                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"healthcentre/loginPortal.html")
                return responseHeadersModifier(response)

        # If any error occurs, sending back a new blank page
        except:

            # Editing response headers so as to ignore cached versions of pages
            response = render(request,"healthcentre/loginPortal.html")
            return responseHeadersModifier(response)

    # If the request method is post
    elif request.method == "POST":

        # Extracting the user information from the post request
        userName = request.POST["useremail"]
        userPassword = request.POST["userpassword"]

        # If such a patient exists
        try:
            patient = Patient.objects.get(email = userName)

            # Storing required session information
            request.session['isDoctor'] = False

        # Otherwise trying if a doctor exists
        except Patient.DoesNotExist:
            try:
                doctor = Doctor.objects.get(email = userName)

                # Storing required session information
                request.session['isDoctor'] = True

            # If no such doctor or patient exists
            except Doctor.DoesNotExist:

                # Storing message inside context variable
                context = {
                    "message":"User does not exist.Please register first."
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"healthcentre/loginPortal.html", context)
                return responseHeadersModifier(response)

        # Getting the hash of user inputted password
        passwordHash = passwordHasher(userPassword)

        # If the logged in user is a doctor
        if request.session['isDoctor']:

            # Accessing all records of doctor
            records = doctor.doctorRecords.all()

            # Getting the count of new prescriptions
            numberNewPendingPrescriptions = doctor.doctorRecords.aggregate(newPendingPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = False) ) ))['newPendingPrescriptions']

            # Storing the same inside request variable
            request.session['numberNewPrescriptions'] = numberNewPendingPrescriptions

            # If the inputted hash and the original user password hash match
            if passwordHash == doctor.passwordHash:

                # Storing required information in session variable of request
                request.session['isLoggedIn'] = True
                request.session['userEmail'] = doctor.emailHash
                request.session['Name'] = doctor.name

                # Redirecting to avoid form resubmission
                # Redirecting to home page
                # Editing response headers so as to ignore cached versions of pages
                response = HttpResponseRedirect(reverse('index'))
                return responseHeadersModifier(response)

            # Else if the password inputted is worng and doesn't match
            else:

                # Storing message inside context variable
                context = {
                    "message":"Invalid Credentials.Please Try Again."
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"healthcentre/loginPortal.html", context)
                return responseHeadersModifier(response)

        # Otherwise if the user is a patient
        else:

            # Accessing all records of patient
            records = patient.patientRecords.all()

            # Getting the count of new prescriptions
            numberNewPrescriptions = patient.patientRecords.aggregate(newCompletedPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = True) ) ))['newCompletedPrescriptions']

            # Storing the same inside request variable
            request.session['numberNewPrescriptions'] = numberNewPrescriptions

            # Updating the completed records
            for record in records:
                if record.isCompleted :
                    record.isNew = False
                    record.save()

            # If the inputted hash and the original user password hash match
            if passwordHash == patient.passwordHash:

                # Storing required information in session variable of request
                request.session['isLoggedIn'] = True
                request.session['userEmail'] = patient.emailHash
                request.session['Name'] = patient.name
                request.session['isDoctor'] = False

                # Redirecting to avoid form resubmission
                # Redirecting to home page
                # Editing response headers so as to ignore cached versions of pages
                response = HttpResponseRedirect(reverse('index'))
                return responseHeadersModifier(response)

            # Else if the password inputted is worng and doesn't match
            else:

                # Storing message inside context variable
                context = {
                    "message":"Invalid Credentials.Please Try Again."
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"healthcentre/loginPortal.html", context)
                return responseHeadersModifier(response)
    # For any other method of access, returning a new blank login page
    else:
        response = render(request,"healthcentre/loginPortal.html")
        return responseHeadersModifier(response)

def emergency(request):
    """ Funtion for emergency situations, for requesting an ambulance."""

    # If the request method is get
    if request.method == "GET":

        # Editing response headers so as to ignore cached versions of pages
        response = render(request,"healthcentre/emergencyPortal.html")
        return responseHeadersModifier(response)

    # If the request method is post and the user is submitting information
    elif request.method == "POST":

        # Extracting the emergency location from the post request
        emergencyLocation = request.POST['emergencyLocation']

        # Giving emergency message to server, can also be connected to IOT devices for alarms
        # If the emergency location text is not an empty string
        if emergencyLocation != "":

            # Printing information and notifying inside of server terminal
            print("------------------------------------------------------------------------")
            print("\n\nEMERGENCY !! AMBULANCE REQUIRED AT " + emergencyLocation + " !!\n\n")
            print("------------------------------------------------------------------------")

            # Storing information inside of context variable
            context = {
                "message" : "Ambulance reaching " + emergencyLocation + " in 2 minutes."
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request, "healthcentre/emergencyPortal.html", context)
            return responseHeadersModifier(response)

        # Else if the emergency location is an empty string
        else:

            # Storing message inside context variable
            context = {
                "message" : "No location entered.Invalid input."
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request, "healthcentre/emergencyPortal.html", context)
            return responseHeadersModifier(response)

    # For any other method of access, returning a new blank emergency page
    else:

        # Editing response headers so as to ignore cached versions of pages
        response = render(request,"healthcentre/emergencyPortal.html")
        return responseHeadersModifier(response)

def logout(request):
    """Function to log out the user."""
    # Erasing all the information of the session variables if user is logged out
    request.session['isDoctor'] = ""
    request.session['isLoggedIn'] = False
    request.session['userEmail'] = ""
    request.session['Name'] = ""
    request.session['numberNewPrescriptions'] = ""

    # Redirecting to avoid form resubmission
    # Redirecting to home page
    # Editing response headers so as to ignore cached versions of pages
    response = HttpResponseRedirect(reverse('login'))
    return responseHeadersModifier(response)

def contactus(request):
    """Function to display contact information."""

    # Editing response headers so as to ignore cached versions of pages
    response = render(request, "healthcentre/contactus.html")
    return responseHeadersModifier(response)

def onlineprescription(request):
    """Function to submit online prescription request to doctor."""

    # Calling session variables checker
    request = requestSessionInitializedChecker(request)

    # If the request method is get
    if request.method == "GET":

        # If the user is logged in
        if request.session['isLoggedIn']:

            # Portal only for patient prescription request submission, not for doctors
            if request.session['isDoctor']:

                # Storing message inside context variable
                context = {
                        "message":"Only for patients."
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request, "healthcentre/prescriptionPortal.html", context)
                return responseHeadersModifier(response)

            # If the user is a patient
            else:

                # Storing available doctors inside context variable
                context = {
                    "doctors" : Doctor.objects.all().order_by('specialization')
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request, "healthcentre/prescriptionPortal.html", context)
                return responseHeadersModifier(response)

        # If the user is not logged in
        else:

            # Storing message inside context variable
            context = {
                    "message":"Please Login First."
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request, "healthcentre/prescriptionPortal.html", context)
            return responseHeadersModifier(response)

    # If the user is posting the prescription request
    elif request.method == "POST":

        # Accepting only if the user is logged in
        if request.session['isLoggedIn']:

            # If the prescription is being submitted back by a doctor
            if request.session['isDoctor']:

                # Extracting information from post request
                prescriptionText = request.POST['prescription']

                # Updating the prescription and saving it
                prescription = Prescription.objects.get(pk = request.POST['prescriptionID'])
                prescription.prescriptionText = prescriptionText
                prescription.isCompleted = True
                prescription.isNew = True
                prescription.save()

                # Getting the records of the doctor
                records = Doctor.objects.get(emailHash = request.session['userEmail']).doctorRecords.all()

                # Storing required information inside context variable
                context = {
                    "user" : records,
                    "successPrescriptionMessage" : "Prescription Successfully Submitted."
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request, "healthcentre/userDoctorProfilePortal.html", context)
                return responseHeadersModifier(response)

            # Else if the patient is submitting prescription request
            else:

                # Extracting information from post request and getting the corresponding doctor
                doctor = Doctor.objects.get(pk = request.POST["doctor"])
                symptoms = request.POST["symptoms"]

                # Saving the prescription under the concerned doctor
                prescription = Prescription(doctor = doctor, patient = Patient.objects.get(emailHash = request.session['userEmail']), symptoms = symptoms)
                prescription.save()

                # Storing information inside context variable
                context = {
                    "successPrescriptionMessage" : "Prescription Successfully Requested.",
                    "doctors"  : Doctor.objects.all().order_by('specialization')
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request, "healthcentre/prescriptionPortal.html", context)
                return responseHeadersModifier(response)

        # Else if the user is not logged in
        else:

            # Storing information inside context variable
            context = {
                    "successPrescriptionMessage":"Please Login First.",
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request, "healthcentre/loginPortal.html", context)
            return responseHeadersModifier(response)

    # For any other method of access, returning a new blank online prescription page
    else:

        # Editing response headers so as to ignore cached versions of pages
        response = render(request, "healthcentre/prescriptionPortal.html")
        return responseHeadersModifier(response)

def responseHeadersModifier(response):
    """Funtion to edit response headers so that no cached versions can be viewed. Returns the modified response."""
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response

def requestSessionInitializedChecker(request):
    """Function to initialize request sessions if they don't exist."""

    # Try except for KeyError
    try:
        # Checking if session variables exist
        if request.session['isDoctor'] and request.session['isLoggedIn'] and request.session['userEmail'] and request.session['Name'] and request.session['numberNewPrescriptions']:
            # Do nothing if they do exist
            pass
    except:
        # Initialize request variables if they don't exist
        request.session['isDoctor'] = ""
        request.session['isLoggedIn'] = False
        request.session['userEmail'] = ""
        request.session['Name'] = ""
        request.session['numberNewPrescriptions'] = ""

    # Returning request
    return request