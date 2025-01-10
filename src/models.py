from typing import List, Optional

from pydantic import BaseModel

class Binance(BaseModel):
    """Binance Payload request"""
    method: str
    params: List[str]
    id: int
    
class Sockets(BaseModel):
    """Contains all the parameters passed by the user"""
    
    host: str
    port: int
    request: Binance
    handshake: str
    topic: str
    client: str
    clientHost: str
    clientPort: int