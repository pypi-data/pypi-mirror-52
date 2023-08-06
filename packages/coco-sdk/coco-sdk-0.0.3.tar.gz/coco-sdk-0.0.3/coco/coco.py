import uuid
import json

import requests
from pygments import highlight, lexers, formatters

class CoCoResponse:
    def __init__(
            self,
            response: str="",
            component_done: bool=False,
            component_failed: bool=False,
            updated_context: dict={},
            confidence: float=1.,
            idontknow: bool=False,
            raw_resp: dict={},
            **kwargs
    ):
        self.response: str = response
        self.component_done: bool = component_done
        self.component_failed: bool = component_failed
        self.updated_context: dict = updated_context
        self.confidence: float = confidence
        self.idontknow: bool = idontknow
        self.raw_resp: dict = raw_resp

        for k, karg in kwargs.items():
            setattr(self, k, karg)

    def __repr__(self):
        instance_dict = {k: v for k, v in self.__dict__.items() if k != "raw_resp"}
        formatted_json = json.dumps(instance_dict, indent=True)
        colorful_json = highlight(
            formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        return colorful_json

def exchange(component_id: str, session_id: str,
                  user_input: str = None, **kwargs) -> CoCoResponse:
    """
    calls coco and try to maintain similar api.
    available optional kwargs are:
        user_input
        context

    full api spec available at app.coco.imperson.com

    Arguments:
        component_id {str} -- the component id from coco app
        session_id {str} -- a randomly generated session id to identify the session

    Returns:
        CoCoResponse instance
    """
    payload = kwargs
    if user_input:
        payload = {**{"user_input": user_input}, **kwargs}
    coco_resp = requests.post(
        "https://app.coco.imperson.com/api/exchange/"
        f"{component_id}/{session_id}",
        json=payload,
    ).json()
    return CoCoResponse(**coco_resp, raw_resp=coco_resp)

def generate_session_id():
    return str(uuid.uuid4())

class ConversationalComponent:
    """
    A wrapper for the coco exchange call to keep a component instance as a variable
    """
    def __init__(self, component_id: str):
        self.component_id = component_id

    def __call__(self, session_id: str, user_input: str = None, **kwargs) \
            -> CoCoResponse:
        return exchange(self.component_id, session_id, user_input, **kwargs)

class ComponentSession:
    """
    A wrapper for a session. generates and keep the session_id for you
    """
    def __init__(self, component_id: str, session_id: str = None):
        self.component = ConversationalComponent(component_id)
        if not session_id:
            self.session_id = generate_session_id()
        else:
            self.session_id = session_id

    def __call__(self, user_input: str = None, **kwargs) -> CoCoResponse:
        return self.component(self.session_id, user_input, **kwargs)

