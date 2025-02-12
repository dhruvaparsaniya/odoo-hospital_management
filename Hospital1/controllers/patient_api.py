import xmlrpc.client
import requests
from odoo import http
from odoo.http import request
import re


def validate_fields(name, email, gender, user_type, mobile_no='0000000000', gov_id='000000000000',
                    birthdate="2003-01-28", physician_speciality='Dermatology'):
    pattern_name = r"^[a-zA-Z ]{2,}$"
    if not re.match(pattern_name, name):
        return {"error": "Invalid name. Name should only contain letters and spaces."}

    pattern_email = r'^[a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,4}$'
    if not re.match(pattern_email, email):
        return {"error": "Invalid email. Please enter a valid email address (format: example@domain.com)"}

    if gender not in ["male", "female"]:
        return {"error": "Invalid gender. Gender can only be 'male' or 'female'."}

    if user_type not in ["patient", "physician"]:
        return {"error": "Invalid user type. User type must be 'patient' or 'physician'."}

    pattern_mobile = r'^\d{10}$'
    if not re.match(pattern_mobile, mobile_no):
        return {"error": "Invalid mobile number. It should contain 10 digits."}

    if user_type == "physician" and not physician_speciality:
        return {"error": "Please enter speciality ex( Dermatology, Cardiologist, Emergency medicine,Psychiatry)"}

    if user_type == "patient" and not gov_id:
        return {"error": "Please enter government ID."}

    if user_type == "patient" and not birthdate:
        return {"error": "Please enter birthdate."}

    return True


def get_user_data(name, email, gender, user_type):
    validated_data = validate_fields(name, email, gender, user_type)
    if validated_data == True:
        if user_type == "patient":
            state = "active"
            active_user = request.env['hospital.patient'].sudo().search([("state", "=", state)])
            user = active_user.search(
                [("name", "=", name), ("email", "=", email), ("gender", "=", gender), ])
            if not user:
                return {"error": "User not found"}
            else:
                response_data = {
                    "status": "success",
                    "value": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "mobile no.": user.mobile_number,
                        "age": user.patient_age,
                        "gender": user.gender
                    }
                }
                return response_data
        elif user_type == "physician":
            user = request.env['hospital.physician'].sudo().search(
                [("name", "=", name), ("email", "=", email), ("gender", "=", gender)])
            if not user.name:
                return {"error": "User name not found"}
            else:
                response_data = {
                    "status": "success",
                    "value": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "gender": user.gender,
                        "mobile no.": user.mobile_number,
                        "speciality": user.physician_specialty.name
                    }
                }
                return response_data
        else:
            return {"error": "Invalid user_type"}
    else:
        return validated_data


def create_users(name, email, gender, mobile_no, gov_id, birthdate, physician_speciality, user_type):
    company = request.env['res.company'].sudo().search([('name', '=', 'My Company')])
    if user_type == "patient":
        validated_data = validate_fields(name=name, email=email, gender=gender, mobile_no=mobile_no,
                                         birthdate=birthdate, gov_id=gov_id, user_type=user_type)
        if validated_data == True:
            request.env['hospital.patient'].sudo().create({
                "patient_name": name,
                "email": email,
                "gender": gender,
                "mobile_number": mobile_no,
                "date_of_birth": birthdate,
                "gov_identity": gov_id,
                "state": "active",
                'company_ids': [(4, company.id)],
                'company_id': company.id,
            })
            return {"patient created successfully"}
        else:
            return validated_data

    elif user_type == "physician":
        validated_data = validate_fields(name=name, email=email, gender=gender, mobile_no=mobile_no,
                                         user_type=user_type, physician_speciality=physician_speciality)
        if validated_data == True:
            physician_speciality = physician_speciality.split(',')
            speciality_id = request.env['hospital.speciality'].sudo().search([('name', 'in', physician_speciality)]).ids
            request.env['hospital.physician'].sudo().create({
                "physician_id": request.env['ir.sequence'].sudo().next_by_code("physician.data"),
                "physician_name": name,
                "email": email,
                "gender": gender,
                "mobile_number": mobile_no,
                'company_ids': [(4, company.id)],
                'company_id': company.id,
                'physician_specialty': [(6, 0, speciality_id)]
            })
            return {"physician created successfully"}
        else:
            return validated_data
    else:
        return {"error": "Invalid user_type"}


def update_user_data(user_id, name, email, gender, mobile_no, user_type, physician_speciality=""):
    validated_data = validate_fields(name=name, email=email, gender=gender, mobile_no=mobile_no, user_type=user_type)
    if True:
        if validated_data == True:
            if user_type == "patient":
                user = request.env['hospital.patient'].sudo().browse(user_id)
                if user.exists():
                    user.sudo().write({
                        "patient_name": name,
                        "email": email,
                        "gender": gender,
                        "mobile_number": mobile_no,
                    })
                    return {"patient updated successfully"}
                else:
                    return {"patient not found"}
            elif user_type == "physician":
                user = request.env['hospital.physician'].sudo().browse(user_id)
                if user:
                    user.sudo().write({
                        "physician_name": name,
                        "email": email,
                        "gender": gender,
                        "mobile_number": mobile_no,
                    })
                    return {"physician updated successfully"}
                else:
                    return {"physician not found"}
            else:
                return {"error": "Invalid user_type"}
        else:
            return validated_data


class UserApi(http.Controller):

    @http.route("/api/web/login", methods=["post"], type="json", auth="none")
    def authenticate_user(self, db, login, password):
        request.session.authenticate(db, login, password)
        user = request.env.user
        if not user:
            return {"error": "Invalid credentials"}

        return {
            "user_id": user.id,
            "user_name": user.name,
            "session_id": request.session.session_token,
            "message": "Login successful"
        }

    @http.route("/api/get_user", methods=["POST"], type="json", auth="user", csrf=False)
    def get_user(self, name, email, gender, user_type, **kwargs):
        user_type = user_type.lower()
        if not user_type:
            return {"error": "Please enter user type"}
        if not email:
            return {"error": "Please enter email"}
        if not name:
            return {"error": "Please enter name"}
        if not gender:
            return {"error": "Please enter gender"}
        return get_user_data(name, email, gender, user_type)

    @http.route("/api/create_user", methods=["POST"], type="json", auth="user", csrf=False)
    def create_user(self, name, email, gender, mobile_no, user_type, gov_id='', birthdate='', physician_speciality="",
                    **kwargs):
        user_type = user_type.lower()
        gender = gender.lower()
        if not user_type:
            return {"error": "Please enter user type"}
        if not name:
            return {"error": "Please enter name"}
        if not email:
            return {"error": "Please enter email"}
        if not gender:
            return {"error": "Please enter gender"}
        if not mobile_no:
            return {"error": "Please enter mobile number"}
        return create_users(name, email, gender, mobile_no, gov_id, birthdate, physician_speciality, user_type)

    @http.route("/api/update_user", methods=["POST"], type="json", auth="user", csrf=False)
    def update_user(self, user_id, name, email, gender, mobile_no, user_type, physician_speciality="", **kwargs):
        user_type = user_type.lower()
        gender = gender.lower()
        if not user_id:
            return {"error": "Please enter user id"}
        if not user_type:
            return {"error": "Please enter user type"}
        if not name:
            return {"error": "Please enter name"}
        if not email:
            return {"error": "Please enter email"}
        if not gender:
            return {"error": "Please enter gender"}
        if not mobile_no:
            return {"error": "Please enter mobile number"}

        return update_user_data(user_id, name, email, gender, mobile_no, user_type, physician_speciality="")

    @http.route("/api/change_state", methods=["POST"], type="json", auth="user", csrf=False)
    def change_state(self, user_id, **kwargs):
        user = request.env['hospital.patient'].sudo().browse(user_id)
        user.write({'state': 'inactivate'})

    @http.route("/api/search_physician", methods=["POST"], type="json", auth="user", csrf=False)
    def change_state(self, speciality, **kwargs):

        if not speciality:
            return {"error": "Speciality is required"}

        external_api_url = "https://67a9dadb65ab088ea7e4bae2.mockapi.io/physiciandata"
        response = requests.get(external_api_url)
        if response.status_code != 200:
            return {"error": "Failed to fetch data from external API"}

        physicians = response.json()
        filtered_doctors = [physician for physician in physicians if physician.get("speciality") == speciality]
        response = {"message": f"This is a list of physicians with speciality {speciality}, please select from this:",
                    "physicians": filtered_doctors}
        return response
