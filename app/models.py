from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, DateTime, Text, UniqueConstraint
from datetime import datetime

class Base(DeclarativeBase): pass

class Search(Base):
    __tablename__ = "searches"
    id: Mapped[int] = mapped_column(primary_key=True)
    segmento: Mapped[str] = mapped_column(String(100))
    produto: Mapped[str] = mapped_column(String(150))
    uf: Mapped[str] = mapped_column(String(2), default="BR")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(20), default="queued")
    leads = relationship("Lead", back_populates="search")

class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True)
    cnpj: Mapped[str] = mapped_column(String(20))
    razao_social: Mapped[str] = mapped_column(String(255))
    nome_fantasia: Mapped[str] = mapped_column(String(255), default="")
    cnae_principal: Mapped[str] = mapped_column(String(20), default="")
    porte: Mapped[str] = mapped_column(String(30), default="")
    uf: Mapped[str] = mapped_column(String(2), default="")
    municipio: Mapped[str] = mapped_column(String(80), default="")
    site_url: Mapped[str] = mapped_column(String(255), default="")
    fonte: Mapped[str] = mapped_column(String(40), default="mock")
    contacts = relationship("Contact", back_populates="company")

class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(primary_key=True)
    search_id: Mapped[int] = mapped_column(ForeignKey("searches.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    score: Mapped[float] = mapped_column(Float, default=0)
    prob_30d: Mapped[float] = mapped_column(Float, default=0)
    prob_90d: Mapped[float] = mapped_column(Float, default=0)
    janela_favoravel: Mapped[str] = mapped_column(String(20), default="")
    notas: Mapped[str] = mapped_column(Text, default="")
    enrichment_status: Mapped[str] = mapped_column(String(20), default="pending")
    search = relationship("Search", back_populates="leads")
    company = relationship("Company")
    __table_args__ = (UniqueConstraint('search_id','company_id', name='uq_search_company'),)

class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    tipo: Mapped[str] = mapped_column(String(20))
    valor: Mapped[str] = mapped_column(String(255))
    origem: Mapped[str] = mapped_column(String(50), default="site")
    verificado: Mapped[bool] = mapped_column(Boolean, default=False)
    company = relationship("Company", back_populates="contacts")

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), default="queued")
    search_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    error: Mapped[str] = mapped_column(Text, default="")

class OptOut(Base):
    __tablename__ = "optouts"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    reason: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)
