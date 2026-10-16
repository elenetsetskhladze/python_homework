from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client()
MODEL = "gemini-3.1-flash-lite"

class JobPosting(BaseModel):
    title: str
    required_experience_years: int | None
    required_skills: list[str]
    nice_to_have_skills: list[str]
    work_type: str | None
    salary_min: float | None
    salary_max: float | None
    salary_currency: str | None
    english_level: str | None
    skills_match: list[str]
    missing_skills: list[str]


candidate_skills = ["Python", "FastAPI", "PostgreSQL", "Docker", "Git"]


jobs = [
    """
    We are looking for a Python Backend Developer.
    At least 2 years of experience with Python and Django is required.
    PostgreSQL and Docker are required.
    The position is remote with a salary of $1500-$2500 per month.
    English B2 or higher is required.
    """,

    """
    We are hiring a Junior FastAPI Developer.
    Python, FastAPI, PostgreSQL and Git are required.
    Docker is a plus.
    This is a hybrid position.
    """,

    """
    We are looking for a Data Analyst.
    SQL and Excel are required.
    Power BI is a plus.
    We offer a competitive salary.
    """
]


SYSTEM_PROMPT = """
You are a job posting analyzer.

Read the job description and extract the important information.

Find the job title, required experience, skills, work type,
salary and English level.

Separate required skills from skills that are only preferred.

Compare the job requirements with the candidate's skills:
- skills_match: skills the candidate already has.
- missing_skills: required skills the candidate does not have.

If some information is not mentioned, use null for that field.
If there are no skills for a list, return an empty list.

Do not guess information that is not provided in the job description.
Do not include preferred skills in missing_skills.
"""





for index, job in enumerate(jobs, start=1):

    response = client.models.generate_content(
        model=MODEL,
        contents=f"""
        JOB DESCRIPTION:
        {job}

        CANDIDATE SKILLS:
        {", ".join(candidate_skills)}
        """,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=JobPosting,
            temperature=0.0,
        ),
    )

    result = response.parsed

    print(f"\n{'=' * 15} JOB {index} {'=' * 15}")
    print(result.model_dump_json(indent=2))