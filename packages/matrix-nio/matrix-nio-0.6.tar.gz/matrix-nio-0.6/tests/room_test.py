import pytest

from helpers import faker
from nio.events import (InviteAliasEvent, InviteMemberEvent, InviteNameEvent,
                        RoomCreateEvent, RoomGuestAccessEvent,
                        RoomHistoryVisibilityEvent, RoomJoinRulesEvent,
                        RoomNameEvent, TypingNoticeEvent)
from nio.responses import RoomSummary
from nio.rooms import MatrixInvitedRoom, MatrixRoom

TEST_ROOM = "!test:example.org"
BOB_ID = "@bob:example.org"

class TestClass(object):
    def _create_test_data(self):
        pass

    @property
    def new_user(self):
        return faker.mx_id(), faker.name(), faker.avatar_url()

    @property
    def test_room(self):
        return MatrixRoom(TEST_ROOM, BOB_ID)

    def test_room_creation(self):
        room = self.test_room
        assert room

    def test_adding_members(self):
        room = self.test_room
        assert not room.users
        mx_id, name, avatar = self.new_user
        room.add_member(mx_id, name, avatar)
        assert room.users
        assert room.members_synced
        assert room.member_count == 1
        member = list(room.users.values())[0]
        assert member.user_id == mx_id
        assert member.display_name == name
        assert member.avatar_url == avatar

    def test_named_checks(self):
        room = self.test_room
        assert not room.is_named
        assert room.is_group

        room.name = "Test room"

        assert room.is_named
        assert not room.is_group

    def test_name_calculation_when_unnamed_with_no_members(self):
        room = self.test_room
        assert room.display_name == "Empty room?"
        assert room.named_room_name() == None

    def test_name_calculation_when_unnamed_with_members(self):
        room = self.test_room
        room.add_member("@alice:example.org", "Alice", None)
        assert room.display_name == "Alice"

        room.add_member(BOB_ID, "Bob", None)
        assert room.display_name == "Alice"

        room.add_member("@malory:example.org", "Alice", None)
        assert (room.display_name ==
                "Alice (@alice:example.org) and Alice (@malory:example.org)")
        room.add_member("@steve:example.org", "Steve", None)
        assert (room.display_name ==
                "Alice (@alice:example.org) and 2 others")

    def test_name_calculation_with_canonical_alias(self):
        room = self.test_room
        room.canonical_alias = "#test:termina.org.uk"
        assert room.display_name == "#test:termina.org.uk"

    def test_name_calculation_prefer_name_over_alias(self):
        room = self.test_room
        room.canonical_alias = "#test:termina.org.uk"
        room.name = "Test room"
        assert room.display_name == "Test room"

    def test_name_calculation_when_hash_already_prefixed(self):
        room = self.test_room

        room.name = "#test"
        assert room.display_name == "#test"

    def test_user_name_calculation(self):
        room = self.test_room

        room.add_member("@alice:example.org", "Alice", None)
        assert room.user_name("@alice:example.org") == "Alice"
        assert room.user_name_clashes("Alice") == ["@alice:example.org"]

        room.add_member("@bob:example.org", None, None)
        assert room.user_name("@bob:example.org") == "@bob:example.org"

        room.add_member("@malory:example.org", "Alice", None)
        assert room.user_name("@alice:example.org") == "Alice (@alice:example.org)"
        assert room.user_name("@malory:example.org") == "Alice (@malory:example.org)"
        assert room.user_name_clashes("Alice") == ["@alice:example.org", "@malory:example.org"]

        room.remove_member("@alice:example.org")
        assert room.user_name("@malory:example.org") == "Alice"

        room.remove_member("@malory:example.org")
        room.add_member("@alice:example.org", None, None)
        assert room.user_name("@alice:example.org") == "@alice:example.org"
        assert room.user_name_clashes("@alice:example.org") == ["@alice:example.org"]

        room.add_member("@malory:example.org", "@alice:example.org", None)
        assert room.user_name("@alice:example.org") == "@alice:example.org"
        assert room.user_name("@malory:example.org") == "@alice:example.org (@malory:example.org)"
        assert room.user_name_clashes("@alice:example.org") == ["@alice:example.org", "@malory:example.org"]

    def test_machine_name(self):
        room = self.test_room
        assert room.machine_name == TEST_ROOM
        room.canonical_alias = "Alias room"
        assert room.machine_name == "Alias room"

    def test_typing_notice_event(self):
        room = self.test_room
        assert not room.typing_users

        room.handle_ephemeral_event(TypingNoticeEvent([BOB_ID]))
        assert room.typing_users == [BOB_ID]

    def test_create_event(self):
        room = self.test_room
        assert not room.creator
        room.handle_event(
                RoomCreateEvent(
                    {
                        "event_id": "event_id",
                        "sender": BOB_ID,
                        "origin_server_ts": 0
                    },
                    BOB_ID, False
                )
        )
        assert room.creator == BOB_ID
        assert room.federate is False
        assert room.room_version == "1"

    def test_guest_access_event(self):
        room = self.test_room
        assert room.guest_access == "forbidden"
        room.handle_event(
            RoomGuestAccessEvent(
                {
                    "event_id": "event_id",
                    "sender": BOB_ID,
                    "origin_server_ts": 0
                },
                "can_join"
            )
        )
        assert room.guest_access == "can_join"

    def test_history_visibility_event(self):
        room = self.test_room
        assert room.history_visibility == "shared"
        room.handle_event(
            RoomHistoryVisibilityEvent(
                {
                    "event_id": "event_id",
                    "sender": BOB_ID,
                    "origin_server_ts": 0
                },
                "invited"
            )
        )
        assert room.history_visibility == "invited"

    def test_join_rules_event(self):
        room = self.test_room
        assert room.join_rule == "invite"
        room.handle_event(
            RoomJoinRulesEvent(
                {
                    "event_id": "event_id",
                    "sender": BOB_ID,
                    "origin_server_ts": 0
                },
                "public"
            )
        )
        assert room.join_rule == "public"

    def test_name_event(self):
        room = self.test_room
        assert not room.name
        room.handle_event(
            RoomNameEvent(
                {
                    "event_id": "event_id",
                    "sender": BOB_ID,
                    "origin_server_ts": 0
                },
                "test name"
            )
        )
        assert room.name == "test name"

    def test_summary_update(self):
        room = self.test_room
        assert not room.summary

        room.update_summary(RoomSummary(1, 2, []))
        assert room.member_count == 2
        assert room.summary

        room.update_summary(RoomSummary(1, 3, ["@alice:example.org"]))
        assert room.member_count == 3
        assert room.summary.heroes == ["@alice:example.org"]

    def test_invited_room(self):
        room = MatrixInvitedRoom(TEST_ROOM, BOB_ID)
        room.handle_event(InviteMemberEvent(
            {},
            "@alice:example.org",
            BOB_ID,
            "invite",
            None,
            {
                "membership": "invite"
            }
        ))
        assert room.inviter == "@alice:example.org"
        assert not room.name

        room.handle_event(InviteNameEvent({}, BOB_ID, "test name"))
        assert room.name == "test name"

        assert not room.canonical_alias
        room.handle_event(InviteAliasEvent({}, BOB_ID, "test alias"))
        assert room.canonical_alias == "test alias"

    def test_handle_member_return_value(self):
        room = self.test_room
        assert not room.users
        mx_id, name, avatar = self.new_user
        assert room.add_member(mx_id, name, avatar)
        assert not room.add_member(mx_id, name, avatar)

        assert room.remove_member(mx_id)
        assert not room.remove_member(mx_id)
