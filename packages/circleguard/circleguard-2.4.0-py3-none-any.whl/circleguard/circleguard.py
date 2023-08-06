from pathlib import Path
import sys
import itertools
import os
from os.path import isfile, join
import logging
from tempfile import TemporaryDirectory

from circleguard.loader import Loader
from circleguard.comparer import Comparer
from circleguard.investigator import Investigator
from circleguard.cacher import Cacher
from circleguard import config
from circleguard.exceptions import CircleguardException
from circleguard.replay import Check, ReplayMap, ReplayPath, Replay, Map, Container
from circleguard.enums import Detect, RatelimitWeight
from slider import Beatmap, Library


class Circleguard:
    """
    Circleguard compares and investigates replays to detect cheats.

    Circleguard provides convenience methods for common use cases: map_check, verify, user_check, and local_check -
    see each method for further documentation. If these convenience methods are not flexible enough for you, you can instantiate
    a Container such as Check or Map and call circleguard.run(container).

    Under the hood, convenience methods simply instantiate a Check object and call circleguard#run(check). The run method
    returns a generator containing Result objects, which contains the result of each comparison of the replays. See the
    Result class for further documentation.
    """

    # used to distinguish log output for cg instances
    NUM = 1

    def __init__(self, key, db_path=None, slider_dir=None, loader=None):
        """
        Initializes a Circleguard instance.

        Args:
            String key: An osu API key.
            [Path or String] db_path: A pathlike object to the databsae file to write and/or read cached replays.
                    If the given file doesn't exist, a fresh database if created. If this is not passed,
                    no replays will be cached or loaded from cache.
            [Path or String] slider_dir: A pathlike object to the directory used by slider to store beatmaps. If None,
                    a temporary directory will be created, and destroyed when this circleguard object is garbage collected.
            Class loader: a subclass of circleguard.Loader, which will be used in place of circleguard.Loader if passed.
                    Instantiated with two args - a key and cacher.
        """

        cacher = None
        if db_path is not None:
            # allows for . to be passed to db_path
            db_path = Path(db_path).absolute()
            cacher = Cacher(config.cache, db_path)

        self.log = logging.getLogger(__name__ + str(Circleguard.NUM))
        # allow for people to pass their own loader implementation/subclass
        self.loader = Loader(key, cacher=cacher) if loader is None else loader(key, cacher)
        self.options = Options()
        if slider_dir is None:
            # have to keep a reference to it or the folder gets deleted and can't be walked by Library
            self.__slider_dir = TemporaryDirectory()
            self.library = Library(self.__slider_dir.name)
        else:
            self.library = Library(slider_dir)

        Circleguard.NUM += 1

    def run(self, container):
        """
        Compares and investigates replays in the container for cheats.

        Args:
            Continer container: The container with replays to look at.

        Returns:
            A generator containing Result objects of the comparisons and investigations.
        """
        cont = container
        self.log.info("Running circleguard with %r", cont)

        cont.filter(self.loader)
        # Containers are instantiated without relation to a cg instance by necessity of
        # easy of use. This means if it is not given an option, it will default to
        # the config value at that time, not the circleguard's option value, which has
        # higher priority than the config value. So we change it here, and only so late
        # because this is the first time the Container gets tied to a cg instance and we are
        # able to give it the cg's option. But don't overwrite the option if it was
        # passed to the Container (will be different from the config value if that is the case).
        # TODO work on cases where config value is changed after container instantiation but before
        # cg is run
        o = self.options
        cont.cascade_options(cache=o.cache, steal_thresh=o.steal_thresh, rx_thresh=o.rx_thresh, detect=o.detect)
        cont.load(self.loader)

        # steal check
        compare1 = [replay for replay in cont.all_replays() if replay.detect & Detect.STEAL]
        compare2 = [replay for replay in cont.all_replays2() if replay.detect & Detect.STEAL]
        # all replays now have replay data, above is where ratelimit waiting would occur
        comparer = Comparer(cont.steal_thresh, compare1, replays2=compare2)
        yield from comparer.compare()

        for replay in cont.all_replays():
            if not replay.detect & Detect.RELAX:
                continue
            bm = self.library.lookup_by_id(replay.map_id, download=True, save=True)
            investigator = Investigator(replay, bm, cont.rx_thresh)
            yield from investigator.investigate()


    def map_check(self, map_id, u=None, num=None, cache=None, steal_thresh=None, rx_thresh=None, mods=None, include=None, detect=None, span=None):
        """
        Checks a map's leaderboard for replay steals.

        Args:
            Integer map_id: The id of the map (not the id of the mapset!) to compare replays from.
            Integer u: A user id. If passed, only the replay made by this user id on the given map will be
                    compared with the rest of the lederboard of the map. No other comparisons will be made.
            Integer num: The number of replays to compare from the map. Defaults to 50, or the config value if changed.
                    Loads from the top ranks of the leaderboard, so num=20 will compare the top 20 scores. This
                    number must be between 1 and 100, as restricted by the osu api.
            Boolean cache: Whether to cache the loaded replays. Defaults to False, or the config value if changed.
                    If no database file was passed, this value has no effect, as replays will not be cached.
            Integer steal_thresh: If a comparison scores below this value, its Result object has ischeat set to True.
                    Defaults to 18, or the config value if changed.
            Integer rx_thresh: if a replay has a ur below this value, it is considered cheated.
                    Deaults to 50, or the config value if changed.
            Integer mods: If passed, download and compare the top num replays set with these exact mods. You can find a
                    reference on what mod maps to what integer value here: https://github.com/ppy/osu-api/wiki#mods.
                    There is currently no support for optional mods (eg HR is required, but other mods optional,
                    so both HR and HDHR scores would be downloaded). This is due to api limitations.
                    If both mods and u are passed, the user's replay will be downloaded regardless of the passed mods,
                    (ie their highest scoring play on the map), but the other replays it is compared against will
                    be downloaded according to the passed mods.
            Function include: A Predicate function that returns True if the replay should be loaded, and False otherwise.
                    The include function will be passed a single argument - the circleguard.Replay object, or one
                    of its subclasses.
            Detect detect: What cheats to run tests to detect for replays on this map.
            String span: A comma separated list of ranges of top replays to check on the map. "1-3" will check the first 3 replays,
                    and "1-3,6,2-4" will check replays 1,2,3,4,6 for instance. Values that appear multiple times or in multiple ranges
                    are only counted once.

        Returns:
            A generator containing Result objects of the comparisons.
        """
        check = self.create_map_check(map_id, u, num, cache, steal_thresh, mods, include, detect, span)
        yield from self.run(check)


    def create_map_check(self, map_id, u=None, num=None, cache=None, steal_thresh=None, mods=None, include=None, detect=None, span=None):
        """
        Creates the Check object used in the map_check convenience method. See that method for more information.
        """
        options = self.options
        num = num if num is not None else options.num
        cache = cache if cache is not None else options.cache
        steal_thresh = steal_thresh if steal_thresh is not None else options.steal_thresh
        include = include if include is not None else options.include
        detect = detect if detect is not None else options.detect

        self.log.info("Map check with map id %d, u %s, num %s, cache %s, steal_thresh %s", map_id, u, num, cache, steal_thresh)

        replays = [Map(map_id, num=num, cache=cache, mods=mods, detect=detect, span=span)]
        replays2 = [ReplayMap(map_id, u, mods=mods)] if u else None

        return Check(replays, loadables2=replays2, cache=cache, steal_thresh=steal_thresh, include=include, detect=detect)

    def verify(self, map_id, u1, u2, cache=None, steal_thresh=None, include=None):
        """
        Verifies that two user's replay on a map are steals of each other.

        Args:
            Integer map_id: The id of the map to compare replays from.
            Integer u1: The user id of one of the users who set a replay on this map.
            Integer u2: The user id of the second user who set a replay on this map.
            Boolean cache: Whether to cache the loaded replays. Defaults to False, or the config value if changed.
                    If no database file was passed, this value has no effect, as replays will not be cached.
            Integer steal_thresh: If a comparison scores below this value, its Result object has ischeat set to True.
                    Defaults to 18, or the config value if changed.
            Function include: A Predicate function that returns True if the replay should be loaded, and False otherwise.
                    The include function will be passed a single argument - the circleguard.Replay object, or one
                    of its subclasses.

        Returns:
            A generator containing Result objects of the comparisons.
        """

        check = self.create_verify_check(map_id, u1, u2, cache, steal_thresh, include)
        yield from self.run(check)

    def create_verify_check(self, map_id, u1, u2, cache=None, steal_thresh=None, include=None):
        """
        Creates the Check object used in the verify_check convenience method. See that method for more information.
        """
        options = self.options
        cache = cache if cache is not None else options.cache
        steal_thresh = steal_thresh if steal_thresh is not None else options.steal_thresh
        include = include if include is not None else options.include

        self.log.info("Verify with map id %d, u1 %s, u2 %s, cache %s", map_id, u1, u2, cache)
        info1 = self.loader.user_info(map_id, user_id=u1)
        info2 = self.loader.user_info(map_id, user_id=u2)
        replay1 = ReplayMap(info1.map_id, info1.user_id, info1.mods)
        replay2 = ReplayMap(info2.map_id, info2.user_id, info2.mods)

        return Check([replay1, replay2], cache=cache, steal_thresh=steal_thresh, include=include, detect=Detect.STEAL)

    def user_check(self, u, num_top, num_users, cache=None, steal_thresh=None, include=None, detect=None, span=None):
        """
        Checks a user's top plays for replay steals.

        For each of the user's top plays, the replay will be compared to the top plays of the map,
        then compared to all the user's other plays on the map, to check for both stealing and remodding.

        If a user has no or only one downloadable replay on the map, no comparisons to the user's other plays are made.
        Obviously, if the play is not downloadable, no comparison is made against the map leaderboard for that replay either.

        Args:
            Integer u: The user id of the user to check.
            Integer num_top: The number of top plays of the user to check for stealing and remodding.
                    This is the total number of plays to check, not the number of plays with replay data -
                    eg if a user only has 3 replays with data available in his top 50, num=50 will result in
                    those 3 replays being checked, not the first 50 the user has data for.
            Integer num_users: The number of replays on each map to compare against the user's replay.
            Boolean cache: Whether to cache the loaded replays. Defaults to False, or the config value if changed.
                    If no database file was passed, this value has no effect, as replays will not be cached.
            Integer steal_thresh: If a comparison scores below this value, its Result object has ischeat set to True.
                    Defaults to 18, or the config value if changed.
            Function include: A Predicate function that returns True if the replay should be loaded, and False otherwise.
                    The include function will be passed a single argument - the circleguard.Replay object, or one
                    of its subclasses.
            Detect detect: What cheats to run tests to detect.
            String span: A comma separated list of ranges of top plays to check. "1-3" will check the top 3 plays,
                    and "1-3,6,2-4" will check top plays 1,2,3,4,6 for instance. Values that appear multiple times or in multiple ranges
                    are only counted once. Just like normal, if the user does not have a replay available for one of the top plays in the span,
                    it will be skipped. The span refers to all of the user's top plays, not just the ones they have a replay available for.

        Returns:
            A generator containing Result objects of the comparisons.
        """

        for check_list in self.create_user_check(u, num_top, num_users, cache, steal_thresh, include, detect, span):
            # yuck; each top play has two different checks (remodding and stealing)
            # which is why we need a double loop
            for check in check_list:
                yield from self.run(check)

    def create_user_check(self, u, num_top, num_users, cache=None, steal_thresh=None, include=None, detect=None, span=None):
        """
        Creates the Check object used in the user_check convenience method. See that method for more information.

        Bewarned that this method does not return a single Check object like all other circleguard#create methods.
        Instead it returns a list of lists of Check objects [[Check, Check], [Check, Check], ...], because each top
        play of the user needs two Check objects, one for replay stealing and one for remodding. Be sure to handle
        this special case accordingly.
        """
        options = self.options
        cache = cache if cache is not None else options.cache
        steal_thresh = steal_thresh if steal_thresh is not None else options.steal_thresh
        include = include if include is not None else options.include
        detect = detect if detect is not None else options.detect

        self.log.info("User check with u %s, num_top %s, num_users %s", u, num_top, num_users)
        ret = []
        for map_id in self.loader.get_user_best(u, num_top, span=span):
            info = self.loader.user_info(map_id, user_id=u)
            ureplay_id = info.replay_id # user replay id
            if not info.replay_available:
                continue  # if we can't download the user's replay on the map, we have nothing to compare against
            user_replay = [ReplayMap(info.map_id, info.user_id, mods=info.mods)]

            infos = self.loader.user_info(map_id, num=num_users)
            replays = []
            for info in infos:
                if info.replay_id == ureplay_id:
                    self.log.debug("Removing map %s, user %s, mods %s from user check with "
                                   "the same replay id as the user's replay", info.map_id, info.user_id, info.mods)
                    continue
                replays.append(ReplayMap(info.map_id, info.user_id, info.mods))

            remod_replays = []
            for info in self.loader.user_info(map_id, user_id=u, limit=False)[1:]:
                remod_replays.append(ReplayMap(info.map_id, info.user_id, mods=info.mods))

            check1 = Check(user_replay, loadables2=replays, cache=cache, steal_thresh=steal_thresh, include=include, detect=detect)
            check2 = Check(user_replay + remod_replays, cache=cache, steal_thresh=steal_thresh, include=include, detect=detect)
            ret.append([check1, check2])

        return ret


    def local_check(self, folder, map_id=None, u=None, num=None, cache=None, steal_thresh=None, include=None, detect=None):
        """
        Compares locally stored osr files for replay steals.

        Args:
            [Path or String] folder: A pathlike object to the directory containing osr files.
            Integer map_id: A map id. If passed, the osr files will be compared against the top
                            plays on this map (50 by default).
            Integer u: A user id. If both this and map_id are passed, the osr files will be compared
                       against the user's play on the map. This value has no effect if passed without map_id.
            Integer num: The number of replays to compare from the map. Defaults to 50, or the config value if changed.
                         Loads from the top ranks of the leaderboard, so num=20 will compare the top 20 scores. This
                         number must be between 1 and 100, as restricted by the osu api. This value has no effect
                         if passed with both u and map_id.
            Boolean cache: Whether to cache the loaded replays. Defaults to False, or the config value if changed.
                           If no database file was passed, this value has no effect, as replays will not be cached.
            Integer steal_thresh: If a comparison scores below this value, its Result object has ischeat set to True.
                            Defaults to 18, or the config value if changed.
            Function include: A Predicate function that returns True if the replay should be loaded, and False otherwise.
                              The include function will be passed a single argument - the circleguard.Replay object, or one
                              of its subclasses.
            Detect detect: What cheats to run tests to detect.

        Returns:
            A generator containing Result objects of the comparisons.
        """

        check = self.create_local_check(folder, map_id, u, num, cache, steal_thresh, include, detect)
        yield from self.run(check)

    def create_local_check(self, folder, map_id=None, u=None, num=None, cache=None, steal_thresh=None, include=None, detect=None):
        """
        Creates the Check object used in the local_check convenience method. See that method for more information.
        """
        options = self.options
        num = num if num is not None else options.num
        cache = cache if cache is not None else options.cache
        steal_thresh = steal_thresh if steal_thresh is not None else options.steal_thresh
        include = include if include is not None else options.include
        detect = detect if detect is not None else options.detect

        paths = [folder / f for f in os.listdir(folder) if isfile(folder / f) and f.endswith(".osr")]
        local_replays = [ReplayPath(path) for path in paths]
        online_replays = None
        if map_id:
            if u:
                infos = [self.loader.user_info(map_id, user_id=u)]
            else:
                # num guaranteed to be defined, either passed or from settings.
                infos = self.loader.user_info(map_id, num=num)

            online_replays = [ReplayMap(info.map_id, info.user_id, info.mods) for info in infos]

        return Check(local_replays, loadables2=online_replays, steal_thresh=steal_thresh, include=include, detect=detect)

    def load(self, loadable):
        """
        Loads the given loadable. This is identical to calling loadable.load(cg.loader).
        """
        loadable.load(self.loader)

    def set_options(self, steal_thresh=None, rx_thresh=None, num=None, cache=None, failfast=None, loglevel=None, include=None, detect=None):
        """
        Changes the default value for different options in circleguard.
        Affects only the ircleguard instance this method is called on.

        Args:
            Integer steal_thresh: If a comparison scores below this value, its Result object has ischeat set to True. 18 by default.
            Integer rx_thresh: if a replay has a ur below this value, it is considered cheated. 50 by default.
            Integer num: How many loadables to load from a map when doing a map check. 50 by default.
            Boolean cache: Whether to cache the loaded loadables. Defaults to False, or the config value if changed.
                           If no database file was passed, this value has no effect, as loadables will not be cached.
            Boolean failfast: Will throw an exception if no comparisons can be made for a given Check object,
                          or silently make no comparisons otherwise. False by default.
            Integer loglevel: What level to log at. Circlecore follows standard python logging levels, with an added level of
                          TRACE with a value of 5 (lower than debug, which is 10). The value passed to loglevel is
                          passed directly to the setLevel function of this instance's logger. WARNING by default.
                          For more information on log levels, see the standard python logging lib.
            Function include: A Predicate function that returns True if the replay should be loaded, and False otherwise.
                          The include function will be passed a single argument - the circleguard.Replay object, or one
                          of its subclasses.
            Detect detect: What cheats to run tests to detect.
        """

        for k, v in locals().items():
            if v is None or k == "self":
                continue
            if k == "loglevel":
                self.log.setLevel(loglevel)
                continue
            if hasattr(self.options, k):
                setattr(self.options, k, v)
            else:  # this only happens if we fucked up, not the user's fault
                raise CircleguardException(f"The key {k} (value {v}) is not available as a config option for a circleguard instance")

def set_options(steal_thresh=None, rx_thresh=None, num=None, cache=None, failfast=None, loglevel=None, include=None, detect=None):
    """
    Changes the default value for different options in circleguard.
    Affects all circleguard instances, even ones that have already been instantiated.

    Args:
        Integer steal_thresh: If a comparison scores below this value, its Result object has ischeat set to True. 18 by default.
        Integer rx_thresh: if a replay has a ur below this value, it is considered cheated. 50 by default.
        Integer num: How many loadables to load from a map when doing a map check. 50 by default.
        Boolean cache: Whether to cache the loaded loadables. Defaults to False, or the config value if changed.
                       If no database file was passed to a circleguard instance, this value has no effect, as loadables will not be cached.
        Boolean failfast: Will throw an exception if no comparisons can be made for a given Check object,
                          or silently make no comparisons otherwise. False by default.
        Integer loglevel: What level to log at. Circlecore follows standard python logging levels, with an added level of
                          TRACE with a value of 5 (lower than debug, which is 10). The value passed to loglevel is
                          passed directly to the setLevel function of the circleguard root logger. WARNING by default.
                          For more information on log levels, see the standard python logging lib.
        Function include: A Predicate functrion that returns True if the replay should be loaded, and False otherwise.
                          The include function will be passed a single argument - the circleguard.Replay object, or one
                          of its subclasses.
        Detect detect: What cheats to run tests to detect.
    """

    for k, v in locals().items():
        if v is None:
            continue
        if k == "loglevel":
            logging.getLogger("circleguard").setLevel(loglevel)
            continue
        if hasattr(config, k):
            setattr(config, k, v)
        else:  # this only happens if we fucked up, not the user's fault
            raise CircleguardException(f"The key {k} (with value {v}) is not available as a config option for global config")



class Options():
    """
    Container class for options, tied to a specific Circleguard instance.
    """

    def __init__(self):
        # underscores to not call the @property functions when
        # accessing these attributes
        self._steal_thresh = None
        self._rx_thresh = None
        self._num = None
        self._cache = None
        self._failfast = None
        self._include = None
        self._detect = None

    # These methods are unfortunately necessary because when config module
    # variables are updated, references to them are not - ie references to
    # config.steal_thresh (or any other) are by value. So, when we access options
    # attributes, just get the latest config variable with these methods.
    @property
    def steal_thresh(self):
        return config.steal_thresh if self._steal_thresh is None else self._steal_thresh
    @steal_thresh.setter
    def steal_thresh(self, v):
        self._steal_thresh = v

    @property
    def rx_thresh(self):
        return config.rx_thresh if self._rx_thresh is None else self._rx_thresh
    @rx_thresh.setter
    def rx_thresh(self, v):
        self._rx_thresh = v

    @property
    def num(self):
        return config.num if self._num is None else self._num
    @num.setter
    def num(self, v):
        self._num = v

    @property
    def cache(self):
        return config.cache if self._cache is None else self._cache
    @cache.setter
    def cache(self, v):
        self._cache = v

    @property
    def failfast(self):
        return config.failfast if self._failfast is None else self._failfast
    @failfast.setter
    def failfast(self, v):
        self._failfast = v

    @property
    def include(self):
        return config.include if self._include is None else self._include
    @include.setter
    def include(self, v):
        self._include = v

    @property
    def detect(self):
        return config.detect if self._detect is None else self._detect
    @detect.setter
    def detect(self, v):
        self._detect = v
