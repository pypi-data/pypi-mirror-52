# pyre-strict

from unittest import TestCase

from lowerpines.message import (
    RefAttach,
    ComplexMessage,
    smart_split_complex_message,
    ImageAttach,
    LocationAttach,
    SplitAttach,
    EmojiAttach,
    QueuedAttach,
    LinkedImageAttach,
)


class ComplexMessageTest(TestCase):
    def test_manual_creation(self) -> None:
        message = ComplexMessage(["Hello, ", RefAttach("user_id_here", "@world")])

        self.assertEqual(message.get_text(), "Hello, @world")
        self.assertEqual(
            message.get_attachments(),
            [{"loci": [[7, 6]], "type": "mentions", "user_ids": ["user_id_here"]}],
        )

    def test_dynamic_creation(self) -> None:
        message = "Hello, " + RefAttach("user_id_here", "@world")

        self.assertEqual(message.get_text(), "Hello, @world")
        self.assertEqual(
            message.get_attachments(),
            [{"loci": [[7, 6]], "type": "mentions", "user_ids": ["user_id_here"]}],
        )

    def test_dynamic_creation_reverse_order(self) -> None:
        message = RefAttach("user_id_here", "@world") + " how are you?"

        self.assertEqual(message.get_text(), "@world how are you?")
        self.assertEqual(
            message.get_attachments(),
            [{"loci": [[0, 6]], "type": "mentions", "user_ids": ["user_id_here"]}],
        )

    def test_str_func(self) -> None:
        message = "test str " + RefAttach("user_id", "with attachment")
        self.assertEqual(
            str(message), str(["test str ", RefAttach("user_id", "with attachment")])
        )

    def test_forward_add(self) -> None:
        message = ComplexMessage("test") + " normal adding"
        self.assertEqual(message.get_text(), "test normal adding")

        message = ComplexMessage("test") + ComplexMessage(" normal adding")
        self.assertEqual(message.get_text(), "test normal adding")

    def test_reverse_add(self) -> None:
        message = "test " + ComplexMessage("reverse adding")
        self.assertEqual(message.get_text(), "test reverse adding")


class SmartSplitComplexMessage(TestCase):
    def test_complex_message(self) -> None:
        message = ComplexMessage(["Hello, ", RefAttach("user_id_here", "@world")])
        text, attachments = smart_split_complex_message(message)
        self.assertEqual(text, "Hello, @world")
        self.assertEqual(
            attachments,
            [{"loci": [[7, 6]], "type": "mentions", "user_ids": ["user_id_here"]}],
        )

    def test_str_message(self) -> None:
        text, attachments = smart_split_complex_message("Hello!")
        self.assertEqual(text, "Hello!")
        self.assertEqual(attachments, [])

    def test_bad_input(self) -> None:
        with self.assertRaises(ValueError):
            smart_split_complex_message(1)  # type: ignore


class MessageAttachTest(TestCase):
    def test_mixing_together(self) -> None:
        message = (
            RefAttach("user1")
            + ImageAttach("http://image.url")
            + LocationAttach("home", 32, 83)
            + SplitAttach("token")
            + EmojiAttach(13, 9)
            + QueuedAttach("queue", "url")
            + LinkedImageAttach("linked_image_url")
        )
        self.assertEqual(message.get_text(), "hometoken\ufffdqueuelinked_image_url")
        self.assertEqual(
            message.get_attachments(),
            [
                {"type": "mentions", "loci": [[0, 0]], "user_ids": ["user1"]},
                {"type": "image", "url": "http://image.url"},
                {"type": "location", "name": "home", "lat": 32, "long": 83},
                {"type": "split", "token": "token"},
                {"type": "emoji", "charmap": [[13, 9]], "placeholder": "\ufffd"},
                {"queues": ["url", "linked_image"], "type": "postprocessing"},
            ],
        )
        self.assertEqual(message.just_str(), "")
        self.assertEqual(
            str(message),
            "[R:, I:, L:home, S:token, E:�, Q: queue, Q: linked_image_url]",
        )

    def test_forward_add(self) -> None:
        message = RefAttach("user_id", "@test") + ComplexMessage(", whats up?")
        self.assertEqual(message.get_text(), "@test, whats up?")


class RefAttachTest(TestCase):
    def test_hidden(self) -> None:
        message = "Test" + RefAttach("user_id_here")
        self.assertEqual(message.get_text(), "Test")
        self.assertEqual(
            message.get_attachments(),
            [{"loci": [[4, 0]], "type": "mentions", "user_ids": ["user_id_here"]}],
        )

    def test_visible(self) -> None:
        message = "Test " + RefAttach("user_id_here", "@all")
        self.assertEqual(message.get_text(), "Test @all")
        self.assertEqual(
            message.get_attachments(),
            [{"loci": [[5, 4]], "type": "mentions", "user_ids": ["user_id_here"]}],
        )

    def test_multiple_in_order(self) -> None:
        message = (
            "Test "
            + RefAttach("user1", "@1")
            + RefAttach("user2", "@2")
            + RefAttach("user3", "@3")
        )
        self.assertEqual(message.get_text(), "Test @1@2@3")
        self.assertEqual(
            message.get_attachments(),
            [
                {
                    "loci": [[5, 2], [7, 2], [9, 2]],
                    "type": "mentions",
                    "user_ids": ["user1", "user2", "user3"],
                }
            ],
        )

    def test_multiple_split(self) -> None:
        message = RefAttach("red_id", "@red") + " vs. " + RefAttach("blue_id", "@blue")
        self.assertEqual(message.get_text(), "@red vs. @blue")
        self.assertEqual(
            message.get_attachments(),
            [
                {
                    "type": "mentions",
                    "loci": [[0, 4], [9, 5]],
                    "user_ids": ["red_id", "blue_id"],
                }
            ],
        )


class ImageAttachTest(TestCase):
    def test_order_independence(self) -> None:
        message1 = ImageAttach("image_url_here") + "Check out my cool image!"
        message2 = "Check out my cool image!" + ImageAttach("image_url_here")

        self.assertEqual(message1.get_text(), message2.get_text())
        self.assertEqual(message1.get_attachments(), message2.get_attachments())
