from typing import List, Optional
from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    to_email: List[EmailStr]
    cc_email: Optional[List[EmailStr]] = None
    bcc_email: Optional[List[EmailStr]] = None
    subject: str
    message: str
