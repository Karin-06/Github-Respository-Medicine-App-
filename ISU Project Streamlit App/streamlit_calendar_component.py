import streamlit as st
from streamlit.components.v1 import ComponentBase
import pandas as pd
import datetime

_RELEASE = False

if not _RELEASE:
    _component_func = st._components._component_func
else:
    _component_func = st._component_func

class StreamlitCalendarComponent(ComponentBase):
    def __init__(self, key=None, calendar_options=None, calendar_events=None, **kwargs):
        super().__init__(key=key, **kwargs)
        self.calendar_options = calendar_options
        self.calendar_events = calendar_events

_streamlit_calendar_component = _component_func(
    StreamlitCalendarComponent, 
    key="streamlit_calendar_component",
    calendar_options={},
    calendar_events=[],
)

def streamlit_calendar(calendar_options, calendar_events):
    return _streamlit_calendar_component(calendar_options=calendar_options, calendar_events=calendar_events)
