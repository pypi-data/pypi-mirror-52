"""Environment for :class:`.VKManager`."""

import json
import aiohttp
from kutana.environment import Environment


class VKEnvironment(Environment):

    """Environment for :class:`.VKManager`"""

    async def _upload_file_to_vk(self, upload_url, data):
        upload_result_text = None

        async with self.manager.session.post(upload_url, data=data) as resp:
            if resp.status == 200:
                upload_result_text = await resp.text()

        try:
            upload_result = json.loads(upload_result_text)

            if "error" in upload_result:
                raise RuntimeError

        except RuntimeError:
            upload_result = None

        return upload_result

    async def reply(self, message, attachment=None, **kwargs):
        """
        Reply to currently processed message.

        :param message: message to reply with
        :param attachment: optional attachment or list of attachments to
            reply with
        :param kwargs: arguments for vkontakte's "messages.send"
        :returns: list with results of sending messages
        """

        return await self.manager.send_message(
            message, self.peer_id, attachment, **kwargs
        )

    async def upload_doc(self, file, filename, **kwargs):
        """
        Upload file to be sent with :func:`.send_message`
        (or :func:`.reply`) as document. If you passed "peer_id", vkontakte's
        method "docs.getWallUploadServer" will be used.

        You can specify document's type with keyword argument "type" or
        "doctype". If you passed "graffiti" as type - method
        "docs.getWallUploadServer" will be used. Default type is "doc".

        :param file: document as file or bytes
        :param filename: name of provided file
        :param kwargs: arguments for vkontakte's methods
        :returns: :class:`.Attachment` or None
        """

        if kwargs.get("peer_id") is None:
            peer_id = self.peer_id

        else:
            peer_id = kwargs["peer_id"]

        doctype = kwargs.get("type", "") or kwargs.get("doctype", "doc")

        if peer_id and doctype != "graffiti":
            upload_data = await self.manager.request(
                "docs.getMessagesUploadServer",
                peer_id=peer_id,
                type=doctype,
            )

        else:
            upload_data = await self.manager.request(
                "docs.getWallUploadServer",
                group_id=kwargs.get("group_id") or self.manager.group_id,
                type=doctype,
            )

        if upload_data.error:
            return None

        upload_url = upload_data.response["upload_url"]

        data = aiohttp.FormData()
        data.add_field("file", file, filename=filename)

        upload_result = await self._upload_file_to_vk(upload_url, data)

        if not upload_result:
            return None

        attachments = await self.manager.request(
            "docs.save", **upload_result
        )

        if attachments.error:
            return None

        return self.manager.create_attachment(
            attachments.response, "doc"
        )

    async def upload_photo(self, file, **kwargs):
        """
        Upload file to be sent with :func:`.send_message`
        (or :func:`.reply`) as photo. If "peer_id" was passed, file will be
        uploaded for user with "peer_id".

        :param file: photo as file or bytes
        :param kwargs: arguments for vkontakte's methods
        :returns: :class:`.Attachment` or None
        """

        if kwargs.get("peer_id") is None:
            peer_id = self.peer_id

        else:
            peer_id = kwargs.get("peer_id")

        upload_data = await self.manager.request(
            "photos.getMessagesUploadServer", peer_id=peer_id
        )

        if upload_data.error:
            return None

        upload_url = upload_data.response["upload_url"]

        data = aiohttp.FormData()
        data.add_field("photo", file, filename="image.png")

        upload_result = await self._upload_file_to_vk(upload_url, data)

        if not upload_result:
            return None

        attachments = await self.manager.request(
            "photos.saveMessagesPhoto", **upload_result
        )

        if attachments.error:
            return None

        return self.manager.create_attachment(
            attachments.response[0], "photo"
        )

    async def get_file_from_attachment(self, attachment):
        if not attachment or not attachment.link:
            return None

        async with self.manager.session.get(attachment.link) as response:
            return await response.read()
