j = {
  "business_information": {
    "business_name": { "type": "string" },
    "legal_entity_type": { "type": "enum", "options": ["LLC", "Corporation", "Partnership", "Sole Proprietor", "Non-Profit"] },
    "date_of_incorporation": { "type": "date" },
    "state_of_incorporation": { "type": "string" },
    "industry": { "type": "string" },
    "naics_code": { "type": "string", "description": "North American Industry Classification System code" }
  },
  "beneficial_owners": {
    "type": "array",
    "items": {
      "full_name": { "type": "string" },
      "ownership_percentage": { "type": "number" },
      "dob": { "type": "date" },
      "ssn_last4": { "type": "string" },
      "address": {
        "street": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" },
        "zip": { "type": "string" }
      }
    }
  },
  "banking_preferences": {
    "account_type": { "type": "enum", "options": ["Checking", "Savings", "Brokerage"] },
    "initial_deposit_amount": { "type": "number" },
    "funding_source": { "type": "enum", "options": ["Wire Transfer", "ACH", "Check", "Cash"] },
    "linked_bank_account": {
      "bank_name": { "type": "string" },
      "routing_number": { "type": "string" },
      "account_number": { "type": "string" }
    }
  },
  "compliance_questions": {
    "politically_exposed_person": { "type": "boolean" },
    "source_of_funds": { "type": "string" },
    "expected_monthly_volume": { "type": "number" },
    "international_transactions": { "type": "boolean" },
    "countries_of_operation": { "type": "array", "items": { "type": "string" } }
  }
}