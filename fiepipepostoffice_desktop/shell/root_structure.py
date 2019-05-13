import typing

from fiepipedesktoplib.assetstructure.shell.structure import GenericTypedAssetsSubdirCommandCommand
from fiepipedesktoplib.assetstructure.shell.structure import StructureRootConfigCommand, StructureAssetConfigCommand
from fiepipedesktoplib.gitstorage.shells.gitroot import Shell as GitRootShell
from fiepipelib.gitstorage.routines.gitasset import GitAssetInteractiveRoutines
from fiepipepostoffice.data.aspect_config import PostOfficeConfiguration
from fiepipepostoffice.data.box_aspect_config import BoxAspectConfig
from fiepipepostoffice.data.delivery_aspect_config import DeliveryAspectConfig
from fiepipepostoffice.routines.root_structure import PostOfficeRootStructureRoutines, PostOfficeApsectRoutines, Box, \
    Section, BoxAspectRoutines, DeliveryAspectRoutines, Delivery
from fiepipelib.git.routines.repo import RepoExists

class PostOfficeCommand(StructureRootConfigCommand[PostOfficeConfiguration, PostOfficeRootStructureRoutines]):
    _boxes_command: "BoxesCommand" = None

    def get_boxes_command(self):
        return self._boxes_command

    def __init__(self, root_shell: GitRootShell):
        super().__init__(root_shell)
        self._boxes_command = BoxesCommand(self)
        self.add_submenu(self._boxes_command, "boxes", [])

    def get_configuration_routines(self) -> PostOfficeApsectRoutines:
        return PostOfficeApsectRoutines(self.get_configuration_data())

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(PostOfficeCommand, self).get_plugin_names_v1()
        ret.append("postoffice_command")
        return ret

    def get_configuration_data(self) -> PostOfficeConfiguration:
        root_routines = self.get_root_shell().get_routines()
        root_routines.load()
        abs_path = root_routines.get_local_repo_path()
        return PostOfficeConfiguration(abs_path)

    def get_structure_routines(self) -> PostOfficeRootStructureRoutines:
        root_routines = self.get_root_shell().get_routines()
        root_routines.load()
        return PostOfficeRootStructureRoutines(root_routines)


class BoxesCommand(GenericTypedAssetsSubdirCommandCommand[
                       PostOfficeCommand, PostOfficeCommand, PostOfficeConfiguration, Box, "BoxCommand"]):
    _post_office_command: PostOfficeCommand = None

    def __init__(self, post_office_command: PostOfficeCommand):
        self._post_office_command = post_office_command
        super().__init__()

    def get_name(self) -> str:
        return "boxes"

    def get_asset_base_path_command(self, name: str) -> "BoxCommand":
        asset_routines = self.get_structure_routines().get_asset_interactive_routines_by_dirname(name)
        asset_routines.load()
        post_office_routines = self._post_office_command.get_structure_routines()
        return BoxCommand(asset_routines, Box(asset_routines, post_office_routines))

    def get_asset_base_path_routines(self, name: str) -> Box:
        asset_routines = self.get_structure_routines().get_asset_routines_by_dirname(name)
        asset_routines.load()
        post_office_routines = self._post_office_command.get_structure_routines()
        return Box(asset_routines, post_office_routines)

    def get_parent_shell(self) -> PostOfficeCommand:
        return self._post_office_command

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(BoxesCommand, self).get_plugin_names_v1()
        ret.append("postoffice.boxes.command")
        return ret


class BoxCommand(StructureAssetConfigCommand[BoxAspectConfig, Box]):
    _incoming_command: "SectionCommand" = None
    _outgoing_command: "SectionCommand" = None
    _box_routines: Box = None

    def __init__(self, asset_routines: GitAssetInteractiveRoutines, box_routines: Box):
        self._box_routines = box_routines
        super().__init__(asset_routines)
        self._incoming_command = SectionCommand(self, "incoming")
        self._outgoing_command = SectionCommand(self, "outgoing")
        self.add_submenu(self._incoming_command, "incoming", [])
        self.add_submenu(self._outgoing_command, "outgoing", [])

    def get_configuration_routines(self) -> BoxAspectRoutines:
        abs_path = self.get_asset_routines().abs_path
        asset_routines = self.get_asset_routines()
        asset_routines.load()
        return BoxAspectRoutines(BoxAspectConfig(abs_path), asset_routines)

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(BoxCommand, self).get_plugin_names_v1()
        ret.append("postoffice.box.command")
        return ret

    def get_configuration_data(self) -> BoxAspectConfig:
        abs_path = self.get_asset_routines().abs_path
        return BoxAspectConfig(abs_path)

    def get_structure_routines(self) -> Box:
        return self._box_routines


class SectionCommand(
    GenericTypedAssetsSubdirCommandCommand[Box, Box, DeliveryAspectConfig, Delivery, "DeliveryCommand"]):
    _box_command: BoxCommand = None

    def get_box_command(self) -> BoxCommand:
        return self._box_command

    _name: str = None

    def get_name(self) -> str:
        return self._name

    def __init__(self, box_command: BoxCommand, name: str):
        self._box_command = box_command
        self._name = name
        super().__init__()

    def get_asset_base_path_command(self, name: str) -> "DeliveryCommand":
        asset_routines = self.get_structure_routines().get_asset_interactive_routines_by_dirname(name)
        asset_routines.load()
        delivery = Delivery(asset_routines, self._box_command.get_structure_routines())
        return DeliveryCommand(asset_routines, delivery)

    def get_asset_base_path_routines(self, name: str) -> Delivery:
        asset_routines = self.get_structure_routines().get_asset_routines_by_dirname(name)
        asset_routines.load()
        return Delivery(asset_routines, self.get_box_command().get_structure_routines())

    def get_structure_routines(self) -> Section:
        if self._name == 'incoming':
            return self._box_command.get_structure_routines().get_incoming()
        elif self._name == "outgoing":
            return self._box_command.get_structure_routines().get_outgoing()
        else:
            raise TypeError("unsupported section name: " + self._name)

    def get_parent_shell(self) -> BoxCommand:
        return self._box_command

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(SectionCommand, self).get_plugin_names_v1()
        ret.append("postoffice.section.command")
        return ret

    def do_new_delivery(self, args):
        """Creates a new delivery using standard naming.
        Usage: new_delivery"""
        self.do_coroutine(self.get_structure_routines().create_new_delivery_routine(self.get_feedback_ui()))

    def complete_checkout(self, text, line, begidx, endidx):
        return self.asset_name_complete(text, line, begidx, endidx)

    def do_checkout(self, args):
        """Pulls down and checks out a delivery to the local storage.

        usage: checkout [delivery]

        arg delivery: the name of the delivery to checkout."""
        args = self.parse_arguments(args)
        if len(args) < 1:
            self.perror("No delivery given.")
            return

        routines = self.get_structure_routines()
        asset_routines = routines.get_asset_routines_by_dirname(args[0])
        asset_routines.load()
        abs_path = asset_routines.abs_path
        if RepoExists(abs_path):
            self.perror("Asset already exists at that path:" + abs_path)
            return
        self.do_coroutine(routines.checkout_by_dirname_routine(args[0], self.get_feedback_ui()))


class DeliveryCommand(StructureAssetConfigCommand[DeliveryAspectConfig, Delivery]):
    _delivery: Delivery = None

    def __init__(self, asset_routines: GitAssetInteractiveRoutines, delivery: Delivery):
        self._delivery = delivery
        super().__init__(asset_routines)

    def get_configuration_routines(self) -> DeliveryAspectRoutines:
        asset_routines = self.get_asset_routines()
        asset_routines.load()
        config = DeliveryAspectConfig(asset_routines.abs_path)
        return DeliveryAspectRoutines(config, asset_routines)

    def get_plugin_names_v1(self) -> typing.List[str]:
        ret = super(DeliveryCommand, self).get_plugin_names_v1()
        ret.append("postoffice.delivery.command")
        return ret

    def get_configuration_data(self) -> DeliveryAspectConfig:
        asset_routines = self.get_asset_routines()
        asset_routines.load()
        return DeliveryAspectConfig(asset_routines.abs_path)

    def get_structure_routines(self) -> Delivery:
        return self._delivery

    def do_is_locked(self, args):
        """Indicates if the delivery is locked.

        Usage: is_locked"""
        args = self.parse_arguments(args)
        config = self.get_configuration_data()
        if not config.exists():
            self.perror("Delivery is not configured.")
            return
        config.load()
        if config.get_locked():
            self.poutput("Yes")
            return
        else:
            self.poutput("No")
            return

    def do_commit_and_lock(self, args):
        """Locks the delivery to prevent further changes.

        Will error if already locked.

        Usage: commit_and_lock
        """
        args = self.parse_arguments(args)
        routines = self.get_structure_routines()
        self.do_coroutine(routines.commit_and_lock_routine(self.get_feedback_ui()))

    def do_unlock(self, args):
        """Unlocks the delivery.  This should very rarely be done.  A delivery should typically be made once.

        Usage: unlock"""
        args = self.parse_arguments(args)
        routines = self.get_structure_routines()
        self.do_coroutine(routines.unlock_routine(self.get_feedback_ui()))

    def do_archive_and_remove(self, args):
        """Pushes a locked delivery to GitLab and then removes it from the local storage.
        Upon succesful removal, will exit this command.

        Errors if the push fails or the delivery isn't commited and locked.

        Usage: archive_and_remove"""
        args = self.parse_arguments(args)
        routines = self.get_structure_routines()
        (success, message) = self.do_coroutine(routines.archive_and_remove(self.get_feedback_ui()))
        if not success:
            self.perror(message)
        else:
            self.poutput(message)
        return True
