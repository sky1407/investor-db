from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator

InvestorType = Literal[
    "vc", "pe", "cvc", "family_office", "angel", "private_investor", "public_fund", "fund_of_funds"
]
EntityKind = Literal[
    "investor", "service_provider", "lender", "platform", "grant_scheme", "public_markets_manager"
]
Stage = Literal["pre-seed", "seed", "series-a", "series-b-plus", "growth", "buyout"]
Currency = Literal["EUR", "USD", "CZK", "GBP", "HUF", "PLN", "CHF"]
ExclusionReason = Literal[
    "not_investor_service",
    "debt_only",
    "platform_only",
    "grant_only",
    "public_markets_only",
    "inactive",
    "no_evidence",
    "duplicate",
]
CheckStatus = Literal["verified", "quote_not_found", "http_error", "fetch_error", "unsupported_content"]

INVESTOR_TYPES: tuple[str, ...] = InvestorType.__args__
EXCLUSION_REASONS: tuple[str, ...] = ExclusionReason.__args__


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Evidence(Strict):
    source_url: HttpUrl
    source_date: date | None = None
    quote: str = Field(min_length=8, max_length=600)

    @field_validator("quote")
    @classmethod
    def quote_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("quote must not be blank")
        return value.strip()


class KindFact(Evidence):
    value: EntityKind


class TypeFact(Evidence):
    value: InvestorType


class SectorsFact(Evidence):
    value: list[str] = Field(min_length=1)


class StagesFact(Evidence):
    value: list[Stage] = Field(min_length=1)


class MoneyFact(Evidence):
    amount: float = Field(gt=0)
    currency: Currency


class Investment(Evidence):
    company: str = Field(min_length=1)
    deal_date: date


class ResearchRecord(Strict):
    candidate_id: str = Field(pattern=r"^c\d{3}$")
    name: str = Field(min_length=1)
    legal_name: str | None = None
    reg_no: str | None = None
    country: str = Field(pattern=r"^[A-Z]{2}$")
    active_in: list[str] = Field(default_factory=list)
    website: HttpUrl | None = None
    entity_kind: KindFact
    investor_type: TypeFact | None = None
    sectors: SectorsFact | None = None
    stages: StagesFact | None = None
    ticket_min: MoneyFact | None = None
    ticket_max: MoneyFact | None = None
    aum: MoneyFact | None = None
    funds: list[str] = Field(default_factory=list)
    investments: list[Investment] = Field(default_factory=list)
    duplicate_of: str | None = Field(default=None, pattern=r"^c\d{3}$")
    notes: str = ""
    researched_at: date

    @field_validator("active_in")
    @classmethod
    def country_codes(cls, value: list[str]) -> list[str]:
        for code in value:
            if len(code) != 2 or not code.isupper():
                raise ValueError(f"invalid country code: {code}")
        return value

    @model_validator(mode="after")
    def investor_needs_type(self) -> "ResearchRecord":
        if self.entity_kind.value == "investor" and self.investor_type is None:
            raise ValueError("entity_kind=investor requires investor_type")
        if self.duplicate_of == self.candidate_id:
            raise ValueError("record cannot be a duplicate of itself")
        return self

    def evidence_items(self) -> list[tuple[str, Evidence]]:
        items: list[tuple[str, Evidence]] = [("entity_kind", self.entity_kind)]
        for field in ("investor_type", "sectors", "stages", "ticket_min", "ticket_max", "aum"):
            fact = getattr(self, field)
            if fact is not None:
                items.append((field, fact))
        items.extend((f"investments[{i}]", inv) for i, inv in enumerate(self.investments))
        return items


class CheckResult(Strict):
    url: str
    status: CheckStatus
    http_status: int | None = None
    detail: str = ""
