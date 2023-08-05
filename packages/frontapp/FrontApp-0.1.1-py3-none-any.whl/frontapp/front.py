from __future__ import annotations

from typing import Dict, List, Optional

import attr
import requests

import datetime as dt

from decorator import decorator
from envparse import env

from frontapp import err


@decorator
def handle_response(func, *args, **kwargs) -> Dict:
    response = func(*args, **kwargs)

    if isinstance(response, List):
        res = {}
        items = []
        for r in response:
            if r.json().get("items"):
                items.extend(r.json().pop("items"))

            res.update(r.json())
        if items:
            res["items"] = items
        return res

    if 200 <= response.status_code <= 299:
        if not response.json():
            return {"status": response.status_code}
        return response.json()

    error_dict = {404: err.NotFound}

    if response.status_code in error_dict:
        raise error_dict[response.status_code](
            f'Status code: {response.status_code}. Message: {response.json()["message"]}'
        )

    raise err.FrontError(
        f'Status code: {response.status_code}. Message: {response.json()["message"]}'
    )


@attr.s(auto_attribs=True)
class Front:
    token: str = attr.ib(repr=False)
    url: str = attr.ib(default="https://api2.frontapp.com", repr=False)

    @classmethod
    def from_environment(cls):
        return cls(token=env("FRONT_TOKEN"))

    @property
    def authorization(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @handle_response
    def get(self, endpoint: str, data: Dict = None, limit=None, offset=None) -> Dict:
        """
        Make a GET request to API endpoint.

        :param endpoint: API endpoint to request

        :param data: dictionary of optional query params

        :param limit: Maximum number of results to return in this query.

        :param offset: An opaque token used to fetch the next page of results.

        :return:
        """
        if not data:
            data = {}
        if limit:
            data["limit"] = limit

        if offset:
            data["pageToken"] = offset
        r = requests.get(self.url + endpoint, params=data, headers=self.authorization)
        if limit or not r.json().get("nextPageLink"):
            return r

        res = [r]
        while r.json().get("nextPageLink"):
            next_page = r.json()["nextPageLink"]
            r = requests.get(next_page, headers=self.authorization)
            res.append(r)
        return res

    # noinspection PyTypeChecker
    @handle_response
    def post(self, endpoint: str, data: Dict) -> Dict:
        """
        Make a POST request to the API endpoint.

        :param endpoint: API endpoint to request

        :param data: data dict to be sent as body json

        :return:
        """
        return requests.post(
            self.url + endpoint,
            json=data,
            headers={**self.authorization, "Content-Type": "application/json"},
        )

    # noinspection PyTypeChecker
    @handle_response
    def put(self, endpoint: str, data: Dict) -> Dict:
        """
        Make a PUT request to the API endpoint.

        :param endpoint: API endpoint to request

        :param data: data dict to be sent as body json

        :return:
        """
        return requests.put(self.url + endpoint, json=data, headers=self.authorization)

    # noinspection PyTypeChecker
    @handle_response
    def delete(self, endpoint: str) -> Dict:
        """
        Make a DELETE request to the API endpoint.

        :param endpoint: API endpoint to request

        :return:
        """
        return requests.delete(self.url + endpoint, headers=self.authorization)

    def send_message(self, inbox_id: str, sender: Sender, message: Message):
        endpoint = f"/channels/{inbox_id}/incoming_messages"
        data = {"sender": sender.to_dict(), **message.__dict__}
        return self.post(endpoint, data=data)


@attr.s(auto_attribs=True)
class Sender:
    handle: str
    name: str

    def to_dict(self):
        return self.__dict__


@attr.s(auto_attribs=True)
class Message:
    body: str
    subject: Optional[str] = attr.ib(default=None)
    metadata: Optional[Dict] = attr.ib(default={})
    attachments: Optional[List] = attr.ib(default=[])


if __name__ == "__main__":
    front = Front.from_environment()
    sender = Sender("some_handle", "Some Name")
    message = Message(
        subject="This is a subject!",
        body=f'This is body: {dt.datetime.now().strftime("%H:%M:%S")}',
    )
    front.send_message("cha_1xxfs", sender, message)
