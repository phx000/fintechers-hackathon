import json

from flask import Flask, request, jsonify
from openai import OpenAI
from flask import send_from_directory
from prompts import JSON_INSTRUCTION, JSON_ADDITIONAL_INSTRUCTION,ENGLISH_INSTRUCTION, ENGLISH_ADDITIONAL_INSTRUCTION, FIRST_MESSAGE

app = Flask(__name__)

client = OpenAI(api_key="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")

# data = [
#     {
#         "first_name": {
#             "type": "string",
#         },
#         "last_name": {
#             "type": "string",
#         },
#     },
#     {
#         "country_code": {
#             "type": "string",
#             "description": "Phone number country code. For example, 1 for US, 34 for Spain"
#         },
#         "phone_number": {"type": "string"},
#     },
#     {
#         "country": {"type": "string"},
#         "state": {"type": "string"},
#         "city": {"type": "string"},
#         "address": {"type": "string"},
#         "zip": {"type": "string"},
#     }
# ]

data=[
  {
    "business_name": {
      "type": "string"
    },
    "legal_entity_type": {
      "type": "string",
      "enum": [
        "LLC",
        "Corporation",
        "Non-Profit",
        ""
      ]
    },
    "naics_code": {
      "type": "string",
      "description": "North American Industry Classification System code"
    }
  },
  {
    "date_of_registration": {
      "type": "string"
    },
    "address": {
      "type": "string",
      "description": "The geographical address."
    },
    "city": {
      "type": "string",
      "description": "City of the USA where the company was registered"
    },
    "state": {
      "type": "string",
      "description": "State of the USA where the company was registered. You should infer this information from the city if possible"
    }
  },
  {
    "beneficial_owners": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "full_name": {
            "type": "string"
          },
          "ownership_percentage": {
            "type": "number",
            "description": "Number from 1 to 100 representing the ownership percentage"
          },
          "role": {
            "type": "string"
          }
        },
        "required": [
          "full_name",
          "ownership_percentage",
          "role"
        ],
        "additionalProperties": False
      }
    }
  },
  {
    "account_type": {
      "type": "string",
      "description": "If the customer asks about which is best, you should instruct them according to our policies",
      "options": [
        "Checking",
        "Savings",
        "Brokerage"
      ]
    },
    "initial_deposit_amount": {
      "type": "number",
      "description": "If the customer asks about which is best, our policies recommend an initial deposit of $20,000"
    }
  }
]

def get_fields_without_value(block_index):
    return {key: value for key, value in data[block_index].items() if "value" not in value}

def extract_data(prompt, block_index):
    needed = get_fields_without_value(block_index)
    response = client.responses.create(
        model="gpt-4o-mini",
        # instruction=JSON_INSTRUCTION
        # input=prompt,
        input=[
            {
                 "role":"developer",
                 "content":JSON_INSTRUCTION
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "form_parser",
                "schema": {
                    "type": "object",
                    "properties": {
                        **needed,
                        "problems": {
                            "type": "string",
                            "description": JSON_ADDITIONAL_INSTRUCTION
                        }
                    },
                    "required": list(needed.keys())+["problems"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )
    return json.loads(response.output_text)


def get_english_message(block_index, problems):
    instructions = ENGLISH_INSTRUCTION
    # if problems:
    #     instructions = ENGLISH_ADDITIONAL_INSTRUCTION + f"{problems}"

    input_=[
        {
            "role":"developer",
            "content":instructions
        }
    ]

    if problems:
        input_.append({
            "role":"developer",
            "content":ENGLISH_ADDITIONAL_INSTRUCTION + f"{problems}"
        })

    input_.append({
        "role":"developer",
        "content":f"FIELDS: {json.dumps(get_fields_without_value(block_index))}"
    })


    response = client.responses.create(
        model="gpt-4o-mini",
        input=input_
        # instructions=instructions,
        # input=f"FIELDS: {json.dumps(get_fields_without_value(block_index))}",
        # input=[
        #     {
        #         "role":"developer",
        #         "content":instructions
        #     },
        #     {
        #         "role":"user",
        #         "content":prompt
        #     }
        # ],
    )
    return response.output_text


def update_data(extracted, block_index):
    for key, value in extracted.items():
        if key != "problems" and value:
            if type(value) == list:
                for kvpair in value:
                    if all(value for value in kvpair.values()):
                        data[block_index][key]["value"] = value
            else:
                data[block_index][key]["value"] = value


def is_block_complete(block_index):
    return all("value" in value for value in data[block_index].values())

def print_result():
    print("\n"*5)
    for block in data:
        for key, value in block.items():
            if type(value) == list:
                print(json.dumps(value, indent=4))
            else:
                print(f"{key}: {value['value']}")
    print("\n"*5)

@app.route('/')
def serve_chat():
    return send_from_directory('', 'index.html')

@app.route("/chat/start", methods=['POST'])
def start_chat():
    response = get_english_message(0, FIRST_MESSAGE)
    return jsonify({
        "response": response,
        "block_index": 0
    }), 200


@app.route("/chat", methods=['POST'])
def chat():
    request_data = request.get_json()  # this expects a 'prompt' and 'block' key-value pairs
    request_block_index = int(request_data["block_index"])

    extracted_data = extract_data(request_data["prompt"], request_block_index)  # extract_data() calls the SCHEMA OpenAI tool to extract data from user's prompt
    update_data(extracted_data, request_block_index)  # with the extracted data, updates the database

    block_index = request_block_index
    if is_block_complete(block_index):  # if the current block needs more info, keep 'block' the same
        if request_block_index == len(data) - 1:
            print_result()
            return jsonify({"response": "Application completed successfully"}), 200
        else:
            block_index = request_block_index + 1

    response = get_english_message(block_index, extracted_data["problems"])
    return jsonify({
        "response": response,
        "block_index": block_index,
    }), 200


if __name__ == "__main__":
    app.run(debug=True)

    #     block_index = data["block_index"]
    # else:
    #     if is_block_last(block_index):  # otherwise, it is guaranteed that the current block is finished, so we need to go to the next one
    #         return jsonify({  # if this was the last block, return success
    #             "response": "Application completed successfully"
    #         }), 200
    #     else:  # otherwise, add the next block to the response
    #         block_index = data["block_index"] + 1

    # response = get_english_message(block_index)
    # return jsonify({
    #     "response": response
    # }), 200
