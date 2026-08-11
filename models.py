from pydantic import BaseModel, Field


class JobOffer(BaseModel):
    id: str = Field(description="Unique identifier of the job offer.")
    title: str = Field(description="Job title.")
    description: str = Field(description="Full job description.")
    publication_date: str = Field(description="Publication date of the job offer.")

    company: str | None = Field(
        default=None,
        description="Name of the company.",
    )
    location: str | None = Field(
        default=None,
        description="Job location.",
    )
    salary: str | None = Field(
        default=None,
        description="Salary or salary range, when available.",
    )
    experience: str | None = Field(
        default=None,
        description="Required experience level or duration.",
    )
    skills: list[str] = Field(
        default_factory=list,
        description="Skills associated with the job offer.",
    )
    apply_url: str | None = Field(
        default=None,
        description="URL used to apply for the job.",
    )

class OfferSummary(BaseModel):
    id: str = Field(description="Unique identifier of the job offer.")
    title: str = Field(description="Job title.")


class OffersSummaryOutput(BaseModel):
    offers: list[OfferSummary] = Field(
        description="List of available job offers."
    )

class SearchOffersInput(BaseModel):
    key_word: str = Field(description="lowercase key word for finding relevent offers")

class ReadOfferInput(BaseModel):
    id: str = Field(
        description="Unique identifier of the job offer to retrieve."
    )