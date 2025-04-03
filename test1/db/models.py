from typing import Annotated

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, text
from sqlalchemy.orm import relationship, DeclarativeBase, Session, Mapped, mapped_column

from .db import engine, SessionLocal, with_db_session

BaseDate = Annotated[Date, mapped_column(nullable=True)]
BaseStr = Annotated[String, mapped_column(nullable=True)]
BaseBool = Annotated[Boolean, mapped_column(nullable=True)]

class Base(DeclarativeBase):
    type_annotation_map = {
        BaseDate: Date,
        BaseStr: String(100),
        BaseBool: Boolean
    }

class GeneralInfo(Base):
    '''Table for general information about the company'''
    
    __tablename__ = 'general_info'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cui: Mapped[BaseStr] = mapped_column(String(20), nullable=False, unique=True)
    data: Mapped[BaseDate] = mapped_column(nullable=False)
    denumire: Mapped[BaseStr]
    adresa: Mapped[str]
    nrRegCom: Mapped[BaseStr]
    telefon: Mapped[BaseStr]
    fax: Mapped[BaseStr]
    codPostal: Mapped[BaseStr]
    act: Mapped[BaseStr]
    stare_inregistrare: Mapped[BaseStr]
    data_inregistrare: Mapped[BaseDate]
    cod_CAEN: Mapped[BaseStr]
    iban: Mapped[BaseStr]

class VATRegistration(Base):
    '''Table for storing information about VAT registration (НДС)'''
    
    __tablename__ = 'vat_registration'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    general_info_id: Mapped[int] = mapped_column(ForeignKey('general_info.id'), nullable=False)
    scpTVA: Mapped[BaseBool]
    data_inceput_ScpTVA: Mapped[BaseDate]
    data_sfarsit_ScpTVA: Mapped[BaseDate]
    data_anul_imp_ScpTVA: Mapped[BaseDate]
    mesaj_ScpTVA: Mapped[BaseStr]

    general_info = relationship("GeneralInfo", back_populates="vat_registration")
    GeneralInfo.vat_registration = relationship("VATRegistration", back_populates="general_info", uselist=False)

class CompanyStatus(Base):
    '''Table for status company'''
    
    __tablename__ = 'company_status'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    general_info_id: Mapped[int] = mapped_column(ForeignKey('general_info.id'), nullable=False)
    dataInactivare: Mapped[BaseDate]
    dataReactivare: Mapped[BaseDate]
    dataPublicare: Mapped[BaseDate]
    dataRadiere: Mapped[BaseDate]
    statusInactivi: Mapped[BaseBool]

    general_info = relationship("GeneralInfo", back_populates="company_status")
    GeneralInfo.company_status = relationship("CompanyStatus", back_populates="general_info", uselist=False)

@with_db_session(SessionLocal)
def save_data_to_db(api_response: dict, session: Session = None):
    result = None
    def upsert_record(model, filter_by:dict, data:dict):
        record = session.query(model).filter_by(**filter_by).first()
        if record:
            nonlocal result
            for key, value in data.items():
                setattr(record, key, value)
            result = {
                "message": "cui update in DB",
                "id": record.id
            }
        else:
            record = model(**data)
            session.add(record)
            session.flush()
            result = {
                "message": "cui add in DB",
                "id": record.id
                }
        return record
    
    def check_perioade_TVA(data, item):
        if data and len(data) > 0:
            return data[0].get(item)
        else:
            return None

    for record in api_response.get("found", []):
        record: dict
        general_info_data: dict = record.get("date_generale", {})
        vat_registration_data: dict = record.get("inregistrare_scop_Tva", {})
        company_status_data: dict = record.get("stare_inactiv", {})
        
        general_info = upsert_record(
            GeneralInfo,
            {"cui": general_info_data.get("cui")},
            {
                "cui": general_info_data.get("cui"),
                "data": general_info_data.get("data"),
                "denumire": general_info_data.get("denumire"),
                "adresa": general_info_data.get("adresa"),
                "nrRegCom": general_info_data.get("nrRegCom"),
                "telefon": general_info_data.get("telefon"),
                "fax": general_info_data.get("fax"),
                "codPostal": general_info_data.get("codPostal"),
                "act": general_info_data.get("act"),
                "stare_inregistrare": general_info_data.get("stare_inregistrare"),
                "data_inregistrare": general_info_data.get("data_inregistrare"),
                "cod_CAEN": general_info_data.get("cod_CAEN"),
                "iban": general_info_data.get("iban"),
            },
        )

        perioade_TVA = vat_registration_data.get("perioade_TVA")
        upsert_record(
            VATRegistration,
            {"general_info_id": general_info.id},
            {
                "general_info_id": general_info.id,
                "scpTVA": vat_registration_data.get("scpTVA"),
                "data_inceput_ScpTVA": check_perioade_TVA(perioade_TVA, "data_inceput_ScpTVA"),
                "data_sfarsit_ScpTVA": check_perioade_TVA(perioade_TVA, "data_sfarsit_ScpTVA"),
                "data_anul_imp_ScpTVA": check_perioade_TVA(perioade_TVA, "data_anul_imp_ScpTVA"),
                "mesaj_ScpTVA": check_perioade_TVA(perioade_TVA, "mesaj_ScpTVA"),
            },
        )

        upsert_record(
            CompanyStatus,
            {"general_info_id": general_info.id},
            {
                "general_info_id": general_info.id,
                "dataInactivare": company_status_data.get("dataInactivare"),
                "dataReactivare": company_status_data.get("dataReactivare"),
                "dataPublicare": company_status_data.get("dataPublicare"),
                "dataRadiere": company_status_data.get("dataRadiere"),
                "statusInactivi": company_status_data.get("statusInactivi"),
            },
        )
        
    return result

def setup_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("DB & table successfully created.")

if __name__ == "__main__":
    setup_database()