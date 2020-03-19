"""
LoadLocationData.py - Load location data into Row/Bin/Tier and Location tables.

Although the Constraints table has the min/max or list values this program
needs, the values are hard coded here because the records in the Constraints
table are about to go away.

The philosophy used here is that there are certain essential rows, bins,
and tiers that make up the components of warehouse locations.  This program
will add those rows, bins, tiers and locations to the database.  This
program doesn't care if the descriptions for these records have changed,
but requires that records with specific keys must be present in the
database.  Once the database has been pre-loaded, the users are free to
make changes as desired.
"""

import logging
import logging.config
from contextlib import contextmanager
from logging import getLogger, debug, error
from pathlib import Path
from typing import Any, Union, Optional, NamedTuple

from sqlalchemy import create_engine, engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, insert
import yaml  # from PyYAML library

from FPIDjango.private import settings_private

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "06/28/2019"
# Copyright 2019 by Travis Risner - MIT License

log = None

"""
# # # # #
Constants
# # # # #
"""
ROW_MIN = 1
""" Minimum row number """
ROW_MAX = 4
""" Maximum row number """
BIN_MIN = 1
""" Minimum bin number """
BIN_MAX = 9
""" Maximum bin number """
TIER_LIST = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
""" List of valid tier names """

ECHO_SQL_TO_LOG = True
""" Indicator of if the SQL statements should be copied to the log """

"""
# # # # # # # # # # # #
SQLAlchemy Declarations
# # # # # # # # # # # #
"""
Base = automap_base()

# configure Session class with desired options
Session = sessionmaker()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class LoadLocationDataClass:
    """
    LoadLocationDataClass - Load location data into location tables.
    """

    # Pre-declare tables that I want to manage.
    class LocRow(Base):
        """ Location Row table definition """
        __tablename__ = 'fpiweb_locrow'

    class LocBin(Base):
        """ Location Bin table definition """
        __tablename__ = 'fpiweb_locbin'

    class LocTier(Base):
        """ Location Tier table definition """
        __tablename__ = 'fpiweb_loctier'

    class Location(Base):
        """ Location table definition """
        __tablename__ = 'fpiweb_location'

    def __init__(self):
        # database connection information
        self.engine = None
        return

    def run_load_loc_data(self):
        """
        Top method for running Load location data into tables.

        :return:
        """
        # establish access to the database
        self.engine = self.connect(
            user=settings_private.DB_USER,
            password=settings_private.DB_PSWD,
            db=settings_private.DB_NAME,
            host=settings_private.DB_HOST,
            port=settings_private.DB_PORT
        )

        # populate the table columns and relationships via reflection
        Base.prepare(self.engine, reflect=True)

        # bind the engine to the session
        Session.configure(bind=self.engine)

        # load the various location tables in a session
        with session_scope() as session:
            self.load_row_table(session)
            self.load_bin_table(session)
            self.load_tier_table(session)
            self.load_location_table(session)

        return

    def connect(self, user: str, password: str, db: str, host:
    str = 'localhost', port: int = 5432) -> engine:
        """
        Establish a connection to the desired PostgreSQL database.

        :param user:
        :param password:
        :param db:
        :param host:
        :param port:
        :return:
        """

        # We connect with the help of the PostgreSQL URL
        # postgresql://federer:grandestslam@localhost:5432/tennis
        url = f'postgresql://{user}:{password}@{host}:{port}/{db}'

        # The return value of create_engine() is our connection object
        con = create_engine(url, client_encoding='utf8', echo=ECHO_SQL_TO_LOG)
        return con

    def load_row_table(self, session: Session):
        """
        Load the row table with values from min to max.

        :session:
        :return:
        """
        for row_ind in range(ROW_MIN, ROW_MAX + 1):
            row_key = f'{row_ind:02}'
            row_descr = f'Row {row_key}'
            try:
                session.add(self.LocRow(loc_row=row_key,
                                        loc_row_descr=row_descr))
                session.commit()
            except IntegrityError:
                print(f'Row {row_ind} already exists')
                session.rollback()

        for record in session.query(self.LocRow):
            print(f'Row: {record.loc_row}  {record.loc_row_descr} ')

        return

    def load_bin_table(self, session: Session):
        """
        Load the bin table with values from min to max.

        :return:
        """
        for bin_ind in range(BIN_MIN, BIN_MAX + 1):
            bin_key = f'{bin_ind:02}'
            bin_descr = f'Bin {bin_key}'
            try:
                session.add(self.LocBin(loc_bin=bin_key,
                                        loc_bin_descr=bin_descr))
                session.commit()
            except IntegrityError:
                print(f'Bin {bin_ind} already exists')
                session.rollback()

        for record in session.query(self.LocBin):
            print(f'Bin: {record.loc_bin}  {record.loc_bin_descr} ')

    def load_tier_table(self, session: Session):
        """
        Load the tier table with values from the list.

        :return:
        """
        for tier_ind in TIER_LIST:
            tier_key = f'{tier_ind}'
            tier_descr = f'Tier {tier_key}'
            try:
                session.add(self.LocTier(loc_tier=tier_key,
                                         loc_tier_descr=tier_descr))
                session.commit()
            except IntegrityError:
                print(f'Tier {tier_ind} already exists')
                session.rollback()

        for record in session.query(self.LocTier):
            print(f'Tier: {record.loc_tier}  {record.loc_tier_descr} ')

    def load_location_table(self, session: Session):
        """
        Construct location records from the row/bin/tier records.

        The location code consists of the row code, bin code, and tier code
        jammed together into a six character id.

        :return:
        """
        for my_row in session.query(self.LocRow):
            for my_bin in session.query(self.LocBin):
                for my_tier in session.query(self.LocTier):
                    loc_code = (
                        f'{my_row.loc_row}{my_bin.loc_bin}{my_tier.loc_tier}'
                    )
                    loc_descr = (
                        f'Row {my_row.loc_row} '
                        f'Bin {my_bin.loc_bin} '
                        f'Tier {my_tier.loc_tier}'
                    )
                    loc_in_warehouse = True
                    try:
                        session.add(
                            self.Location(
                                loc_code=loc_code,
                                loc_descr=loc_descr,
                                loc_row_id=my_row.id,
                                loc_bin_id=my_bin.id,
                                loc_tier_id=my_tier.id,
                                loc_in_warehouse=loc_in_warehouse,
                            ))
                        session.commit()
                    except IntegrityError:
                        print(f'Location {loc_code} already exists')
                        session.rollback()

        # for loc_rec, row_rec, bin_rec, tier_rec in session.query(
        for loc_rec in session.query(
                self.Location).join(
                self.LocRow).join(
                self.LocBin).join(
                self.LocTier):
            print(
                f'Location: {loc_rec.loc_code} {loc_rec.loc_descr}'
                f'({loc_rec.locrow.loc_row_descr}/'
                f'{loc_rec.locbin.loc_bin_descr}/'
                f'{loc_rec.loctier.loc_tier_descr})'
            )


class Main:
    """
    Main class to start things rolling.
    """

    def __init__(self):
        """
        Get things started.
        """
        self.LoadLocData = None
        return

    def run_load_loc_data(self):
        """
        Prepare to run Load location data into tables.

        :return:
        """
        self.LoadLocData = LoadLocationDataClass()
        debug('Starting up LoadLocData')
        self.LoadLocData.run_load_loc_data()
        return

    @staticmethod
    def start_logging(work_dir: Path, debug_name: str):
        """
        Establish the logging for all the other scripts.

        :param work_dir:
        :param debug_name:
        :return: (nothing)
        """

        # Set flag that no logging has been established
        logging_started = False

        # find our working directory and possible logging input file
        _workdir = work_dir
        _logfilename = debug_name

        # obtain the full path to the log information
        _debugConfig = _workdir / _logfilename

        # verify that the file exists before trying to open it
        if Path.exists(_debugConfig):
            try:
                #  get the logging params from yaml file and instantiate a log
                with open(_logfilename, 'r') as _logdictfd:
                    _logdict = yaml.load(_logdictfd, Loader=yaml.SafeLoader)
                logging.config.dictConfig(_logdict)
                logging_started = True
            except Exception as xcp:
                print(f'The file {_debugConfig} exists, but does not contain '
                      f'appropriate logging directives.')
                raise ValueError('Invalid logging directives.')
        else:
            print(f'Logging directives file {_debugConfig} either not '
                  f'specified or not found')

        if not logging_started:
            # set up minimal logging
            _logfilename = 'debuginfo.txt'
            _debugConfig = _workdir / _logfilename
            logging.basicConfig(filename='debuginfo.txt', level=logging.INFO,
                                filemode='w')
            print(f'Minimal logging established to {_debugConfig}')

        # start logging
        global log
        log = logging.getLogger(__name__)
        logging.info(f'Logging started: working directory is {_workdir}')
        return


if __name__ == "__main__":
    workdir = Path.cwd()
    debug_file_name = 'debug_info.yaml'
    main = Main()
    main.start_logging(workdir, debug_file_name)
    main.run_load_loc_data()

# EOF
