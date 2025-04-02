import pandas as pd
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Securely load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class PromptDrivenCRMGenerator:
    def __init__(self):
        self.system_context = """
        You are an expert business data architect creating precise, industry-standard data models.

        Key Guidelines:
        - Generate sheets capturing core business workflows
        - Use standard PascalCase naming
        - Focus on practical, minimal schema design
        - Ensure logical entity relationships
        - Maximize operational utility
        """

    def generate_prompt(self, user_description):
        return f"""
    You are an expert business data modeler creating structured, minimal data schemas.

    🔹 Business Scenario:
    {user_description}

    🎯 Objective:
    Design a CRM schema that models real-world operations accurately with clear entities and practical columns.

    📌 Guidelines:
    - Identify 3–5 core entities relevant to the business
    - Include only essential columns for each entity
    - Order columns logically, always starting with unique identifiers (e.g., CustomerId, OrderId)
    - Use PascalCase for all names (e.g., OrderDate, IsActive)
    - Leverage the following **reference data types** to inspire realistic column names (but DO NOT include data types in the output):
    Boolean, Currency, Date, DateTime, Decimal, Document, Image, Integer, List, Percentage, Text, Multi Select, Digital Signature, Rating, Radio Button, Assign to, Time
    - Avoid redundancy or over-complication
    - Focus on business utility and schema clarity

    🧾 Output Format (STRICT JSON ONLY):

    {{
    "sheets": [
        {{
        "name": "EntityName",
        "columns": ["ColumnName1", "ColumnName2"]
        }}
    ]
    }}
    """

    def call_openai(self, prompt):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_context},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return None

    def parse_response(self, ai_response):
        if ai_response is None:
            return {"sheets": []}

        try:
            # Multiple JSON extraction strategies
            if "```json" in ai_response:
                ai_response = ai_response.split("```json")[1].split("```")[0].strip()
            
            parsed_data = json.loads(ai_response)
            return parsed_data
        except json.JSONDecodeError:
            print("Error parsing AI response.")
            return {"sheets": []}

    def generate_excel_sheets(self, parsed_data):
        output_dfs = {}
        
        for sheet in parsed_data.get('sheets', []):
            sheet_name = sheet['name']
            columns = sheet.get('columns', [])
            
            # Create DataFrame with columns as column headers
            df = pd.DataFrame(columns=columns)
            output_dfs[sheet_name] = df
        
        return output_dfs

    def save_to_excel(self, dataframes, output_path):
        try:
            with pd.ExcelWriter(output_path) as writer:
                for sheet_name, df in dataframes.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"✅ CRM Model Generated: {output_path}")
        except Exception as e:
            print(f"Excel Generation Error: {e}")

def generate_crm_from_prompt(user_description, output_path='generated_crm_model.xlsx'):
    crm_generator = PromptDrivenCRMGenerator()
    
    detailed_prompt = crm_generator.generate_prompt(user_description)
    ai_response = crm_generator.call_openai(detailed_prompt)
    parsed_data = crm_generator.parse_response(ai_response)
    
    output_dataframes = crm_generator.generate_excel_sheets(parsed_data)
    crm_generator.save_to_excel(output_dataframes, output_path)
    
    return parsed_data

# Example Usage
if __name__ == "__main__":
    sample_description = "CRM for a digital marketing agency tracking leads, clients, and campaigns."
    output_path = "generated_crm_model.xlsx"
    
    result = generate_crm_from_prompt(sample_description, output_path)
    # print(json.dumps(result, indent=2))