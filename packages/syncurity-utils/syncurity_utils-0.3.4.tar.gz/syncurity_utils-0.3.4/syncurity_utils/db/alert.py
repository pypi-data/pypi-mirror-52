
from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.dialects.postgresql import JSONB

from syncurity_utils.db.db import Base


class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, Sequence('alert_id_seq'), primary_key=True)
    payload = Column(JSONB)
    timestamp = Column(Integer)
    sensor_ref_name = Column(String)
    irflow_alert_id = Column(Integer)
    integration_id = Column(Integer)
    tenant_id = Column(Integer)
    alert_type_id = Column(Integer)

    def __init__(self, payload, timestamp, sensor_ref_name, irflow_alert_id, integration_id, tenant_id,
                 alert_type_id):
        self.payload = payload
        self.timestamp = timestamp
        self.sensor_ref_name = sensor_ref_name
        self.irflow_alert_id = irflow_alert_id
        self.integration_id = integration_id
        self.tenant_id = tenant_id
        self.alert_type_id = alert_type_id

    def __repr__(self):
        return "<Alert(Id=%s, payload='%s', " \
               "timestamp='%s', " \
               "irflow_alert_id='%s', " \
               "integration_id='%s', " \
               "tenant_id='%s', " \
               "sensor_ref_name='%s', " \
               "alert_type_id='%s')>" \
               % (self.id, self.payload, self.timestamp,
                  self.irflow_alert_id, self.integration_id, self.tenant_id, self.sensor_ref_name, self.alert_type_id)
