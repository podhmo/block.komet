# -*- coding:utf-8 -*-
import sqlalchemy.types as t
from .. import interfaces as i

## tentative
default_classfier = {
    (t.INTEGER,t.INTEGER): [i.IInteger, i.IInteger],
    (t.Integer,t.Integer): [i.IInteger, i.IInteger],
    (t.INTEGER,): i.IInteger,
    (t.INT,): i.IInteger, 
    (t.CHAR,): i.IString, 
    (t.VARCHAR,): i.IString, 
    (t.NVARCHAR,): i.IString, 
    (t.TEXT,): i.IString, 
    (t.BLOB,): i.IUnknown, 
    (t.CLOB,): i.IUnknown, 
    (t.BINARY,): i.IUnknown, 
    (t.VARBINARY,): i.IUnknown, 
    (t.BOOLEAN,): i.IBoolean, 
    (t.BIGINT,): i.IInteger, 
    (t.SMALLINT,): i.IInteger, 
    (t.INTEGER,): i.IInteger, 
    (t.DATE,): i.IDate, 
    (t.FLOAT,): i.IFloat,
    (t.NUMERIC,): i.IInteger, #xxx:
    (t.REAL,): i.IFloat, 
    (t.DECIMAL,): i.IInteger, 
    (t.TIMESTAMP,): i.IUnknown, 
    (t.DATETIME,): i.IDateTime, 
    (t.DATE,): i.IDate, 
    (t.TIME,): i.ITime,
    (t.String,): i.IString, 
    (t.Text,): i.IString, 
    (t.Integer,): i.IInteger, 
    (t.SmallInteger,): i.IInteger, 
    (t.BigInteger,): i.IInteger, 
    (t.Numeric,): i.IInteger, 
    (t.Float,): i.IFloat, 
    (t.DateTime,): i.IDateTime, 
    (t.Date,): i.IDate, 
    (t.Time,): i.ITime,
    (t.LargeBinary,):i.IUnknown, 
    (t.Binary,):i.IUnknown, 
    (t.Boolean,):i.IBoolean, 
    (t.Unicode,):i.IString, 
    (t.Concatenable,):i.IUnknown, 
    (t.UnicodeText,):i.IString, 
    (t.Interval,):i.IUnknown, 
    (t.Enum,):i.IUnknown, 
}