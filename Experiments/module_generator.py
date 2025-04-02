import pandas as pd
import openai
import json
import os
from dotenv import load_dotenv
from utils import MetadataLoader, export_full_metadata
import re

load_dotenv()

# Securely load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Updated context reflecting your new business logic
GITBOOK_CONTEXT = """
TableFlow is a no-code platform for building ERP systems.

Business Concept:
- The system has two "Type" values: "Module" and "Dashboard".
- "Modules" are top-level navigation elements (e.g., Sales, Inventory).
- "Dashboard" is used where traditionally a "Menu" would exist.
- A "Dashboard" is always a child under a "Module".
- Dashboards can link to CRUD tables, reports, workflows, or visual dashboards.

Important:
- Do NOT use "Menu" as a type. Replace it with "Dashboard" as per our standard.
- Each metadata record must include: Module, Parent Module, Type (Module/Dashboard), Color, Icon.
- Leave Color and Icon blank ("").
- Ensure that Dashboards always have a parent Module.
- Apply proper logical grouping based on the provided dataset.
"""

class ModuleGeneratorAI:
    def __init__(self, summary):
        self.summary = summary

    def generate_prompt(self):
        prompt = f"""
        You are an enterprise metadata architect for TableFlow ERP.

        {GITBOOK_CONTEXT}

        Here is the dataset summary you are working with:
        {json.dumps(self.summary, indent=2)}

        📌 Key Guidelines:
        1. Create a clean two-level hierarchy:
        - **Modules** should represent broad functional areas or management domains (e.g., "Sales", "Inventory", "Client Management").
        - **Dashboards** should represent business entities or screens within a module (e.g., "Clients", "Leads", "Orders", "Employees").

        2. Avoid assigning data tables directly as Modules unless they truly represent a full domain.
        - For example, prefer:
            - "Client Management" → Module
            - "Clients" → Dashboard
        - NOT:
            - "Clients" → Module
            - "Client Management" → Dashboard

        3. Apply grouping logic:
        - Similar tables (e.g., "Leads", "Deals") should fall under a single logical module ("Sales").
        - Use business intuition to create clean top-level Modules and logical Dashboard assignments.

        4. Don't repeat names:
        - Avoid cases where Module and Dashboard names are identical.
        - Always aim to group dashboards under a distinct parent Module.

        Output must be in this JSON format:
        [
            {{"Module": "ModuleName", "Parent Module": "", "Type": "Module", "Color": "", "Icon": ""}},
            {{"Module": "DashboardName", "Parent Module": "ModuleName", "Type": "Dashboard", "Color": "", "Icon": ""}}
        ]

        Think carefully before assigning "Module" or "Dashboard" types.
        """
        return prompt

    def call_openai(self):
        prompt = self.generate_prompt()
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a metadata expert for TableFlow ERP platform."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content

    def parse_ai_response(self, ai_response):
        # Extract JSON block if present
        if "```json" in ai_response:
            ai_response = ai_response.split("```json")[1].split("```")[0].strip()
        # Parse as Python list and convert to DataFrame
        parsed_data = json.loads(ai_response)
        return pd.DataFrame(parsed_data)

    def generate_modules(self):
        """Generate and return modules metadata as a DataFrame without writing to disk."""
        ai_output = self.call_openai()
        modules_df = self.parse_ai_response(ai_output)
        return modules_df
def extract_json(text):
    """
    Try to extract a JSON object from a string.
    First, attempt to parse the entire text.
    If that fails, use regex to locate a JSON substring.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Attempt to extract the JSON substring
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
    return None
def is_relevant_for_erp_llm(summary):
    """
    Use the LLM to determine if the dataset summary is relevant for generating ERP modules.
    The LLM is prompted to analyze the dataset summary and respond with a JSON object in the format:
    {"relevant": true} if the dataset is business-related, or {"relevant": false} if not.
    """
    prompt = f"""
    You are an expert in enterprise resource planning (ERP) systems.
    Given the following dataset summary, please determine if it is relevant for generating ERP modules.
    Relevance means that the dataset contains business-related data such as client information, sales records,
    inventory management, employee records, etc.
    Respond with a JSON object exactly in the following format:
    {{"relevant": true}} if relevant, or {{"relevant": false}} if not.
    
    Dataset summary:
    {json.dumps(summary, indent=2)}
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Change to your appropriate model if needed
        messages=[
            {"role": "system", "content": "You are an ERP systems expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    answer = response.choices[0].message.content
    result = extract_json(answer)
    if result is None:
        print("Error parsing relevance result: No valid JSON found in response.")
        return False
    return result.get("relevant", False)

def main_pipeline(input_file, output_file=None):
    """
    Loads and summarizes the input file,
    generates the Modules metadata in memory,
    and optionally exports the complete metadata to an Excel file.
    Returns the generated modules DataFrame.
    """
    # Load + summarize data
    loader = MetadataLoader(input_file)
    if loader.load_excel() is not True:
        print(loader.load_excel())
        return None

    summary = loader.summarize()
    print("✅ Data Summary:", summary)
    print("✅ Data Summary Ready!")

    # Check dataset relevance using the LLM-based approach
    if not is_relevant_for_erp_llm(summary):
        print("⚠️ The dataset does not appear to be relevant for ERP module generation. Skipping metadata generation.")
        # Optionally, you can keep existing metadata unchanged or assign an empty DataFrame
        loader.data['Modules'] = pd.DataFrame([])
        export_full_metadata(loader.data, output_file)
        print("✅ Exported metadata with no generated modules.")
        return

    # Generate metadata using OpenAI
    generator = ModuleGeneratorAI(summary)
    modules_df = generator.generate_modules()
    print("🤖 Generated Modules DataFrame:")
    print(modules_df)

    # Merge step: update the 'Modules' sheet in the metadata dictionary
    loader.data['Modules'] = modules_df

    # If an output file is provided, export the complete metadata Excel
    if output_file:
        export_full_metadata(loader.data, output_file)
        print("✅ Modules Metadata Excel ready!")

    # Return the modules DataFrame for in-memory chaining
    return modules_df

if __name__ == "__main__":
    input_path = "CRM_Food_Inventory_Sample.xlsx"
    output_path = r"D:\Experiments\New Excel Approach\metadata_generator\outputs\module.xlsx"
    modules_df = main_pipeline(input_path, output_path)
    print("✅ Done!")
