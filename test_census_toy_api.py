import requests
import unittest
import random
import string
BASE_URL = "https://census-toy.nceng.net/prod/toy-census"

class TestCensusToyAPI(unittest.TestCase):
    
    # Generate random genders and countries using the randomuser.me API
    @classmethod
    def setUpClass(cls):
        cls.genders = []
        cls.countries = []
        for i in range(10):
            response = requests.get("https://randomuser.me/api/")
            data = response.json()["results"][0]
            cls.genders.append(data["gender"])
            cls.countries.append(data["location"]["country"])

    # Test the CountByGender action
    def test_count_by_gender(self):
        # Send a POST request to the Census Toy API with random genders
        payload = {
            "actionType": "CountByGender",
            "users": [{"gender": gender} for gender in self.genders]
        }
        response = requests.post(BASE_URL, json=payload)
        data = response.json()

        # Check that the response is successful and the output is sorted by value
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(data[i]["value"] >= data[i+1]["value"] for i in range(len(data)-1)))

    # Test the CountByCountry action
    def test_count_by_country(self):
        # Send a POST request to the Census Toy API with random countries
        payload = {
            "actionType": "CountByCountry",
            "users": [{"location": {"country": country}} for country in self.countries]
        }
        response = requests.post(BASE_URL, json=payload)
        data = response.json()

        # Check that the response is successful and the output is sorted by value
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(data[i]["value"] >= data[i+1]["value"] for i in range(len(data)-1)))

    def test_count_password_complexity_non_alpha(self):
        num = random.randint(1,100000)
        password = string.punctuation + str(num)
        payload = {
            "actionType": "CountPasswordComplexity",
            "users": [{"login": {"password": password}}]
        }
        response = requests.post(BASE_URL, json=payload)
        data = response.json()
        # Check that the response is successful and the output length matches the set length of complexity
        self.assertEqual(response.status_code, 200)
        self.assertEqual((data[0]["value"]), len(password))

    def test_count_password_complexity_alpha(self):
        password = random.choice(string.ascii_letters)
        payload = {
            "actionType": "CountPasswordComplexity",
            "users": [{"login": {"password": password}}]
        }
        response = requests.post(BASE_URL, json=payload)
        data = response.json()
        # Check that the response is successful and the output length matches the set length of complexity
        self.assertEqual(response.status_code, 200)
        self.assertEqual((data[0]["value"]), 0)

    def test_verify_result_count_for_top_value(self):
        num = random.randint(1,10)
        payload = {
            "actionType": "CountByGender",
            "top" : str(num),
            "users": [{"gender": gender} for gender in self.genders]
            
        }
        response = requests.post(BASE_URL, json=payload)
        data = response.json()
        # Check that the response is successful and the output length matches the set length of complexity
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(str(data[0]["value"])), 10)

    def test_missing_payload(self):
        response = requests.post(BASE_URL)
        # Check that the response fail and displays 400 with missing payload
        self.assertEqual(response.status_code, 400)
    
    def test_missing_mandatory_values_payload(self):
        #I would rather have this payload json in a file to read in and append values as needed, but I could not get this to work in time
        payload = {
            "actionType": "",
            "top": 50,
            "users": [
                {
                    "gender": "male",
                    "name": {
                        "title": "",
                        "first": "",
                        "last": ""
                    },
                    "location": {
                        "street": "",
                        "city": "",
                        "state": "",
                        "postcode": 3294
                    },
                    "email": "",
                    "login": {
                        "username": "",
                        "password": "aaaaa",
                        "salt": "fYBp4g4a",
                        "md5": "",
                        "sha1": "",
                        "sha256": ""
                    },
                    "dob": "1956-09-17 02:13:36",
                    "registered": "2009-05-03 14:40:51",
                    "phone": "00-3540-6154",
                    "cell": "0498-678-691",
                    "id": {
                        "name": "TFN",
                        "value": "377488473"
                    },
                    "picture": {
                        "large": "https://randomuser.me/api/portraits/women/38.jpg",
                        "medium": "https://randomuser.me/api/portraits/med/women/38.jpg",
                        "thumbnail": "https://randomuser.me/api/portraits/thumb/women/38.jpg"
                    },
                    "nat": "AU"
                }
            ]
        }
#would like to read in json and append here before sending out payload in request
        # listObj = json.load(payload)
        # listObj.append({"actionType": ""})
        response = requests.post(BASE_URL, json= payload)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()