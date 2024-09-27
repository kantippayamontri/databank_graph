from pydantic import BaseModel, Field

class Device(BaseModel):
    name: str = Field(alias="device_name")
    type: str = Field(alias="device_type")
    unprocessed_data: list[str] = Field(alias="device_unprocessed")
    raw_data: dict[str, dict[str, str]] | None = Field(alias="raw_data")

class Service(BaseModel):
    ...
    
class Data(BaseModel):
    id:str
    label: str

class Position(BaseModel):
    x:int 
    y:int

class RelationData(BaseModel):
    source: str
    target: str

class Node(BaseModel):
    data: Data | None 
    position: Position | None

class Relation(BaseModel):
    data: RelationData | None