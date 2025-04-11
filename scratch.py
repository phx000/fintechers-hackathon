#%%
from openai import OpenAI
#%%
client = OpenAI(api_key="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")
#%%
response = client.responses.create(
    model="gpt-4o-mini",
    instructions="Your goal is to extract the needed information from the user's input. You will only fill in data that you are sure about. For example, if you are given Jose Antonio Maria Guzman as a name and you are NOT ABSOLUTELY SURE what is the first name what the last name and middle name, DO NOT POPULATE THE FIELDS WITH ANY NAMES, LEAVE IT AS BLANK. Perform basic validation on the user's input, for example, mike#gmail.com into mike@gmail.com, Cslifornia into California. Do not always take the user's input literally since they may be answering in an informal tone. The goal is to make the user's experience of filling out the form though you swift, so make intelligent and flexible decisions to make the user's experience as good as possible. Logically infer other fields even if they are not explicitly specified, like if a user says their address is in California, infer that the country is the United States. Do not be too strict about these guesses, PRIORITIZE USER EXPERIENCE OVER DATA QUALITY",
    input="I worked for amazon as a cloud infra tech lead. managed 20 people. left becase they didn pay enough. also worked for google as a junior soft eng. left because it wasnt of interest to me",
    text={
        "format": {
            "type": "json_schema",
            "name": "form_parser",
            "schema": {
                "type": "object",
                "properties": {
                    # "first_name": {"type": "string"},
                    # "last_name": {"type": "string"},

                    # "country": {"type": "string"},
                    # "state": {"type": "string"},
                    # "city": {"type": "string"},
                    # "address": {"type": "string"},
                    # "zip": {"type": "string"},

                    # "email": {"type": "string"},
                    # "country_code": {
                    #     "type": "string",
                    #     "description": "Phone number country code. For example, 1 for US, 34 for Spain"
                    # },
                    # "phone_number": {"type": "string"},

                    "employment_history": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "employer": {"type": "string"},
                                "start_date": {"type": "string", "description": "If no day of month provided, assume 1st. Hour always 0. return ISO string"},
                                "end_date": {"type": "string", "description": "If no day of month provided, assume 1st. Hour always 0. return ISO string"},
                                "responsibilities": {"type": "string"},
                                "reason_for_leaving": {"type": "string"},
                            },
                            "required": ["employer", "start_date", "end_date", "responsibilities", "reason_for_leaving"],
                            "additionalProperties": False
                        }
                    },

                    "comment": {
                        "type": "string",
                        "description": "Point out here any mistakes the user made regarding the mandatory fields. If no mistakes, leave as a blank string. Also, if you are unsure about the user's input, ask for a clarification here"
                    }
                },
                # "required": ["first_name", "last_name", "comment"],
                # "required": ["country", "state", "city", "address", "zip", "comment"],
                # "required": ["email", "country_code", "phone_number", "comment"],

                "required": ["employment_history","comment"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)
print(response.output_text)