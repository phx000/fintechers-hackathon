## Hackathon project
We built a chat-based form filler using GPT-4o. We leveraged its ability to return data in a fixed schema.

### Example
The bank needs to know your `first_name`, `last_name`, `address`, `city`, `state`  and `NAICS_code`.
- The chat asks you for your full name. It will use reasoning to parse it into `first_name` and `last_name`. If it is not able, it will ask for clarification.
- _(The AI saves all the data it gets in real time)_
- It asks you for your address. You may enter it in any format you like, and it will infer data. For example, by saying Los Angeles, it will populate the `state` field with `California`.
- If you don't know what a NAICS code is, just ask the AI. It will likely ask you for questions on your specific situation (e.g. marital status, number of employees, etc.) and then it will suggest a NAICS code that fits your case.

### Motivation
Friction in forms is a huge problem in the banking industry. The harder it is for a customer to apply for a loan at your bank, the more likely it is they will leave the website and never come back. Make it as easy as possible by offering a smart, chat-based approach to it.