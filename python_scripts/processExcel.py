import os
import pandas as pd
from openai import OpenAI

"""
Process and review SoCI formulas using reusable prompt execution.

- Removes duplicated prompt-calling logic by introducing `run_prompt` and `process_rows`.
- Consolidates Excel output to one workbook with two sheets.
- Reads API key from OPENAI_API_KEY environment variable.
"""

# Initialize OpenAI client
client = OpenAI(api_key="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")

# Load initial data
file_path = "/Users/spencerdraftworx/Dropbox/Automated EXCEL DIFF/FRS102 Master/SoCIFormulasToUpdate.csv"
df = pd.read_csv(file_path)
print(f"- Shape: {df.shape[0]} rows, {df.shape[1]} columns")

def run_prompt(prompt_id: str, version: str, variables: dict) -> str:
    """Execute a stored prompt with variables and return plain text output."""
    response = client.responses.create(
        prompt={
            "id": prompt_id,
            "version": version,
            "variables": variables,
        }
    )
    return response.output_text


def process_rows(df: pd.DataFrame, variables_map: dict, output_column: str, prompt_id: str, version: str, progress_label: str) -> pd.DataFrame:
    """Run a prompt per-row using a mapping of prompt variables to DataFrame columns."""
    if output_column not in df.columns:
        df[output_column] = ''

    print(f"\nProcessing {progress_label}...")
    for index, row in df.iterrows():
        try:
            variables = { var_name: row[col_name] for var_name, col_name in variables_map.items() }
            result = run_prompt(prompt_id, version, variables)
            df.at[index, output_column] = result
            print(f"Processed row {index + 1}/{len(df)}")
        except Exception as e:
            print(f"Error processing row {index + 1}: {str(e)}")
            df.at[index, output_column] = f"ERROR: {str(e)}"

    print("Processing complete!")
    return df

# Run update flow (per-row prompt execution)
df = process_rows(
    df=df,
    variables_map={
        "original_formula": "Formula",
    },
    output_column="Updated_Formula",
    prompt_id="pmpt_68b6dbb7401c8190b01b4456b65df67a0a822fd0862f8358",
    version="3",
    progress_label="all formulas"
)

# Load review data
review_file_path = "/Users/spencerdraftworx/Dropbox/Automated EXCEL DIFF/FRS102 Master/Final Master VS NJ Latest/FormulasToReview.csv"
dfReview = pd.read_csv(review_file_path)
print(f"\nReview data - Shape: {dfReview.shape[0]} rows, {dfReview.shape[1]} columns")

# Run review evaluation flow
dfReview = process_rows(
    df=dfReview,
    variables_map={
        "original_formula": "Formula",
        "junior1_formula": "Updated_Formula (AI Review)",
        "junior2_formula": "NJ_Latest_Formula",
    },
    output_column="Review Notes",
    prompt_id="pmpt_68b6dbb7401c8190b01b4456b65df67a0a822fd0862f8358",
    version="6",
    progress_label="all reviews"
)

# Save both outputs to a single workbook with two sheets
output_path = "/Users/spencerdraftworx/Dropbox/Automated EXCEL DIFF/FRS102 Master/Final Master VS NJ Latest/Updated_SOCI_Formulas.xlsx"
with pd.ExcelWriter(output_path) as writer:
    df.to_excel(writer, index=False, sheet_name="UpdatedFormulas")
    dfReview.to_excel(writer, index=False, sheet_name="ReviewNotes")
print(f"Wrote results to '{output_path}' (sheets: UpdatedFormulas, ReviewNotes)")